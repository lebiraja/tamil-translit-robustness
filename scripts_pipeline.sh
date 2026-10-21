#!/bin/sh
# Waits for tuning to finish, then runs C3 and C2 automatically (resumable; skips finished runs).
cd ~/work/tamil-translit-robustness
while [ "$(ls configs/best_*.yaml 2>/dev/null | wc -l)" -lt 6 ]; do sleep 120; done
.venv/bin/python scripts/run_matrix.py c3 > logs/c3.log 2>&1
.venv/bin/python scripts/run_matrix.py c2 > logs/c2.log 2>&1
echo done > logs/pipeline.done
