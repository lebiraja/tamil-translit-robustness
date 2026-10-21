#!/bin/sh
# Waits for tuning and the early C3 workers, then finishes C3 (Transformer-8M) and runs C2 (resumable; skips finished runs).
cd ~/work/tamil-translit-robustness
while [ "$(ls configs/best_*.yaml 2>/dev/null | wc -l)" -lt 6 ]; do sleep 120; done
while pgrep -f "run_matrix.py c3 --seeds" > /dev/null; do sleep 60; done
.venv/bin/python scripts/run_matrix.py c3 --seeds 0,1,2 > logs/c3_c.log 2>&1 &
.venv/bin/python scripts/run_matrix.py c3 --seeds 3,4 > logs/c3_d.log 2>&1
wait
.venv/bin/python scripts/run_matrix.py c2 --seeds 0,1,2 > logs/c2_a.log 2>&1 &
.venv/bin/python scripts/run_matrix.py c2 --seeds 3,4 > logs/c2_b.log 2>&1
wait
echo done > logs/pipeline.done
