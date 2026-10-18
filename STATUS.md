# STATUS

Newest entry on top.

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
