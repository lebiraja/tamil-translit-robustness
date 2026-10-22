"""Full fine-tuning of a trained checkpoint (all weights trainable, same architecture and vocabulary).

Data mix: Dakshina train (repeated), A3 sampled back-transliterations, Aksharantar train (quality-filtered), with online
noise from all six operators. The result is written in the same single-file format as every other checkpoint
({model, kw, arch, vocab}), weights only, so there is nothing to merge afterwards.
"""

from __future__ import annotations

import gzip
import json
import math
import random
import time
from pathlib import Path

import torch
import torch.nn.functional as F
from pydantic import BaseModel
from torch.utils.data import DataLoader

from . import data as D
from . import noise
from .augment import Policy
from .evaluate import evaluate
from .models import build, n_params
from .train import ROOT, eval_sets, git_commit, load_suite, read_pairs, set_seed


class FTConfig(BaseModel):
    name: str = "v2-ft"
    init: str = "models/v1-a4-transformer-3m.pt"
    seed: int = 0
    epochs: int = 5
    patience: int = 2
    batch_size: int = 512
    lr: float = 1e-4
    warmup: int = 500
    final_lr_frac: float = 0.1
    label_smoothing: float = 0.1
    clip: float = 1.0
    bf16: bool = False
    dakshina_repeat: int = 3
    a3: str = "data/synth/a3_sampled.tsv"
    ak_train: str = "data/aksharantar-tamil/tam_train.tsv.gz"
    ak_min_score: float = -0.10
    limit_ak: int = 0  # 0 = all; >0 only for smoke tests
    clean_frac: float = 0.5
    workers: int = 4
    beam: int = 10
    noisy_suite: str = "data/synth/noisy_test"
    independent_suite: str = "data/synth/independent"
    out_dir: str = "results/final"
    ckpt_dir: str = "runs"


def load_ak(path: str, min_score: float, banned: set[str], vocab: D.Vocab, limit: int) -> tuple[list[tuple[str, str]], dict]:
    """Aksharantar train rows: IndicCorp rows need score >= min_score, other sources are kept; drop banned natives."""
    sv, tv = set(vocab.src), set(vocab.tgt)
    out, st = set(), {"rows": 0, "low_score": 0, "banned_native": 0, "bad_chars": 0}
    with gzip.open(ROOT / path, "rt", encoding="utf-8") as f:
        next(f)
        for line in f:
            r = line.rstrip("\n").split("\t")
            st["rows"] += 1
            if r[2] == "IndicCorp" and len(r) > 3 and r[3] and float(r[3]) < min_score:
                st["low_score"] += 1
                continue
            n, ro = D.nfc(r[0]), D.norm_roman(r[1])
            if n in banned:
                st["banned_native"] += 1
                continue
            if not ro.isascii() or not ro.isalpha() or any(c not in sv for c in ro) or any(c not in tv for c in n):
                st["bad_chars"] += 1
                continue
            out.add((ro, n))
            if limit and len(out) >= limit:
                break
    st["kept"] = len(out)
    return sorted(out), st


def lr_at(step: int, total: int, c: FTConfig) -> float:
    if step < c.warmup:
        return c.lr * (step + 1) / c.warmup
    prog = min(1.0, (step - c.warmup) / max(1, total - c.warmup))
    return c.lr * (c.final_lr_frac + (1 - c.final_lr_frac) * 0.5 * (1 + math.cos(math.pi * prog)))


def dev_scores(model, vocab, dev_in, dev_ref, dev_mix, device):
    clean, _ = evaluate(model, vocab, dev_in, dev_ref, beam=1, device=device)
    mixed, _ = evaluate(model, vocab, dev_mix, dev_ref, beam=1, device=device)
    return clean["cer"], mixed["cer"]


def run(c: FTConfig) -> dict:
    t0 = time.time()
    set_seed(c.seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    ck = torch.load(ROOT / c.init, map_location=dev, weights_only=False)
    vocab = D.Vocab(**ck["vocab"])
    model = build(ck["arch"], len(vocab.src), len(vocab.tgt), **ck["kw"]).to(dev)
    model.load_state_dict(ck["model"])
    for p in model.parameters():  # full fine-tuning: every weight trains
        p.requires_grad_(True)
    rows = {s: D.load_lexicon(s) for s in D.SPLITS}
    banned = {n for s in ("dev", "test") for n, _, _ in rows[s]}
    for f in (ROOT / "data/synth/independent").glob("AK-all.tsv"):
        for line in f.read_text(encoding="utf-8").splitlines()[1:]:
            banned.update(line.split("\t")[2].split("|"))
    dak = D.pairs(rows["train"])
    a3 = read_pairs(c.a3)
    ak, ak_stats = load_ak(c.ak_train, c.ak_min_score, banned, vocab, c.limit_ak)
    mixture = dak * c.dakshina_repeat + a3 + ak
    mix_stats = {"dakshina_pairs": len(dak), "dakshina_repeat": c.dakshina_repeat, "a3_pairs": len(a3), "ak": ak_stats, "mixture_per_epoch": len(mixture)}
    print("data", json.dumps(mix_stats), flush=True)
    policy = Policy("all", c.clean_frac)
    dev_in, dev_ref = eval_sets(rows["dev"])
    dev_mix = [noise.noisy_variant(w, "MIX", 0.3, 777) for w in dev_in]
    opt = torch.optim.Adam(model.parameters(), lr=c.lr, betas=(0.9, 0.98), eps=1e-9)
    steps_per_epoch = math.ceil(len(mixture) / c.batch_size)
    total = steps_per_epoch * c.epochs
    run_id = f"{c.name}-s{c.seed}"
    ckd = ROOT / c.ckpt_dir / run_id
    ckd.mkdir(parents=True, exist_ok=True)
    c0, m0 = dev_scores(model, vocab, dev_in, dev_ref, dev_mix, dev)
    print(f"[{run_id}] start (v1 weights) dev CER clean {c0:.2f} MIX0.3 {m0:.2f}", flush=True)
    best, bad, step, hist = (c0 + m0) / 2, 0, 0, [{"epoch": -1, "dev_clean": c0, "dev_mix": m0}]
    torch.save({"model": model.state_dict(), "kw": ck["kw"], "arch": ck["arch"], "vocab": ck["vocab"]}, ckd / "best.pt")
    for ep in range(c.epochs):
        rng = random.Random(c.seed * 100003 + ep)
        items = [(policy.noisy(r, rng), n) for r, n in mixture]
        loader = DataLoader(D.PairDataset(items, vocab), batch_size=c.batch_size, shuffle=True, collate_fn=D.collate,
                            num_workers=c.workers, generator=torch.Generator().manual_seed(c.seed * 7919 + ep))
        model.train()
        tot = cnt = 0.0
        te = time.time()
        for src, tgt in loader:
            src, tgt = src.to(dev, non_blocking=True), tgt.to(dev, non_blocking=True)
            for g in opt.param_groups:
                g["lr"] = lr_at(step, total, c)
            with torch.autocast(dev, dtype=torch.bfloat16, enabled=c.bf16 and dev == "cuda"):
                logits = model(src, tgt[:, :-1])
            loss = F.cross_entropy(logits.float().reshape(-1, logits.size(-1)), tgt[:, 1:].reshape(-1), ignore_index=0,
                                   label_smoothing=c.label_smoothing)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), c.clip)
            opt.step()
            step += 1
            tot += loss.item() * src.size(0)
            cnt += src.size(0)
            if step % 500 == 0:
                print(f"[{run_id}] step {step}/{total} loss {tot / cnt:.4f} lr {lr_at(step, total, c):.2e} {cnt / (time.time() - te):.0f} pairs/s", flush=True)
        cl, mx = dev_scores(model, vocab, dev_in, dev_ref, dev_mix, dev)
        crit = (cl + mx) / 2
        hist.append({"epoch": ep, "train_loss": tot / cnt, "dev_clean": cl, "dev_mix": mx, "sec": time.time() - te})
        print(f"[{run_id}] ep{ep} loss {tot / cnt:.4f} devCER(greedy) {cl:.2f} | MIX0.3 {mx:.2f} | crit {crit:.2f} | {time.time() - te:.0f}s", flush=True)
        if crit < best - 1e-4:
            best, bad = crit, 0
            torch.save({"model": model.state_dict(), "kw": ck["kw"], "arch": ck["arch"], "vocab": ck["vocab"]}, ckd / "best.pt")
        else:
            bad += 1
            if bad >= c.patience:
                break
    model.load_state_dict(torch.load(ckd / "best.pt", map_location=dev, weights_only=False)["model"])
    res: dict = {"config": c.model_dump(), "model_kw": ck["kw"], "n_params": n_params(model), "commit": git_commit(), "torch": torch.__version__,
                 "gpu": torch.cuda.get_device_name(0) if dev == "cuda" else "cpu", "data": mix_stats, "history": hist, "best_crit": best,
                 "trainable_params": sum(p.numel() for p in model.parameters() if p.requires_grad)}
    res["dev"], _ = evaluate(model, vocab, dev_in, dev_ref, beam=c.beam, device=dev)
    ti, tr = eval_sets(rows["test"])
    res["test"], _ = evaluate(model, vocab, ti, tr, beam=c.beam, device=dev)
    res["noisy"], res["independent"] = {}, {}
    for f in sorted((ROOT / c.noisy_suite).glob("test.*.tsv")):
        _, noisy, refs = load_suite(f)
        res["noisy"][f.stem[5:]], _ = evaluate(model, vocab, noisy, refs, beam=c.beam, device=dev)
    for f in sorted((ROOT / c.independent_suite).glob("*.tsv")):
        _, noisy, refs = load_suite(f)
        res["independent"][f.stem], _ = evaluate(model, vocab, noisy, refs, beam=c.beam, device=dev)
    res["wall_s"] = time.time() - t0
    out = ROOT / c.out_dir
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{run_id}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    return res
