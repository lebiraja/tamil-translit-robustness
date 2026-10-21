# AUTOPILOT: unattended run on Leica

You are the Claude session running on the lab server Leica, in `/home/lebiraja/work/tamil-translit-robustness`. Lebi has left (laptop off, monitor off). Your job is to take the project from "tuning is running" to "all experiments done, analysed and documented", with no human in the loop. A Stop hook (`scripts/autopilot_hook.py`) wakes you whenever the state changes and tells you the next action; run `python3 scripts/autopilot_status.py` any time to see it. You are finished only when `logs/AUTOPILOT_DONE` exists.

Read first: `CLAUDE.md`, `DECISIONS.md`, `docs/experiment-plan.md`, `docs/datasets/final-dataset.md`, top of `STATUS.md`, `HANDOVER.md`. Do not ask the user questions. Decide, act, document why.

## 1. What the project is (one paragraph)
Latin-script (Tanglish) to Tamil-script word transliteration with character-level seq2seq models. We measure how much typing noise hurts (C1 paired noisy test sets), which training augmentation helps (C2: A0 baseline, A1 random char noise, A2 Tamil-phonological noise, A3 sampled back-transliteration, A4 = A2+A3, CTRL = greedy romanization of the same words), and whether a BiLSTM+attention or a small pre-LN Transformer is more robust at matched size and tuning (C3: 1M/3M/8M parameters, 5 seeds). Output is an IEEE paper (written on the laptop later) so every number must come from a logged run.

## 2. State already done (do not redo)
- Code in `src/translit/`, scripts in `scripts/`, tests pass (`.venv/bin/python -m pytest tests -q`, expect 20 passed).
- Data on this machine: `data/dakshina-ta/`, `data/synth/noisy_test/` (28 suites), `data/synth/independent/` (AK-Freq, AK-NEI, AK-NEF, AK-all), `data/synth/native_pool.tsv`, `data/synth/a3_sampled.tsv` (123,488 pairs), `data/synth/a3_greedy.tsv` (60,000 pairs). If any is missing: `python scripts/prepare_data.py all` regenerates the first three kinds; `python scripts/train.py configs/reverse_lstm.yaml` then `python scripts/synthesize_a3.py --k 3` regenerates A3.
- Reproduction gate passed (BiLSTM dev CER 8.95, Transformer 9.38; `results/gate/`).
- Tuning started: `scripts/tune.py` runs 20 random-search trials per (arch,size) on dev CER only; writes `results/tune/` and `configs/best_<arch>_<size>.yaml`. A watcher `scripts_pipeline.sh` (started separately) launches `run_matrix.py c3` then `c2` once all 6 best configs exist.
- The private WhatsApp and human-typed sets are NOT on this machine and must not be copied here. They are evaluated later on the laptop.

## 3. Stage runbook
Always work in the repo root with `.venv/bin/python`. Long jobs: `setsid nohup ... > logs/<name>.log 2>&1 < /dev/null &` so they survive your session.
1. **Tuning (stage `tuning`).** Three workers: `tune.py lstm 1m; lstm 8m` | `lstm 3m; transformer 1m` | `transformer 3m; transformer 8m`. If a worker died, relaunch its missing combos (finished trials are skipped, so rerunning is safe): `setsid nohup .venv/bin/python scripts/tune.py <arch> <size> > logs/tune_<arch><size>.log 2>&1 < /dev/null &`. When BiLSTM workers finish early, start the Transformer 8m combo in its own worker so it does not wait in line. Do not run more than 4 GPU jobs at once (12 GB GPU, 15 GB RAM).
2. **C3 (stage `c3`).** `scripts_pipeline.sh` starts it; if no pipeline is running, run `.venv/bin/python scripts/run_matrix.py c3 > logs/c3.log 2>&1` (30 runs, resumable, writes `results/c3/`). To go faster you may split seeds across two processes: `--seeds 0,1,2` and `--seeds 3,4`.
3. **C2 (stage `c2`).** `run_matrix.py c2` (80 runs at 3M params with the tuned 3m configs, writes `results/c2/`; conditions A0, A1, A2, A3, A4, CTRL, A2-noGEM, A2-noVDROP).
4. If a run crashes: read the traceback, fix the cause in code (add a regression test if it is logic), log it in `FIXES.md`, rerun. If CUDA out-of-memory with parallel jobs, lower parallelism, not batch size (batch size is a tuned hyperparameter). A run that diverges (loss NaN) is a real finding: keep it, log it, do not silently drop it.

## 4. Healthcheck (every wake-up, 5 seconds)
`uname -r` must be `6.17.0-22-generic` and `nvidia-smi` must show the RTX 5070. If not, stop all work, write the problem in `STATUS.md`, and wait; do not try to fix the kernel or driver.

Also keep the live dashboard up: `curl -s -m 3 localhost:8383/api/state >/dev/null || sh scripts/dashboard/run.sh` (port 8383, see `docs/dashboard.md`). Do not change its charts unless something is broken.

## 5. Analysis scripts you must write (stage `analysis`)
Plain numpy/scipy/pandas only (no new downloads; there is no internet beyond the Claude API). Add pytest tests with hand-computed values for the statistics helpers.
- `scripts/evaluate_ckpt.py`: for every `runs/<name>-s<seed>/best.pt` of c3 and c2, rebuild the model from the stored `kw`/`vocab`, run beam 10 on clean test, all 28 noisy suites and the 4 independent suites, and save per-item results to `results/items/<name>-s<seed>.npz` (arrays: top-1 correct flag, edit distance to closest reference, reference length, per suite). Do not commit these files (add `results/items/` to `.gitignore`).
- `scripts/aggregate.py`: reads `results/c3`, `results/c2`, `results/items` and writes `results/summary/`:
  - `c3_clean.csv`: per (arch,size): mean and sd over seeds of dev/test CER, top-1, top-5, MRR, n_params, wall time.
  - `c1_degradation.csv`: per (arch,size,op,severity): mean and sd CER and top-1 over seeds, absolute and relative degradation versus clean test.
  - `c2.csv`: per (arch,condition): clean test, every noise op at severity 0.3, MIX at 0.1/0.3/0.5, independent sets; and the held-out-operator comparisons (A2-noGEM tested on GEM, A2-noVDROP tested on V-DROP versus A2).
  - `stats.json`: paired bootstrap (10,000 resamples over test items) of CER difference for: best BiLSTM vs best Transformer at each size (clean and MIX 0.3); A2 vs A1; A3 vs CTRL; A4 vs A2; plus Kruskal-Wallis across the six C2 conditions and Dunn post-hoc with Holm correction, using per-seed mean CER. Report effect sizes and p-values; with 5 seeds be honest that power is low.
  - `summary.json`: a short machine-readable digest and the list of the input run files with their git commits.
- Also record the realised-noise table `data/synth/noisy_test/manifest.json` contents into `results/summary/noise_manifest.json`.
Write `docs/results.md`: tables rendered as Markdown from the CSVs, 10 to 20 lines of plain interpretation per research question (RQ1 to RQ4 in `docs/experiment-plan.md`), what is surprising, what is null, and every limitation. Do not overclaim; a null result is a result.

## 6. Decisions you may make alone
- Relaunch, resume, reorder or parallelise runs; fix bugs; add tests; write the scripts above.
- Fall back from 5 seeds to 3 for the 8M configurations only if the remaining GPU time exceeds 24 hours; record the deviation in `STATUS.md` and `docs/results.md`.
- Anything inside the locked scope of `DECISIONS.md`.
## Never, without Lebi
- Reboot or shut down Leica, touch GRUB, kernel, drivers, Docker, Swarm, systemd services, or other users' processes (ENDCORE may use this GPU; if `nvidia-smi` shows other users' jobs, share the GPU rather than killing them).
- `sudo` of any kind. Install system packages. Use the network for anything but the Claude API and local git.
- Change the locked scope, models, datasets, splits or the noise test sets (`data/synth/noisy_test`): the paper depends on them. If you believe something is wrong, write it in `STATUS.md` under "Needs Lebi" and carry on with everything else.
- Delete `runs/`, `results/`, or `data/`. Force-push. Write passwords, tokens or the WhatsApp data anywhere.

## 7. Documentation duties (as the project always does)
After each stage finishes: prepend a `STATUS.md` entry (what ran, counts, key numbers, anything odd, wall time). After a real bug fix: prepend `FIXES.md` (symptom, root cause, fix with file:line, verification). Move `HANDOVER.md` "Current" to "Previous versions" before rewriting it at the end. Keep `docs/experiment-plan.md` honest about deviations. Commit after each stage with conventional messages ending with `Co-Authored-By: Claude <noreply@anthropic.com>`; commit only small files (JSON/CSV/Markdown/scripts; never checkpoints, `runs/`, `results/items/`, `data/`).

## 8. Pushing and handing back
There is no stored GitHub credential on this machine. Commit locally. If the environment variable `GH_TOKEN` is set in your shell, push with `git -c http.extraheader="Authorization: Basic $(printf 'x-access-token:%s' "$GH_TOKEN" | base64 -w0)" push origin main` (never write the token to a file or the git config). If it is not set, do not look for one; the laptop session will pull your commits over ssh (`git pull airoot:work/tamil-translit-robustness main`).
The paper is compiled on the laptop (no TeX here). Your handover to it is: `results/summary/`, `docs/results.md`, updated `STATUS.md`/`HANDOVER.md`, plus the list under "Needs Lebi / laptop" below.

## 9. Finish
When all of: c3 30/30, c2 80/80, `results/summary/summary.json` written, `docs/results.md` written, docs updated, everything committed, tests passing: write `HANDOVER.md` v3 (what exists, headline numbers, what the laptop session must do: evaluate the WhatsApp set and human-typed set on the checkpoints in `runs/`, fill the paper's Results section, compile with latexmk, view figures), then `echo done > logs/AUTOPILOT_DONE`. The Stop hook then lets you stop.

## Needs Lebi / laptop (leave for them, do not attempt)
- Verify `wa_verify.tsv` (real-chat words) and decide the human typists; evaluate those sets on the checkpoints; paper figures and compile; revoke the exposed GitHub and Hugging Face tokens and rotate the lab passwords.
