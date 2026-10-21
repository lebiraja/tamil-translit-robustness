"""Random-search tuning, equal budget per (architecture, size). Selection uses dev CER (beam 10) only.

  python scripts/tune.py lstm 3m [--trials 20]
Writes results/tune/<arch>-<size>-t<k>.json per trial and configs/best_<arch>_<size>.yaml (resumable).
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from translit.train import ROOT, Config, run  # noqa: E402

SIZES = {"1m": 1_000_000, "3m": 3_000_000, "8m": 8_000_000}


def sample(arch: str, rng: random.Random) -> dict:
    cfg = dict(
        lr=10 ** rng.uniform(-3.5, -2.5),
        batch_size=rng.choice([64, 128, 256, 512]),
        dropout=rng.choice([0.1, 0.2, 0.3, 0.4]) if arch == "lstm" else rng.choice([0.05, 0.1, 0.2, 0.3]),
        label_smoothing=rng.choice([0.0, 0.05, 0.1]),
        epochs=60, patience=6,
    )
    if arch == "transformer":
        cfg["warmup"] = rng.choice([400, 800, 1600, 3200])
    return cfg


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("arch")
    ap.add_argument("size")
    ap.add_argument("--trials", type=int, default=20)
    a = ap.parse_args()
    rng = random.Random(f"tune-{a.arch}-{a.size}")
    best = (1e9, None)
    for k in range(a.trials):
        hp = sample(a.arch, rng)
        name = f"{a.arch}-{a.size}-t{k}"
        f = ROOT / "results/tune" / f"{name}-s100.json"
        if f.exists():
            r = json.loads(f.read_text())
        else:
            r = run(Config(name=name, arch=a.arch, params=SIZES[a.size], seed=100, noisy_suite=None, independent_suite=None,
                           eval_test=False, out_dir="results/tune", **hp))
        cer = r["dev"]["cer"]
        print(f"{name} dev CER {cer:.2f} hp {hp}", flush=True)
        if cer < best[0]:
            best = (cer, hp)
    out = ROOT / "configs" / f"best_{a.arch}_{a.size}.yaml"
    out.write_text(yaml.safe_dump(best[1] | {"_dev_cer_beam10": round(best[0], 3)}))
    print("best", best)


if __name__ == "__main__":
    main()
