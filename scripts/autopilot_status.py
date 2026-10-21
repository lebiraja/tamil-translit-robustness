"""Print the experiment stage and the next action. No dependencies (plain python3). Used by the autopilot Stop hook
and by the Leica Claude session: `python3 scripts/autopilot_status.py [--json]`."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
N_TUNE, N_BEST, N_C3, N_C2 = 120, 6, 30, 80  # 6 combos x 20 trials; 6 configs; 2x3x5 runs; 2 archs x 8 conditions x 5 seeds


def count(p: str, pat: str = "*.json") -> int:
    d = ROOT / p
    return len(list(d.glob(pat))) if d.exists() else 0


def running() -> list[str]:
    out = subprocess.run(["pgrep", "-fa", r"scripts/(tune|run_matrix|train|evaluate_ckpt|aggregate)\.py"], capture_output=True, text=True).stdout
    return [l[:110] for l in out.splitlines() if "pgrep" not in l]


def status() -> dict:
    s = {
        "tune_trials": count("results/tune"), "best_configs": count("configs", "best_*.yaml"),
        "c3_runs": count("results/c3"), "c2_runs": count("results/c2"),
        "summary_written": (ROOT / "results/summary/summary.json").exists(),
        "item_dumps": count("results/items", "*.npz"),
        "done": (ROOT / "logs/AUTOPILOT_DONE").exists(), "running": running(),
    }
    if s["done"]:
        s["stage"], s["next"] = "done", "Nothing. Autopilot finished."
    elif s["best_configs"] < N_BEST:
        s["stage"] = "tuning"
        s["next"] = ("Tuning is in progress (scripts/tune.py). If no tune job is running, relaunch the missing combos from AUTOPILOT.md "
                     "section 3 (they resume; finished trials are skipped).")
    elif s["c3_runs"] < N_C3:
        s["stage"] = "c3"
        s["next"] = "Run: .venv/bin/python scripts/run_matrix.py c3 (resumable). Check logs/c3.log."
    elif s["c2_runs"] < N_C2:
        s["stage"] = "c2"
        s["next"] = "Run: .venv/bin/python scripts/run_matrix.py c2 (resumable). Check logs/c2.log."
    elif not s["summary_written"]:
        s["stage"] = "analysis"
        s["next"] = "Do AUTOPILOT.md sections 5-7: write and run evaluate_ckpt.py and aggregate.py, then the docs and the final commit."
    else:
        s["stage"] = "wrap-up"
        s["next"] = "Finish docs (STATUS, HANDOVER, FIXES, docs/results.md), commit, then `echo done > logs/AUTOPILOT_DONE`."
    return s


if __name__ == "__main__":
    st = status()
    if "--json" in sys.argv:
        print(json.dumps(st))
    else:
        print(f"STAGE {st['stage']} | tune {st['tune_trials']}/{N_TUNE} (best cfgs {st['best_configs']}/{N_BEST}) | c3 {st['c3_runs']}/{N_C3} | "
              f"c2 {st['c2_runs']}/{N_C2} | summary {st['summary_written']} | jobs running: {len(st['running'])}")
        for r in st["running"]:
            print("  ", r)
        print("NEXT:", st["next"])
