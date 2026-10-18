# CHECKLIST (2-week plan, target 2026-11-01)

## Phase 0: planning (done 2026-10-18)
- [x] Topic locked (#34)
- [x] 32 papers read, knowledge base, refs.bib
- [x] Dataset located and verified
- [x] Novelty and scope decisions confirmed (DECISIONS.md)
- [x] Docs created

## Phase 1: setup (Oct 19-20)
- [ ] Confirm exact due date and deliverable with staff
- [ ] Confirm teammates and roles
- [ ] Docker/venv with PyTorch supporting RTX 5070 (sm_120); pinned requirements
- [ ] Download Tamil files from Dakshina (byte ranges in DATASET.md), verify counts
- [ ] Check Aksharantar overlap if we use it
- [ ] Clean obvious bad pairs (~0.35%) with a logged rule

## Phase 2: human test set (Oct 19-22, parallel)
- [ ] Sample ~1,500 Dakshina test words; split 500 per person
- [ ] Prompt sheet in Tamil script; typing instructions (WhatsApp-style, no correcting)
- [ ] Collect, store with typist id and timestamp
- [ ] Check no personal data

## Phase 3: code (Oct 19-23)
- [ ] Data loader, char vocab, pairs
- [ ] Noise operators (V-DROP, V-LEN, GEM, DIGRAPH, KEY, REPEAT, MIX) with unit tests
- [ ] BiLSTM+attention model
- [ ] Small Transformer (pre-LN)
- [ ] Metrics: top-1, top-5, CER
- [ ] Beam search

## Phase 4: experiments (Oct 23-29)
- [ ] Baselines on clean dev/test, compare to Roark 2020 numbers
- [ ] Hyperparameter search, equal budget per architecture
- [ ] 5 seeds per final config
- [ ] Noise degradation curves
- [ ] Augmentation runs A0-A3 + clean control
- [ ] Human-set evaluation
- [ ] Stats tests

## Phase 5: paper (Oct 27-31)
- [ ] IEEEtran skeleton, refs.bib wired in
- [ ] Figures: degradation curves, architecture, results tables
- [ ] Related work, method, experiments, discussion, limitations
- [ ] Proofread, all numbers traced to logged runs
- [ ] Compile clean PDF

## Phase 6: submit (Nov 1)
- [ ] Final PDF, code, report as staff requires
- [ ] Word2Vec CBOW/Skip-gram assignment (separate, posted Oct 16)
