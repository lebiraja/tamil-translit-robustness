# CHECKLIST (updated 2026-10-22)

## Phase 0: planning and research: DONE (2026-10-18)
32 papers read, knowledge base, novelty scope (C1+C2+C3), 28 datasets surveyed, leakage audit, documentation set, private repo.

## Phase 1: setup: DONE (2026-10-21)
- [x] venv with CUDA 12.8 PyTorch on Leica (RTX 5070), CPU torch on the laptop
- [x] Dakshina Tamil fetched and verified (68,218 / 6,827 / 6,864 pairs, sha256)
- [x] Repo skeleton, tests (30 pass), dashboard on Leica :8383

## Phase 2: human-typed set: PENDING (Lebi)
- [x] Protocol, sampling and typing-sheet script (`scripts/make_human_prompts.py`)
- [ ] Decide typists, collect about 1,500 words, quality checks, datasheet
- [x] Real-chat word set built from private exports (413 words, model-labelled)
- [ ] Lebi verifies `data/private/wa_verify.tsv`

## Phase 3: code: DONE
- [x] Loaders, metrics, noise operators (all with tests), BiLSTM and Transformer, trainer with resume and retry, beam search, evaluator, statistics, aggregation, fine-tuning

## Phase 4: experiments: DONE except RQ2
- [x] Reproduction gate (BiLSTM dev CER 8.39 to 8.43 vs published 8.4)
- [x] Tuning 120 trials; C3 30 runs; C1 28 noisy suites; independent sets; C2 80 runs; statistics
- [x] Final model: full fine-tune (v2), gates 1 to 3 passed
- [ ] RQ2 and gate 4: real-chat and human sets on the models
- [ ] Optional C4 (LM/lexicon reranking), error analysis of colloquial forms

## Phase 5: paper: DRAFT DONE (9 pages)
- [x] IEEEtran skeleton, all sections written from logged numbers, 5 figures, 6 tables, references cleaned, builds clean
- [x] Claim-to-evidence map, reproducibility guide, model card
- [x] Co-authors added (KRM Lohit, Allen John Isac, KP Shohil), affiliation corrected
- [ ] Page limit, venue entries for arXiv-only references, add RQ2 results, proofread, final PDF

## Phase 6: deliverables and housekeeping
- [x] Typing demo (`app/`), English filter
- [ ] Upload v2 to the private Hugging Face repo (optional)
- [ ] Word2Vec CBOW/Skip-gram assignment (separate course task)
- [ ] Revoke GitHub and HF tokens, rotate lab passwords, delete `~/work/git.txt` and `hug.txt`, remove Leica cron jobs, remove the Excel from the repo before any public release
