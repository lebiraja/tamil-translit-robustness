"""Run an experiment block sequentially, skipping runs whose result JSON already exists (resumable).

  python scripts/run_matrix.py gate        # reproduction gate: lstm + transformer, 3M, seed 0 (laptop OK)
  python scripts/run_matrix.py c3          # 2 archs x 3 sizes x 5 seeds, clean training (Leica)
  python scripts/run_matrix.py c2          # A0..A4 + control x 2 archs x 5 seeds at the chosen size (Leica)
Options: --dry (print only), --seeds 0,1,2, --size 3000000
Block c2 needs data/synth/a3_sampled.tsv and a3_greedy.tsv (scripts/synthesize_a3.py) first.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from translit.retry import with_retries  # noqa: E402
from translit.train import ROOT, Config, run  # noqa: E402

SIZES = {"1m": 1_000_000, "3m": 3_000_000, "8m": 8_000_000}
ARCH = {
    "lstm": dict(epochs=80, patience=8, lr=1e-3, dropout=0.2),
    "transformer": dict(epochs=120, patience=10, lr=7e-4, warmup=800, dropout=0.1, label_smoothing=0.1),
}
C2 = {  # name -> overrides
    "A0": {},
    "A1": dict(augment="random"),
    "A2": dict(augment="phon"),
    "A3": dict(extra_pairs=["data/synth/a3_sampled.tsv"]),
    "A4": dict(augment="phon", extra_pairs=["data/synth/a3_sampled.tsv"]),
    "CTRL": dict(extra_pairs=["data/synth/a3_greedy.tsv"]),
    "A2-noGEM": dict(augment="phon", held_out=["GEM"]),
    "A2-noVDROP": dict(augment="phon", held_out=["V-DROP"]),
}


def tuned(arch: str, size_name: str) -> dict:
    """Best config from scripts/tune.py if present, else the defaults in ARCH."""
    f = ROOT / "configs" / f"best_{arch}_{size_name}.yaml"
    if f.exists():
        import yaml

        return {k: v for k, v in yaml.safe_load(f.read_text()).items() if not k.startswith('_')}
    return ARCH[arch]


def plan(block: str, seeds: list[int], size: int) -> list[Config]:
    out: list[Config] = []
    if block == "gate":
        for a, kw in ARCH.items():
            out.append(Config(name=f"gate-{a}-3m", arch=a, params=3_000_000, seed=0, out_dir="results/gate", **kw))
    elif block == "c3":
        for a, kw in ARCH.items():
            for sn, sp in SIZES.items():
                for s in seeds:
                    out.append(Config(name=f"c3-{a}-{sn}", arch=a, params=sp, seed=s, out_dir="results/c3", **tuned(a, sn)))
    elif block == "c2":
        for a in ARCH:
            kw = tuned(a, "3m")
            for cond, ov in C2.items():
                for s in seeds:
                    out.append(Config(name=f"c2-{a}-{cond}", arch=a, params=size, seed=s, out_dir="results/c2", **(kw | ov)))
    else:
        raise SystemExit(f"unknown block {block}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("block")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--size", type=int, default=3_000_000)
    a = ap.parse_args()
    cfgs = plan(a.block, [int(x) for x in a.seeds.split(",")], a.size)
    for i, c in enumerate(cfgs, 1):
        sz = next((k for k, v in SIZES.items() if v == c.params), None)
        if a.block in ("c3", "c2") and not (ROOT / "configs" / f"best_{c.arch}_{sz or '3m'}.yaml").exists():
            print(f"[{i}/{len(cfgs)}] {c.name} seed {c.seed} SKIPPED: tuned config best_{c.arch}_{sz}.yaml not ready", flush=True)
            continue
        done = ROOT / c.out_dir / f"{c.name}-s{c.seed}.json"
        print(f"[{i}/{len(cfgs)}] {c.name} seed {c.seed} {'(done)' if done.exists() else ''}", flush=True)
        if a.dry or done.exists():
            continue
        r = with_retries(lambda c=c: run(c), f"{c.name}-s{c.seed}")
        if r is None:
            continue
        print(f"   dev CER {r['dev']['cer']:.2f} top1 {r['dev']['top1']:.1f} | test CER {r['test']['cer']:.2f} top1 {r['test']['top1']:.1f}")


if __name__ == "__main__":
    main()
