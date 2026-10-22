"""Unattended supervisor for Leica (plain python3, stdlib only apart from run_matrix's imports).

Every POLL_S it: logs health every 30 min, refuses to launch anything unless the kernel is the known-good one and the GPU is
cool, and launches whatever work is missing (tuning combos, C3, C2, per-item evaluation, aggregation) within a GPU-job cap.
Everything it launches is resumable, so it is safe to start it any number of times; a lock file allows one instance.
It never kills processes, never uses sudo and only starts this project's own scripts.

  python3 scripts/supervisor.py            # run forever (cron starts it every 10 min under flock)
  python3 scripts/supervisor.py --once     # one pass, then exit (also: --dry to print what it would launch)
"""

from __future__ import annotations

import argparse
import fcntl
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv/bin/python")
KERNEL_OK = "6.17.0-22-generic"
MAX_GPU_JOBS, MAX_TEMP, POLL_S, HEALTH_S = 4, 85, 300, 1800
MAX_EVAL_BUSY, MAX_EVAL_IDLE = 2, 3  # parallel evaluators (per-model locks); fewer while training runs, RAM is 15 GB
TUNE = [(a, s) for a in ("lstm", "transformer") for s in ("1m", "3m", "8m")]
SEED_SPLITS = ["0,1,2", "3,4"]
N = {"c3": 30, "c2": 80}


def log(msg: str) -> None:
    line = f"{datetime.now().isoformat(timespec='seconds')} {msg}"
    print(line, flush=True)
    (ROOT / "logs").mkdir(exist_ok=True)
    with open(ROOT / "logs/supervisor.log", "a") as f:
        f.write(line + "\n")


def sh(*cmd: str) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()


def running(pattern: str) -> int:
    """Count python processes whose command line is '<python> <pattern>' (anchored, so sh -c wrappers do not match)."""
    return len([p for p in sh("pgrep", "-f", r"^\S*python\S* " + pattern).splitlines() if p.strip()])


def gpu_jobs() -> int:
    return running(r"scripts/(tune|run_matrix|evaluate_ckpt)\.py")


def count(rel: str, pat: str = "*.json") -> int:
    d = ROOT / rel
    return len(list(d.glob(pat))) if d.exists() else 0


def temp() -> int:
    try:
        return int(sh("nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader"))
    except ValueError:
        return 999


def launch(args: list[str], logname: str, dry: bool) -> None:
    log(f"LAUNCH {' '.join(args)} -> logs/{logname}")
    if dry:
        return
    out = open(ROOT / "logs" / logname, "a")
    subprocess.Popen([PY, *args], cwd=ROOT, stdout=out, stderr=out, stdin=subprocess.DEVNULL, start_new_session=True)


def pending(block: str, seeds: str) -> int:
    """Runs of this seed split that are not finished and whose tuned config exists (read from run_matrix --dry)."""
    out = sh(PY, "scripts/run_matrix.py", block, "--seeds", seeds, "--dry")
    return sum(1 for l in out.splitlines() if l.startswith("[") and "(done)" not in l and "SKIPPED" not in l)


def health() -> None:
    from autopilot_status import status

    s = status()
    log(f"HEALTH kernel {sh('uname', '-r')} gpu {sh('nvidia-smi', '--query-gpu=name,temperature.gpu,memory.used', '--format=csv,noheader')} "
        f"| {s['stage']} tune {s['tune_trials']}/120 best {s['best_configs']}/6 c3 {s['c3_runs']}/30 c2 {s['c2_runs']}/80 "
        f"items {s['item_dumps']} | failed_runs.txt {'yes' if (ROOT / 'logs/failed_runs.txt').exists() else 'no'}")


def step(dry: bool) -> None:
    if sh("uname", "-r") != KERNEL_OK:
        log(f"WAIT wrong kernel {sh('uname', '-r')}; launching nothing")
        return
    if temp() > MAX_TEMP:
        log(f"WAIT GPU too hot ({temp()} C); launching nothing")
        return
    slots = MAX_GPU_JOBS - gpu_jobs()

    def room() -> bool:
        return slots > 0

    for arch, size in TUNE:  # tuning combos not finished and not running
        if room() and not (ROOT / f"configs/best_{arch}_{size}.yaml").exists() and not running(f"scripts/tune.py {arch} {size}"):
            launch(["scripts/tune.py", arch, size], f"tune_{arch}{size}.log", dry)
            slots -= 1
    for block in ("c3", "c2"):
        if block == "c2" and count("results/c3") < N["c3"]:
            continue
        for seeds in SEED_SPLITS:
            if room() and pending(block, seeds) and not running(f"scripts/run_matrix.py {block} --seeds {seeds}"):
                launch(["scripts/run_matrix.py", block, "--seeds", seeds], f"{block}_{seeds.replace(',', '')}.log", dry)
                slots -= 1
    done_runs = count("results/c3") + count("results/c2")
    todo = done_runs - count("results/items", "*.npz")
    max_eval = MAX_EVAL_BUSY if running(r"scripts/(tune|run_matrix)\.py") else MAX_EVAL_IDLE
    while room() and todo > running("scripts/evaluate_ckpt.py") and running("scripts/evaluate_ckpt.py") < max_eval:
        launch(["scripts/evaluate_ckpt.py", "--check"], f"evaluate_{running('scripts/evaluate_ckpt.py') + 1}.log", dry)
        slots -= 1
        if dry:
            break
        time.sleep(3)  # let the new process appear before counting again
    all_done = count("results/c3") >= N["c3"] and count("results/c2") >= N["c2"]
    if (all_done and count("results/items", "*.npz") >= done_runs and not running("scripts/evaluate_ckpt.py")
            and not (ROOT / "results/summary/summary.json").exists() and not running("scripts/aggregate.py")):
        launch(["scripts/aggregate.py"], "aggregate.log", dry)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    sys.path.insert(0, str(ROOT / "scripts"))
    lock = open(ROOT / "logs/supervisor.lock", "w") if (ROOT / "logs").exists() else None
    if lock and not a.dry:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return  # another supervisor is running
    last_health = 0.0
    while True:
        if (ROOT / "logs/AUTOPILOT_DONE").exists():
            log("AUTOPILOT_DONE exists; supervisor exits")
            return
        try:
            if time.time() - last_health > HEALTH_S:
                health()
                last_health = time.time()
            step(a.dry)
        except Exception as e:  # noqa: BLE001 - the supervisor itself must not die
            log(f"ERROR {type(e).__name__}: {e}")
        if a.once or a.dry:
            return
        time.sleep(POLL_S)


if __name__ == "__main__":
    main()
