"""Claude Code Stop hook for unattended runs on Leica.

When the Claude session finishes a turn it would normally go idle. This hook instead waits (cheaply, no tokens) until the
experiment state changes (a result file appears or a job exits) or 30 minutes pass, then blocks the stop and feeds Claude
the current status and next action, so it keeps working until logs/AUTOPILOT_DONE exists. Escape hatch: if nothing is
running and the status is unchanged for 3 consecutive wake-ups, it lets Claude stop and writes logs/AUTOPILOT_STUCK.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from autopilot_status import status  # noqa: E402

MAX_WAIT_S, POLL_S = int(os.environ.get("AUTOPILOT_MAX_WAIT", 5400)), int(os.environ.get("AUTOPILOT_POLL", 60))


def signature(s: dict) -> tuple:
    """Wake only on real events (a config finished, a stage advanced, a job started or exited), not on every trial/run."""
    return (s["best_configs"], s["c3_runs"] // 10, s["c2_runs"] // 20, s["summary_written"], s["item_dumps"] // 20, len(s["running"]))


def main() -> None:
    try:
        json.load(sys.stdin)
    except Exception:
        pass
    s0 = status()
    if s0["done"]:
        return
    (ROOT / "logs").mkdir(exist_ok=True)
    t0 = time.time()
    if s0["running"]:
        while time.time() - t0 < MAX_WAIT_S:
            time.sleep(POLL_S)
            if signature(status()) != signature(s0):
                break
    s = status()
    if s["done"]:
        return
    state_f = ROOT / "logs/.autopilot_state.json"
    prev = json.loads(state_f.read_text()) if state_f.exists() else {"sig": None, "same": 0}
    same = prev["same"] + 1 if (not s["running"] and prev["sig"] == list(signature(s))) else 0
    state_f.write_text(json.dumps({"sig": list(signature(s)), "same": same}))
    if same >= 3:
        (ROOT / "logs/AUTOPILOT_STUCK").write_text(json.dumps(s, indent=1))
        return
    reason = (
        "AUTOPILOT: keep going; do not ask the user anything. Read AUTOPILOT.md if you have not this session.\n"
        f"Stage: {s['stage']}. Counts: tune {s['tune_trials']}/120, best configs {s['best_configs']}/6, c3 {s['c3_runs']}/30, c2 {s['c2_runs']}/80, "
        f"summary written: {s['summary_written']}. Jobs running: {len(s['running'])}.\nNEXT ACTION: {s['next']}\n"
        "If jobs are running and there is nothing useful to do, reply with one line and stop; the hook will wake you when something changes. "
        "Record anything notable in STATUS.md and commit locally."
    )
    print(json.dumps({"decision": "block", "reason": reason}))


if __name__ == "__main__":
    main()
