# STATUS

Newest entry on top.

## 2026-10-21 · C3 started early (5 of 6 configs tuned)
- Tuning 103/120: BiLSTM 1M/3M/8M and Transformer 1M/3M done; Transformer-8M still tuning (alone, queued after 3M). Started C3 now in two workers (seeds 0-2, 3-4) instead of waiting; GPU 10.9/12 GB, so no third job.
- Guard added to `scripts/run_matrix.py`: c3/c2 runs are SKIPPED (not run with default hyperparameters) when their tuned config does not exist yet. Without it Transformer-8M would have silently trained untuned.
- `scripts_pipeline.sh` rewritten: waits for 6 configs and for the early C3 workers, then finishes C3 (Transformer-8M) and runs C2 in two workers (seeds 0-2, 3-4). Reason: avoids two processes training the same run.
- Needs Lebi: nothing.

## 2026-10-21 · Autopilot on Leica: tuning running, analysis tooling ready
- Autopilot session started on Leica (healthcheck OK: kernel 6.17.0-22-generic, RTX 5070). Tuning at 36/120 trials; BiLSTM trials take 1.5-5 min, Transformer-3m 6-11 min. Best dev CER so far: BiLSTM-3m 8.35, BiLSTM-1m 8.39, Transformer-3m 8.72 (dev, beam 10, seed 100).
- Wrote `src/translit/stats.py` (corpus CER, paired bootstrap, Kruskal-Wallis + eta2, Dunn + Holm, Cohen's d) with hand-computed tests (`tests/test_stats.py`; suite now 28 passed), `scripts/evaluate_ckpt.py` (per-item npz; reproduces the gate JSON exactly: clean CER 9.239, MIX.0.3 25.167, AK-all 12.311; about 4.3 min per checkpoint) and `scripts/aggregate.py` (smoke-tested on synthetic inputs in a scratch dir via `AGG_ROOT`).
- Scheduling: `tune.py` has no lock, so two workers on the same combo would collide. Detached the chain wrapper of worker 3 (our own `sh` process); `transformer 3m` keeps running and `transformer 8m` will be launched by hand as its own worker once GPU memory allows (Transformer-3m alone uses 6 GB).
- Git identity on Leica set repo-locally to match earlier commits.
- Needs Lebi: nothing yet.

## 2026-10-21 (afternoon) · Live dashboard on Leica port 8383
- Built and deployed `scripts/dashboard/` (stdlib python server + offline SVG page): live loss/dev-CER curves with a verdict per job, tuning view for all 6 searches, results tables, past-run comparison, live log tail, GPU/CPU/RAM/disk/kernel header. Details: `docs/dashboard.md`. Verified in a browser from the laptop (all tabs render; JSON NaN bug and axis clipping fixed). It is already showing real overfitting in the BiLSTM gate run (train loss to ~0 while dev CER rises).
- Merging Leica's local commits with ours conflicted once in STATUS.md (both prepended); resolved by keeping both entries. Leica session is progressing on its own (tuning 37/120, analysis tooling written and tested).

## 2026-10-21 (afternoon) · Autopilot set up for the Leica Claude session
- Found Lebi's Claude on Leica (pid 19348, interactive, `--dangerously-skip-permissions`, cwd = project). It is not reachable by cross-session messaging from the laptop (not listed as a peer), so it is driven by files instead: `AUTOPILOT.md` (runbook: stages, commands, analysis scripts to write, what it may and may not do, docs duties, finish condition), `scripts/autopilot_status.py` (stage and next action), `scripts/autopilot_hook.py` (Stop hook: waits without tokens until results change, then re-prompts; stops at `logs/AUTOPILOT_DONE`; escape hatch after 3 identical idle wake-ups -> `logs/AUTOPILOT_STUCK`), `docs/autopilot/settings.template.json` (installed on Leica as `.claude/settings.json`).
- Hook tested on Leica with a 5 s wait: returns the correct block message. Tuning at 26/120 trials when installed; the c3 -> c2 watcher (`scripts_pipeline.sh`) is running.
- The Leica session must be told once to read `AUTOPILOT.md` and load the hook (`/hooks` or restart with `--continue`). Pushes from Leica need `GH_TOKEN` exported in its shell; otherwise the laptop pulls over ssh.

## 2026-10-21 (later) · Datasets generated, Leica set up, reproduction gate PASSED, tuning running
- Datasets generated: 28 paired noisy test sets (6,833 inputs each), independent Aksharantar sets (2,607 / 991 / 706), 60,000-word A3 pool, A3 sampled pairs 123,488 (+60,000 greedy control), WhatsApp real-chat set (370 + 43) built from Sonnet-made labels, `wa_verify.tsv` handed to Lebi to check. Datasheet: `docs/datasets/final-dataset.md`.
- Leica ready: repo cloned (token via command header only, remote URL clean), uv + venv (no sudo), torch 2.11.0+cu128 works on RTX 5070, kernel 6.17.0-22 unchanged, 20 tests pass.
- **Reproduction gate (seed 0, 3M params):** BiLSTM dev CER 8.95 / top-1 62.8 (Roark 2020: 8.4 / 65.3, gap +0.55 CER); Transformer dev CER 9.38 (Roark 9.4). Within the D13 limit of 1 CER point. Top-1 is 2.5 points under Roark for the LSTM: likely an evaluation-definition difference; documented, not hidden. Test (clean) CER: LSTM 9.24, Transformer 9.86. Results: `results/gate/*.json`.
- Noisy sanity (LSTM, severity 0.3): V-DROP CER 24.1, KEY 22.0, DIGRAPH 12.5, V-LEN 10.3, GEM 10.3, REPEAT 10.7, MIX 25.2 vs clean 9.24. Independent: AK-Freq 5.95, AK-NEF 25.0, AK-NEI 27.9.
- Haiku pilot: 34.4% exact match to attested human romanizations (900 variants), 77.2% within one edit: not used as training data.
- Found and fixed: temperature-1 back-transliteration produced degenerate outputs; added a closeness-to-greedy filter (17,828 of 141,316 samples dropped). Transformer "1M" budget lands at 0.80M (width step 32); acceptable, tighten if time.
- Running now on Leica: random-search tuning, 20 trials x 6 (arch, size) combos, 3 workers, selection on dev only. Next: C3 (5 seeds), C2 (A0..A4, CTRL, held-out), WA/human evaluation, statistics, paper skeleton.

## 2026-10-21 · GO given: Phase 1 started, code written, Leica connected
- Lebi said go ("make everything ready to train and test", synthesise the dataset, train on Leica). D14 is satisfied; Lebi also authorised using Leica and the GitHub push/pull flow (credentials were given in chat and are used only via commands, never stored).
- Fetched Dakshina Tamil to `data/dakshina-ta/` (byte ranges); counts match docs (68,218 / 6,827 / 6,864 pairs); `SHA256SUMS` saved.
- Wrote and pushed (`655089c`): `src/translit/` (noise operators V-DROP, V-LEN, GEM, DIGRAPH, KEY, REPEAT, MIX, RANDOM; loaders and vocab; metrics; BiLSTM+attention and pre-LN Transformer with a parameter-budget helper; batched beam, greedy and sampling decoders; augmentation policies A0/A1/A2; training loop with early stopping and results JSON), `scripts/` (`prepare_data.py`, `train.py`, `run_matrix.py`, `synthesize_a3.py`, `make_human_prompts.py`, `setup_env.sh`), `configs/`, `tests/`, `requirements.txt`.
- Noise and metric tests pass (17). Loader, model, training and decode code has NOT been run yet: PyTorch (cu128, ~2.5 GB) was still downloading on the laptop (first attempt hit a uv lock and a download timeout).
- Leica checked: kernel 6.17.0-22-generic, RTX 5070 idle, 237 GB free, Python 3.12.3 with venv, no pip/uv. Nothing installed there yet.
- Not done yet: synthetic noisy test sets, A3 pool and synthesis, reproduction gate, Leica environment, typing sheets generated.

## 2026-10-18 · Documentation pass (everything written up in detail)
- **Done:** `docs/session-log-2026-10-18.md` (full chronological record incl. mistakes), `docs/infrastructure.md`, `docs/experiment-plan.md`, `docs/human-typing-protocol.md`, `docs/paper-outline.md`, `docs/architecture.md`, `docs/docker.md`, `docs/glossary.md`, `docs/README.md`, `docs/datasets/README.md`; rewrote `PROJECT_INTRO.md`, `CHECKLIST.md`, `DECISIONS.md` (D1-D17 plus open items), `HANDOVER.md` (v2), `CLAUDE.md`; added root `README.md`; `FIXES.md` entries F1, F2.
- **Decisions added:** D11 (Dakshina stays baseline), D12 (dataset usage rules), D13 (reproduction gate), D14 (wait for Lebi's go), D15 (never reboot Leica), D16 (repo and privacy), D17 (secrets).
- **Open:** who types the human set; Leica kernel pin; Leica free of other jobs; go signal for Phase 1.
- **Next:** wait for Lebi's go, then Phase 1 setup.

## 2026-10-18 · Repo created and pushed
- **Done:** private GitHub repo `lebiraja/tamil-translit-robustness`, branch `main`; commits `090d4f2`, `ec69268`, `7522579`. `.gitignore` excludes `data/`, venvs, `.env`, checkpoints.
- **Note:** the Excel with other students' names is in the repo; remove before any public release.

## 2026-10-18 · Lab server reviewed (read-only)
- **Done:** read `/home/lebi/workspace/networks/dscs-lab/`. Corrected the GPU split: laptop RTX 4050 6 GB, Leica RTX 5070 12 GB (FIXES F1).
- **Risk:** Leica's GPU works only on kernel 6.17.0-22 and the permanent pin was never applied; do not reboot.

## 2026-10-18 · Datasets found and documented
- **Done:** ~28 datasets downloaded to `data/` (gitignored, ~1 GB). Docs: `docs/datasets/pairs-and-text-datasets.md`, `docs/datasets/informal-tanglish-datasets.md`, plus measurement and overlap scripts.
- **Findings:** Aksharantar Tamil test contains all Dakshina test pairs; the 4,335-row filtered set is our independent test. IndicXlit sentence pairs and the gowtham58 sets are Dakshina copies (never train on them). Aksharantar train has stem overlap with Dakshina test (report as a separate condition). Real informal Tanglish exists (DravidianCodeMix, HopeEDI) but only with labels, no Tamil-script gold, so the human-typed set (D4) stays. Real comments drop vowels 3-5x more than Dakshina.
- **Not obtained:** NEWS En-Ta, Brahmi-Net (502), OSCAR, TAMZHI, Hellsten, Wolf-Sonkin, HASOC/FIRE 2021 (login).
- **Next:** wait for Lebi's go; then environment setup and the human typing set.

## 2026-10-18 · Research phase complete, decisions locked
- **Done:** Topic #34 chosen. 32 papers downloaded and read (`research/papers/`, `research/notes/`), `KNOWLEDGE_BASE.md`, `refs.bib`, `NOVELTY_CANDIDATES.md`, `DATASET.md`, `DATASET_QUESTIONS.md`. Decisions D1-D9 in `DECISIONS.md`. Created `PROJECT_INTRO.md`, `CHECKLIST.md`, `HANDOVER.md`, `FIXES.md`.
- **Finding:** Dakshina is formal romanized Wikipedia Tamil, not chat Tanglish; no paired Tamil robustness benchmark exists. Scope is C1+C2+C3.
- **Blockers:** none; open questions listed in `DECISIONS.md`.
- **Next:** Phase 1 setup (env for RTX 5070, download Tamil data), start human typing in parallel.
