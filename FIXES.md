# FIXES

Prepend an entry for each real bug or documentation error fixed: symptom, root cause, fix with `file:line`, verification. Newest on top. No code exists yet, so these are documentation and process fixes.

## F3 · 2026-10-22 · Supervisor launched duplicate workers; evaluation starved
- **Symptom:** three `run_matrix.py c2 --seeds 0,1,2` processes trained the same run at once (identical loss lines in the log); the per-item evaluation sat at 31/110 for hours; one run crashed with `FileNotFoundError: last.tmp -> last.pt` (two processes sharing one checkpoint folder).
- **Root cause:** `scripts/supervisor.py` checked for a running worker with the pattern `run_matrix.py <block> --seeds <s>` while `running()` anchors the match as `<python> <pattern>`, so it never matched `python scripts/run_matrix.py ...`. The supervisor believed no worker existed and launched another each cycle (about 17:06 onward); duplicates filled the 3 GPU slots, so evaluation never got one.
- **Fix:** pattern now starts with `scripts/` (supervisor.py, `running(f"scripts/run_matrix.py ...")`); `run_matrix.py` takes a per-run flock (`logs/locks/<run>.lock`) so two processes never train one run; `evaluate_ckpt.py` takes a per-model lock, saves atomically and logs score mismatches to `logs/eval_mismatch.txt`. Commits 9a729b9, 9f01dd5.
- **Impact:** 33 of the 72 C2 runs finished by 09:20 (seeds 0-2, finished after 23:56) overlapped with a duplicate. A clean BiLSTM rerun (c2-lstm-A2-noGEM-s0) reproduced the stored result exactly (test CER 10.0306, dev 9.2760, 18 epochs). A clean Transformer re-run differed within normal variation (9.30 vs 9.13 test CER). The evaluator re-scored all 110 stored checkpoints against their logs: only c2-transformer-CTRL-s1 did not reproduce (8.43 vs 8.49); it was moved to quarantine/ (not deleted), retrained cleanly and now matches (8.899 vs 8.899). Whether to retrain the other 32 overlapped runs is left to Lebi (see docs/results.md section 5).
## F2 · 2026-10-18 · Leftover "laptop RTX 5070" in D10
- **Symptom:** `DECISIONS.md` row D10 still said the laptop was an RTX 5070 after F1 had been applied elsewhere.
- **Root cause:** F1 corrected D7, `CLAUDE.md` and `HANDOVER.md` but D10 was missed.
- **Fix:** `DECISIONS.md` D10 changed to "laptop RTX 4050 for development" (commit `7522579`); the later rewrite of `DECISIONS.md` keeps the correct values in D7 and D10.
- **Verification:** ran `grep -rn "laptop.*5070" --include=*.md .`; every match either states the correct split (laptop RTX 4050, Leica RTX 5070) or describes the mistake itself.

## F1 · 2026-10-18 · Wrong GPU attributed to the laptop
- **Symptom:** early docs said the laptop has an RTX 5070 (12 GB, Blackwell) and planned PyTorch for it.
- **Root cause:** Lebi pasted the 5070 spec while saying "my lab system"; it was recorded as the laptop's GPU without checking. The lab docs (`/home/lebi/workspace/networks/dscs-lab/`, README and file 08) show the laptop `rog` has an RTX 4050 6 GB and the lab server Leica has the RTX 5070 12 GB.
- **Fix:** `DECISIONS.md` D7, `CLAUDE.md` rules, `HANDOVER.md` next steps rewritten to the correct split (laptop dev, Leica long runs); `docs/infrastructure.md` created with the verified specs and the Leica constraints.
- **Verification:** compared against `dscs-lab/README.md` ("Laptop RTX 4050 6 GB", "Leica RTX 5070 12 GB") and file 08 context section.

## Process notes (not bugs, recorded for the next session)
- Two dataset agents hit "No response from API" timeouts mid-task; fixed by resuming with a narrower brief and writing docs in small pieces. One doc had already been written before the timeout.
- Overlapping scope between the two dataset agents (both downloaded informal sets) was resolved by splitting ownership explicitly (pair sets versus informal sets).
- Idle and duplicate agent notifications were relayed to Lebi and confused them; relay only actionable news.
