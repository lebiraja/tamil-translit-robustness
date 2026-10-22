"""python scripts/finetune.py [key=value ...]   e.g. limit_ak=20000 epochs=1 name=smoke"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from translit.finetune import FTConfig, run  # noqa: E402

if __name__ == "__main__":
    cfg = {k: yaml.safe_load(v) for k, v in (a.split("=", 1) for a in sys.argv[1:] if "=" in a)}
    r = run(FTConfig(**cfg))
    print(json.dumps({k: r[k] for k in ("dev", "test", "n_params", "trainable_params", "wall_s")}, indent=1))
