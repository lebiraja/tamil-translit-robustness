"""Retry wrapper for long unattended runs: a crash is logged and retried (training resumes from last.pt)."""

from __future__ import annotations

import time
import traceback
from collections.abc import Callable
from datetime import datetime
from typing import TypeVar

from .data import ROOT

T = TypeVar("T")


def with_retries(fn: Callable[[], T], label: str, tries: int = 3, wait_s: float = 120.0) -> T | None:
    """Call ``fn``; on an exception log it to logs/failed_runs.txt and retry. Returns None if every try failed."""
    for k in range(1, tries + 1):
        try:
            return fn()
        except Exception:  # noqa: BLE001 - deliberately broad: keep the unattended queue alive
            tb = traceback.format_exc()
            print(f"!! {label} failed (try {k}/{tries})\n{tb}", flush=True)
            (ROOT / "logs").mkdir(exist_ok=True)
            with open(ROOT / "logs/failed_runs.txt", "a") as f:
                f.write(f"{datetime.now().isoformat(timespec='seconds')} {label} try {k}/{tries}\n{tb}\n")
            if k < tries:
                time.sleep(wait_s)
    return None
