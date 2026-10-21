# STATUS

Newest entry on top.

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
