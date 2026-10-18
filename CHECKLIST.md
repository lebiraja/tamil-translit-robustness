# CHECKLIST

Soft internal target about 2026-11-01 (Lebi: deadline does not matter, D8). Phases are ordered by dependency. Nothing in Phase 1 onward starts until Lebi says go (D14).

## Phase 0: planning and research (DONE 2026-10-18)
- [x] Read the Excel (35 topics, 8 claimed) and Lebi's GitHub projects
- [x] Topic #34 chosen and locked (D1)
- [x] 32 papers downloaded and read, 32 notes, `KNOWLEDGE_BASE.md`, `refs.bib` (32 entries)
- [x] `NOVELTY_CANDIDATES.md` (8 candidates), scope locked to C1+C2+C3 (D2)
- [x] Dakshina verified (`research/DATASET.md`), quirks and baselines recorded
- [x] About 28 further datasets downloaded to `data/` (965 MB), two dataset docs, scripts, leakage audit
- [x] Aksharantar overlap resolved; independent test file `tam_test.no_dakshina.tsv` (4,335 rows)
- [x] Lab server docs read (`/home/lebi/workspace/networks/dscs-lab/`), `docs/infrastructure.md`
- [x] Private GitHub repo created and pushed (`lebiraja/tamil-translit-robustness`)
- [x] Documentation set written (this pass): session log, experiment plan, typing protocol, paper outline, architecture, docker, glossary, dataset index

## Phase 1: setup (after Lebi says go)
- [ ] Answer the open items in `DECISIONS.md` (who types; Leica kernel pin; Leica free)
- [ ] Laptop venv or Docker, CUDA 12.8+ PyTorch, pinned `requirements.txt`
- [ ] GPU smoke test on the laptop (RTX 4050), later on Leica (RTX 5070, `uname -r` = 6.17.0-22-generic)
- [ ] Fetch Dakshina Tamil by byte range into `data/dakshina-ta/`; verify 25,000 / 2,500 / 2,500 words and 68,218 / 6,827 / 6,864 pairs; record sha256
- [ ] Data cleaning rule for the roughly 0.35% suspect pairs, logged; test set not silently cleaned
- [ ] Repo skeleton: `src/translit/`, `configs/`, `scripts/`, `results/`, `tests/`, `paper/`
- [ ] Verify the NVIDIA container toolkit on Leica (or choose a venv there)

## Phase 2: human-typed set (parallel with Phase 3)
- [ ] Confirm typists and design (`docs/human-typing-protocol.md`)
- [ ] Sample about 1,500 Dakshina test words with a recorded seed (stratified by length)
- [ ] Prepare the prompt sheet / form (Tamil script only, no autocorrect)
- [ ] Collect; store `data/human-typed/typist_<id>.tsv` plus `manifest.json`
- [ ] Quality checks (duplicates, pasted entries, 5% spot check), per-typist pattern rates
- [ ] Consent noted; datasheet `docs/datasets/human-typed-set.md`

## Phase 3: code
- [ ] Loaders (Dakshina, Aksharantar filtered, human set), NFC and lowercase handling, vocab from train only, with tests
- [ ] Metrics: CER, top-k, MRR, multi-reference handling, with hand-computed tests
- [ ] Noise operators V-DROP, V-LEN, GEM, DIGRAPH (symmetric), KEY, REPEAT, MIX with determinism, pairing and never-empty tests
- [ ] BiLSTM+attention model; pre-LN Transformer; parameter-budget helper (1M / 3M / 8M)
- [ ] Training loop (seeds, early stopping on dev, optional bf16), beam search, results JSON writer
- [ ] CPU end-to-end smoke test (tiny model, 100 pairs)

## Phase 4: experiments (mostly on Leica)
- [ ] **Reproduction gate (D13):** match Roark/Kirov dev CER within about 1 point; document the evaluation definition
- [ ] Hyperparameter search, equal budget per architecture and size
- [ ] C3 final models, 5 seeds each; statistics
- [ ] C1 paired noisy test sets (4 severities x operators), degradation curves
- [ ] Human-set evaluation; synthetic-vs-human correlation (RQ2)
- [ ] Independent Aksharantar evaluation (AK-Freq, AK-NEI, AK-NEF separately)
- [ ] C2 augmentation matrix (A0 to A4 + control), held-out noise types
- [ ] Hand-check about 300 real-comment tokens to validate noise rates
- [ ] (Optional) C4 reranking; (optional) IndicXlit reference run
- [ ] Error analysis (confusions under V-DROP and GEM, oracle top-k ceilings)

## Phase 5: paper
- [ ] IEEEtran skeleton in `paper/`, `refs.bib` wired in, clean compile
- [ ] Figures and tables generated from `results/` (see `docs/paper-outline.md`)
- [ ] Related work, data, method, experiments, analysis, limitations and ethics, conclusion
- [ ] Every number traced to a logged run; published numbers cited with split and source
- [ ] Proofread; final PDF

## Phase 6: submit and housekeeping
- [ ] Final PDF, code and anything staff requires (confirm format with staff when convenient)
- [ ] Word2Vec CBOW/Skip-gram assignment (separate, posted 2026-10-16)
- [ ] Remove the Excel (other students' names) from the repo if it is ever made public
- [ ] Revoke the Hugging Face token pasted in chat; rotate the two lab-session passwords
- [ ] Update STATUS, HANDOVER, FIXES and docs for any change
