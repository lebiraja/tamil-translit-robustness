"""Per-item evaluation of trained checkpoints, for paired statistics (scripts/aggregate.py).

For every runs/<name>-s<seed>/best.pt whose name matches the prefixes (default c3-, c2-), rebuild the model from the
stored kw/vocab, decode with beam 10 on clean test, the 28 noisy suites and the 4 independent suites, and save
results/items/<run>.npz with, per suite S: S__correct (top-1 equals any reference), S__top5, S__edits (to the closest
reference), S__reflen. Item order is the fixed order of each suite file, so arrays align across runs. Resumable.

  python scripts/evaluate_ckpt.py [--prefix c3-,c2-] [--only NAME] [--check]
--check also compares the corpus CER with the run's results JSON (must agree; same decoder and data).
"""

from __future__ import annotations

import argparse
import fcntl
import json
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from translit import data as D  # noqa: E402
from translit.evaluate import translate  # noqa: E402
from translit.metrics import closest  # noqa: E402
from translit.models import build  # noqa: E402
from translit.train import eval_sets, load_suite  # noqa: E402

ROOT = D.ROOT


def suites() -> dict[str, tuple[list[str], list[list[str]]]]:
    out = {"clean": eval_sets(D.load_lexicon("test"))}
    for f in sorted((ROOT / "data/synth/noisy_test").glob("test.*.tsv")):
        _, noisy, refs = load_suite(f)
        out[f.stem[5:]] = (noisy, refs)
    for f in sorted((ROOT / "data/synth/independent").glob("*.tsv")):
        _, noisy, refs = load_suite(f)
        out[f.stem] = (noisy, refs)
    return out


def load(ck: Path, dev: str):
    s = torch.load(ck, map_location=dev)
    v = D.Vocab(s["vocab"]["src"], s["vocab"]["tgt"])
    m = build(s["arch"], len(v.src), len(v.tgt), **s["kw"]).to(dev)
    m.load_state_dict(s["model"])
    return m.eval(), v


def result_json(run: str) -> Path | None:
    for d in ("c3", "c2", "gate"):
        p = ROOT / "results" / d / f"{run}.json"
        if p.exists():
            return p
    return None


@torch.no_grad()
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prefix", default="c3-,c2-")
    ap.add_argument("--only")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    (ROOT / "logs").mkdir(exist_ok=True)
    lock = open(ROOT / "logs/locks_evaluate.lock", "w")  # single instance
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print("another evaluate_ckpt is running; exiting")
        return
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    out_dir = ROOT / "results/items"
    out_dir.mkdir(parents=True, exist_ok=True)
    cks = sorted(p for p in (ROOT / "runs").glob("*/best.pt") if p.parent.name.startswith(tuple(a.prefix.split(","))))
    if a.only:
        cks = [p for p in cks if p.parent.name == a.only]
    S = suites()
    for ck in cks:
        run = ck.parent.name
        dst = out_dir / f"{run}.npz"
        if dst.exists() or result_json(run) is None:  # skip done and unfinished runs (no results JSON yet)
            continue
        model, vocab = load(ck, dev)
        arrs: dict[str, np.ndarray] = {}
        for name, (inputs, refs) in S.items():
            nbest = translate(model, vocab, inputs, beam=10, device=dev)
            ed, ln = zip(*(closest(h[0] if h else "", r) for h, r in zip(nbest, refs, strict=True)), strict=True)
            arrs[f"{name}__edits"] = np.array(ed, dtype=np.int32)
            arrs[f"{name}__reflen"] = np.array(ln, dtype=np.int32)
            arrs[f"{name}__correct"] = np.array([bool(h) and h[0] in set(r) for h, r in zip(nbest, refs, strict=True)])
            arrs[f"{name}__top5"] = np.array([any(x in set(r) for x in h[:5]) for h, r in zip(nbest, refs, strict=True)])
        if a.check:
            js = json.loads(result_json(run).read_text())
            got = 100.0 * arrs["clean__edits"].sum() / arrs["clean__reflen"].sum()
            want = js["test"]["cer"]
            print(f"   check {run}: items CER {got:.3f} vs JSON {want:.3f}", flush=True)
            if abs(got - want) > 0.05:
                raise SystemExit(f"mismatch for {run}")
        np.savez_compressed(dst, **arrs)
        print(f"{run}: clean CER {100.0 * arrs['clean__edits'].sum() / arrs['clean__reflen'].sum():.2f}", flush=True)


if __name__ == "__main__":
    main()
