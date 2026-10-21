"""python scripts/train.py configs/baseline_lstm.yaml [key=value ...]   (e.g. seed=3 epochs=2)"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from translit.train import Config, run  # noqa: E402


def main() -> None:
    cfg = yaml.safe_load(open(sys.argv[1])) if len(sys.argv) > 1 and "=" not in sys.argv[1] else {}
    for kv in (a for a in sys.argv[1:] if "=" in a):
        k, v = kv.split("=", 1)
        cfg[k] = yaml.safe_load(v)
    res = run(Config(**cfg))
    keys = ("dev", "test")
    print(json.dumps({k: res[k] for k in keys if k in res} | {"n_params": res["n_params"], "wall_s": res["wall_s"]}, indent=1))


if __name__ == "__main__":
    main()
