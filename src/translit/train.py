"""Training loop, early stopping on dev CER, results JSON."""

from __future__ import annotations

import json
import os
import random
import subprocess
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from pydantic import BaseModel
from torch.utils.data import DataLoader

from . import data as D
from .augment import Policy
from .evaluate import evaluate
from .models import build, config_for_budget, n_params

ROOT = D.ROOT


class Config(BaseModel):
    name: str = "run"
    arch: str = "lstm"  # lstm | transformer
    direction: str = "roman2native"  # native2roman is used only to synthesise A3 data
    params: int = 3_000_000
    model_kw: dict | None = None  # overrides params budget
    seed: int = 0
    epochs: int = 60
    patience: int = 8
    batch_size: int = 128
    lr: float = 1e-3
    warmup: int = 800  # transformer inverse-sqrt warmup steps
    dropout: float = 0.2
    label_smoothing: float = 0.0
    clip: float = 1.0
    bf16: bool = False
    augment: str = "none"  # none | random | phon
    held_out: list[str] = []
    clean_frac: float = 0.4
    extra_pairs: list[str] = []  # TSV files of roman<TAB>native added to training (A3, control)
    noisy_suite: str | None = "data/synth/noisy_test"  # dir of test.<OP>.<p>.tsv, evaluated at the end
    independent_suite: str | None = "data/synth/independent"  # Aksharantar non-Dakshina sets
    beam: int = 10
    resume: bool = True  # save last.pt every epoch and continue from it if present
    eval_test: bool = True  # False for tuning runs: selection must use dev only
    out_dir: str = "results/runs"
    ckpt_dir: str = "runs"


def set_seed(s: int) -> None:
    random.seed(s)
    np.random.seed(s)
    torch.manual_seed(s)
    torch.cuda.manual_seed_all(s)


def save_last(path: Path, model, opt, sched, ep: int, best: float, bad: int, hist: list, dev: str) -> None:
    """Atomic per-epoch training state (write a temp file, then rename), so a crash or power cut cannot corrupt it."""
    tmp = path.with_suffix(".tmp")
    torch.save({"model": model.state_dict(), "opt": opt.state_dict(), "sched": sched.state_dict(), "epoch": ep, "best": best,
                "bad": bad, "hist": hist, "rng_cpu": torch.get_rng_state(),
                "rng_cuda": torch.cuda.get_rng_state() if dev == "cuda" else None}, tmp)
    os.replace(tmp, path)


def git_commit() -> str:
    try:
        return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], text=True).strip()
    except Exception:
        return "unknown"


def read_pairs(path: str) -> list[tuple[str, str]]:
    out = []
    for line in (ROOT / path).read_text(encoding="utf-8").splitlines():
        r, n, *_ = line.split("\t")
        out.append((D.norm_roman(r), D.nfc(n)))
    return out


def eval_sets(rows):
    table = D.reference_table(rows)
    ins = sorted(table)
    return ins, [table[i] for i in ins]


def load_suite(path: Path):
    """Noisy test TSV: clean_roman, noisy_roman, refs joined by '|'."""
    clean, noisy, refs = [], [], []
    for line in path.read_text(encoding="utf-8").splitlines()[1:]:
        c, n, r = line.split("\t")
        clean.append(c)
        noisy.append(n)
        refs.append(r.split("|"))
    return clean, noisy, refs


@torch.no_grad()
def dev_loss(model, vocab, items, dev: str) -> float:
    model.eval()
    tot = cnt = 0.0
    for src, tgt in DataLoader(D.PairDataset(items, vocab), batch_size=256, collate_fn=D.collate):
        src, tgt = src.to(dev), tgt.to(dev)
        lg = model(src, tgt[:, :-1])
        tot += F.cross_entropy(lg.reshape(-1, lg.size(-1)), tgt[:, 1:].reshape(-1), ignore_index=0, reduction="sum").item()
        cnt += (tgt[:, 1:] != 0).sum().item()
    return tot / cnt


def run(cfg: Config) -> dict:
    t0 = time.time()
    set_seed(cfg.seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    rows = {s: D.load_lexicon(s) for s in D.SPLITS}
    base = D.pairs(rows["train"])
    extra = [p for f in cfg.extra_pairs for p in read_pairs(f)]
    train_pairs = sorted(set(base) | set(extra))
    vocab = D.Vocab.build(base + extra)
    if cfg.direction == "native2roman":  # swap roles: input native, output roman
        vocab = D.Vocab.build([(n, r) for r, n in train_pairs])
        train_pairs = [(n, r) for r, n in train_pairs]
    kw = cfg.model_kw or config_for_budget(cfg.arch, cfg.params, len(vocab.src), len(vocab.tgt))
    kw = dict(kw, dropout=cfg.dropout)
    model = build(cfg.arch, len(vocab.src), len(vocab.tgt), **kw).to(dev)
    policy = Policy(cfg.augment, cfg.clean_frac, tuple(cfg.held_out))
    opt = torch.optim.Adam(model.parameters(), lr=cfg.lr, betas=(0.9, 0.98), eps=1e-9)
    if cfg.arch == "transformer":
        sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min((s + 1) / cfg.warmup, (cfg.warmup / (s + 1)) ** 0.5))
    else:
        sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: 1.0)
    dev_in, dev_ref = eval_sets(rows["dev"]) if cfg.direction == "roman2native" else ([], [])
    run_id = f"{cfg.name}-s{cfg.seed}"
    ck = ROOT / cfg.ckpt_dir / run_id
    ck.mkdir(parents=True, exist_ok=True)
    best, bad, hist = 1e9, 0, []
    start = 0
    last = ck / "last.pt"
    if cfg.resume and last.exists():  # continue an interrupted run from its last finished epoch
        st = torch.load(last, map_location=dev, weights_only=False)
        model.load_state_dict(st["model"])
        opt.load_state_dict(st["opt"])
        sched.load_state_dict(st["sched"])
        best, bad, hist, start = st["best"], st["bad"], st["hist"], st["epoch"] + 1
        torch.set_rng_state(st["rng_cpu"].cpu())
        if dev == "cuda":
            torch.cuda.set_rng_state(st["rng_cuda"].cpu())
        print(f"[{run_id}] resumed after epoch {st['epoch']}", flush=True)
    for ep in range(start, cfg.epochs):
        if bad >= cfg.patience:
            break
        rng = random.Random(cfg.seed * 100003 + ep)
        items = [(policy.noisy(r, rng) if cfg.direction == "roman2native" else r, n) for r, n in train_pairs]
        loader = DataLoader(D.PairDataset(items, vocab), batch_size=cfg.batch_size, shuffle=True, collate_fn=D.collate,
                            generator=torch.Generator().manual_seed(cfg.seed * 7919 + ep))
        model.train()
        tot = cnt = 0.0
        for src, tgt in loader:
            src, tgt = src.to(dev), tgt.to(dev)
            with torch.autocast(dev, dtype=torch.bfloat16, enabled=cfg.bf16 and dev == "cuda"):
                logits = model(src, tgt[:, :-1])
            loss = F.cross_entropy(logits.float().reshape(-1, logits.size(-1)), tgt[:, 1:].reshape(-1), ignore_index=0,
                                   label_smoothing=cfg.label_smoothing)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), cfg.clip)
            opt.step()
            sched.step()
            tot += loss.item() * src.size(0)
            cnt += src.size(0)
        if cfg.direction == "roman2native":
            m, _ = evaluate(model, vocab, dev_in, dev_ref, beam=1, device=dev)
            crit = m["cer"]
        else:
            crit = dev_loss(model, vocab, [(n, r) for r, n in D.pairs(rows["dev"])], dev)
            m = {"cer": float("nan")}
        hist.append({"epoch": ep, "train_loss": tot / cnt, "dev_cer_greedy": m["cer"]})
        print(f"[{run_id}] ep{ep} loss {tot / cnt:.4f} devCER(greedy) {m['cer']:.2f}", flush=True)
        if crit < best - 1e-4:
            best, bad = crit, 0
            torch.save({"model": model.state_dict(), "kw": kw, "arch": cfg.arch, "vocab": vocab.to_json()}, ck / "best.pt")
        else:
            bad += 1
        if cfg.resume:
            save_last(last, model, opt, sched, ep, best, bad, hist, dev)
        if bad >= cfg.patience:
            break
    model.load_state_dict(torch.load(ck / "best.pt", map_location=dev)["model"])
    result: dict = {
        "config": cfg.model_dump(), "model_kw": kw, "n_params": n_params(model), "commit": git_commit(),
        "torch": torch.__version__, "gpu": torch.cuda.get_device_name(0) if dev == "cuda" else "cpu",
        "history": hist, "best_dev_crit": best,
        "metric_definition": "CER corpus-level vs closest of all attested references; top-k any reference; src/translit/metrics.py",
        "data_sha256": (D.DAKSHINA / "SHA256SUMS").read_text().split() if (D.DAKSHINA / "SHA256SUMS").exists() else [],
    }
    if cfg.direction == "roman2native":
        result["dev"], _ = evaluate(model, vocab, dev_in, dev_ref, beam=cfg.beam, device=dev)
        if cfg.eval_test:
            ti, tr = eval_sets(rows["test"])
            result["test"], _ = evaluate(model, vocab, ti, tr, beam=cfg.beam, device=dev)
        suite = ROOT / cfg.noisy_suite if cfg.noisy_suite else None
        result["noisy"] = {}
        if suite and suite.exists():
            for f in sorted(suite.glob("test.*.tsv")):
                _, noisy, refs = load_suite(f)
                result["noisy"][f.stem[5:]], _ = evaluate(model, vocab, noisy, refs, beam=cfg.beam, device=dev)
        ind = ROOT / cfg.independent_suite if cfg.independent_suite else None
        result["independent"] = {}
        if ind and ind.exists():
            for f in sorted(ind.glob("*.tsv")):
                _, noisy, refs = load_suite(f)
                result["independent"][f.stem], _ = evaluate(model, vocab, noisy, refs, beam=cfg.beam, device=dev)
    result["wall_s"] = time.time() - t0
    out = ROOT / cfg.out_dir
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{run_id}.json").write_text(json.dumps(result, indent=1, ensure_ascii=False))
    return result
