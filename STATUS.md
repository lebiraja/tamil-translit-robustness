# STATUS

Newest entry on top.

## 2026-10-27 · Open-sourced under Apache-2.0
- **Done:** `LICENSE` (Apache-2.0) and README license section; GitHub `lebiraja/tamil-translit-robustness` now public. `Projects_with_Team_Members.xlsx` and `research/papers/` (32 third-party PDFs) removed from all history with git-filter-repo, then one authorised force-push of main (commit hashes changed); both stay on disk, gitignored. HF `lebiraja/tamil-tanglish-translit-v2` is public with LICENSE and `license: apache-2.0` in the card. The 113-checkpoint HF repo stays private.
- **Caveat:** model card credits Dakshina (CC BY-SA 4.0) and Aksharantar (CC BY 4.0); share-alike on trained weights is unsettled (D18).
- **Needs Lebi:** revoke the HF token pasted in chat today (and the earlier GitHub/HF ones) and rotate the lab passwords.

## 2026-10-23 · Paper v3 written (staff structure)
- **Done:** `paper/v3/main.tex` (7 pages, builds clean, no undefined citations): six sections as the staff asked (Abstract of 145 words, Introduction, Related Work grouped rule-based/neural/LLM with a gap table, Proposed Methodology, Results and Discussion with comparison tables and figure last, Conclusion). New title "Robustness of Character-Level Transliteration to Informal Typing in Romanized Tamil". Two gaps claimed: G1 paired benchmark, G2 remedies and transfer. PDF: `paper/releases/paper-v3.pdf`. Plan: `docs/paper-v3-plan.md`. Audio of the staff conversation transcribed from `ignore-it/` (not saved).
- **Corrected from v2:** reproduction paragraph compared our test top-1 with Roark's dev top-1; dev top-1 now 65.1 (BiLSTM 3M) vs 65.3 and 65.8 (Transformer 3M) vs 65.7. Azam 2025 sentence now notes fine-tuned GPT-4o reaches 37%. Mined-pair filter now states the authors' threshold (-0.35) and ours (-0.10).
- **Open:** venue and page limit; run the staff's plagiarism check; real chat is still preliminary (`data/private/wa_verify.tsv` unverified).

## 2026-10-22 · Paper author block and layout (v3 layout tried and reverted)
- Author block rebuilt in IEEE style (name with division and college under each, two authors per row), kept. A v3 layout (abstract alone in the left column, Introduction at the top of the right column) was tried and dropped at Lebi's request: `main.tex` is back to the v2 layout (text identical to `paper-v2.pdf`), the v3 PDF and the `paper-v3` tag were removed. Releases: `paper-v1.pdf`, `paper-v2.pdf` (final); tags `paper-v1.1`, `paper-v2.1`.

## 2026-10-22 · Co-authors added to paper v1 and v2
- Authors: Lebi Raja, KRM Lohith, Allen John Isac, KP Shohil (same division and college). Both PDFs rebuilt clean (9 pages); tags `paper-v1.1` and `paper-v2.1`.

## 2026-10-22 · Paper v1 and v2 released
- Affiliation corrected to "Division of Data Science and Cybersecurity, Karunya Institute of Technology and Sciences, India". `paper/releases/paper-v2.pdf` is the final (with the deployment model); `paper/releases/paper-v1.pdf` is the earlier complete draft without it. Git tags `paper-v1` (fef4072) and `paper-v2`. Both build clean (9 pages).

## 2026-10-22 · Paper updated with the v2 model, final draft built
- `paper/` now includes the deployment-model section (v2 table and a v1-vs-v2 figure), the privacy statement for the real-chat words, consistency fixes (introduction, noise-rate source), a cleaned reference list and Times text via newtx under XeLaTeX. 9 pages, 6 figures, 6 tables, exit 0, no undefined references. PDF: `paper/main.pdf`.
- Still open before submission: co-authors, venue page limit, verified real-chat labels and RQ2 results, venue details for a few arXiv-only references.

## 2026-10-22 · v2 uploaded to its own private Hugging Face repo
- `lebiraja/tamil-tanglish-translit-v2` (private): `model.pt` (12.6 MB, the single fine-tuned file), `config.json` (architecture, vocab, metrics), model card, `SHA256SUMS`, `example.py` and the five small source files needed to run it (`translit/`); tested standalone from a clean folder before upload. Separate from the earlier private repo `lebiraja/tamil-translit-robustness-models` (all 113 experiment checkpoints).
- The token Lebi pasted was used only as an environment variable for the upload; it is in no file. Token type is fine-grained; rotate it with the others.

## 2026-10-22 (evening) · Final model v2, typing demo with English filter, IEEE paper draft
- **Final model:** full fine-tune of the best A4 Transformer on 2.41M pairs per epoch (D19), 5 epochs, 20 min on Leica (13.7k pairs/s). All 3,153,844 weights trainable and changed (mean abs change 0.024); single 12.6 MB file `models/v2-ft-transformer-3m.pt`. Gates: dev CER 8.56 vs 8.47 (+0.10, pass), AK-all 10.76 vs 10.95 (pass, small), MIX 0.3 17.77 vs 21.80 (pass, but all six operators were trained so this is not held-out), KEY 15.40 vs 23.04. Preliminary real chat (370 words, unverified model labels): CER 24.9 vs 25.4, top-1 39.7 vs 40.5, top-5 71.1 vs 68.6: tied. Observation: colloquial forms (poren, enna) are the failures; real chat sits near CER 25, like heavy synthetic noise. Details: `results/final/v2-ft-s0.json`, `docs/model-card.md`.
- **Demo:** `app/` (FastAPI + one page) shows top-5 per word, click to swap, copy; English words kept as typed (D21); `docs/demo.md`. Runs on the laptop CPU at http://localhost:8000.
- **Paper draft:** `paper/` IEEEtran, XeLaTeX, 9 pages, builds clean (exit 0, no undefined references, no overfull boxes). Figures (5) and tables (6) generated from `results/` by `scripts/make_figures.py` / `scripts/make_tables.py`; claim-to-evidence map `docs/paper-claims-map.md`; reproducibility guide `docs/reproducibility.md`; model card.
- Dashboard (Leica :8383) follows the fine-tune log (Logs tab, Runs tab block "final").
- Open: verify `data/private/wa_verify.tsv` (real-chat gate and RQ2); who types the human set; co-authors; venue page limit; upload v2 to the private Hugging Face repo (not done); revoke the GitHub and HF tokens and rotate passwords (token files `~/work/git.txt`, `~/work/hug.txt` still on Leica).

## 2026-10-22 · Pushed: code and docs to GitHub, checkpoints to a private Hugging Face repo
- GitHub `lebiraja/tamil-translit-robustness` main updated (code, docs, results JSON/CSV, summary tables). A laptop session had already pushed an older draft of docs/results.md and the summary files; rebased onto it and kept the final versions (post CTRL-s1 retrain).
- Hugging Face: private model repo `lebiraja/tamil-translit-robustness-models`: 113 checkpoints (110 C3/C2 best.pt, 2 gate models, the reverse model), 1.52 GB, plus README model card and MANIFEST.json with sha256 and logged scores. Script: `scripts/push_to_hf.py` (token only from the HF_TOKEN environment variable; pinned `huggingface_hub==0.34.4`).
- Both tokens were pasted in chat; neither is stored in any file or git config. Rotate both. This also supersedes the CLAUDE.md note "never checkpoints" for this one explicit request from Lebi: checkpoints went to Hugging Face only, never to GitHub.

## 2026-10-22 · ALL EXPERIMENTS DONE, analysed, docs/results.md written
- Tuning 120/120, C3 30/30 (5 seeds x 6 models), C2 80/80 (2 archs x 8 conditions x 5 seeds); 110 checkpoints re-scored per item (28 noisy + 4 independent + clean suites, beam 10) and aggregated: `results/summary/` (c3_clean, c1_degradation, c2 CSVs, stats.json with paired bootstrap, Kruskal-Wallis, Dunn-Holm, noise_manifest). `docs/results.md` is generated by `scripts/make_results_md.py` from `docs/results_text.md` (prose) plus the summary files.
- Headline (details and caveats in docs/results.md): vowel drop and keyboard noise hurt most (+12 to +15 CER at 0.3); Tamil-aware noise (A2) and A4 give the best noisy results, A1/A2 cost about 0.8 clean CER, A4 about none; A3 gains over baseline are mostly extra data (CTRL matches on clean); robustness does not transfer to held-out operators (V-DROP); BiLSTM = Transformer at 3M on clean, Transformer degrades less under MIX.
- Incident: supervisor duplicate-worker bug (FIXES F3). One run (c2-transformer-CTRL-s1) failed the checkpoint-vs-log check, was quarantined and retrained cleanly. 32 other overlapped runs kept; disclosed in results.md.
- Tooling added overnight: per-epoch resume (`last.pt`), retry wrapper, supervisor + cron, per-run and per-model locks, parallel evaluators, dashboard Plan tab.
- **Needs Lebi:** (1) decide whether to retrain the 32 overlapped C2 runs (about 5 to 8 h on Leica) or accept the disclosure; (2) human-typed and WhatsApp sets must be evaluated on the laptop (not on Leica) for RQ2; checkpoints are in `runs/` on Leica (about 1.8 GB, never pushed; copy the ones needed); (3) push to GitHub (no token stored; local commits ahead of origin); (4) rotate the GitHub token and the sudo password pasted in chat; (5) the paper (`paper/`, IEEEtran) is not started.
- Local git commits are not pushed.

## 2026-10-22 · Overnight: C3 done, C2 74/80, duplicate-worker incident fixed, parallel evaluation
- Tuning 120/120, C3 30/30 (including Transformer-8M after two GPU out-of-memory retries), C2 74/80 at 10:00. Evaluation had stalled at 31/110; now 2 parallel evaluators with per-model locks (3 once training ends). Details of the supervisor bug and the contamination check: FIXES F3.
- Open question for the paper: 33 C2 runs overlapped with a duplicate process. BiLSTM check matched exactly. Transformer clean rerun (c2-transformer-A0-s0) was still running; `logs/eval_mismatch.txt` lists any stored model that does not reproduce its logged score. Disclose the incident in docs/results.md either way.
- Needs Lebi: nothing. GitHub push still pending (no token stored); rotate the token and sudo password pasted in chat.

## 2026-10-21 · Dashboard: new Plan tab (checklist and live timer)
- Requested by Lebi. `scripts/dashboard/server.py` gets `plan()` (checklist of 38 items derived from files on disk: set-up, tuning per combo, C3 per arch/size, C2 per arch/condition, analysis and wrap-up; start time = first tuning trial; timer stops when `logs/AUTOPILOT_DONE` exists) and the page gets a Plan tab with a ticking elapsed clock, a countdown to the estimated finish and per-item progress bars.
- Time-left estimate is rough (measured run times, assumes no crashes and Claude online for the write-up). First reading: about 24 h left at 13/38 items. Checked by headless Firefox screenshot. Server restarted on port 8383 (`sh scripts/dashboard/run.sh`).
- Needs Lebi: nothing.

## 2026-10-21 · Self-survival layer (resume, retry, supervisor, cron)
- Approved by Lebi. `src/translit/train.py`: atomic per-epoch `last.pt` and resume (new Config field `resume`, default on); `tests/test_resume.py` confirms an interrupted-then-resumed run gives the same loss curve and dev CER as an uninterrupted one. Training maths, data, seeds and metrics are unchanged, so finished tuning and C3 runs stay valid; runs that started before the change finished with the old code and are unaffected.
- `src/translit/retry.py` + wiring in `run_matrix.py` and `tune.py`: 3 tries per run, tracebacks to `logs/failed_runs.txt`, queue keeps going.
- `scripts/supervisor.py` replaces `scripts_pipeline.sh`; user cron (`@reboot`, every 10 min, flock) keeps it alive. Safety: kernel and temperature gate, 3-job cap, no kills, no sudo. Details in AUTOPILOT.md section 8.
- 30 tests pass (resume test run separately, about 1 min on CPU).
- Needs Lebi: nothing. Reminder: GitHub token and sudo password were pasted in chat; rotate them. Local commits are not pushed (no token stored).

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
