# HANDOVER

> Version: v2 · Last changed: 2026-10-18

## Current (v2) · addendum 2026-10-21
GO was given. Code exists in `src/translit/` and `scripts/` (commit `655089c`); noise and metric tests pass; model/training code is unrun. Next: finish torch install, run `pytest`, `python scripts/prepare_data.py all`, reverse model -> `synthesize_a3.py`, reproduction gate (`run_matrix.py gate`), then Leica (clone via token-in-command, never stored). See STATUS top entry.


### Where we are
Planning, research and dataset survey are complete and fully documented. No project code exists, nothing has been trained, and the environment is not set up. Lebi said "don't start now, I will let you know". Topic #34 (informal romanized Tamil transliteration, Dakshina) is locked; scope C1 + C2 + C3; paper in IEEE format. The repo is private on GitHub (`lebiraja/tamil-translit-robustness`, branch `main`).

### Read first (in this order)
1. `DECISIONS.md` (locked choices D1 to D17 and open items)
2. `PROJECT_INTRO.md` (what and why)
3. `docs/session-log-2026-10-18.md` (everything done so far, including mistakes)
4. `docs/experiment-plan.md` (what to run), `docs/human-typing-protocol.md`, `docs/infrastructure.md`
5. `docs/datasets/README.md` then the two dataset docs and `research/DATASET.md`
6. `research/KNOWLEDGE_BASE.md` and `research/NOVELTY_CANDIDATES.md`
7. `CHECKLIST.md` for the phased plan

### What exists
- 32 papers read (`research/papers/`, `research/notes/`), `refs.bib` with 32 entries.
- About 28 datasets in `data/` (gitignored, 965 MB). Dakshina itself is NOT yet downloaded (fetch the Tamil files only, about 23 MB, per `research/DATASET.md` section 2).
- Docs: experiment plan, human-typing protocol, paper outline, architecture (planned), docker (planned), infrastructure, glossary, dataset index.

### Next session, do this first (after Lebi says go)
1. Ask Lebi the open items in `DECISIONS.md` (who types the human set; kernel pin on Leica; Leica free of other jobs).
2. Laptop: create a venv or Docker image with a CUDA 12.8+ PyTorch build, pin `requirements.txt`, run a GPU smoke test (laptop RTX 4050).
3. Fetch the Dakshina Tamil files by byte range into `data/dakshina-ta/`; verify 25,000 / 2,500 / 2,500 words and 68,218 / 6,827 / 6,864 pairs.
4. Prepare the typing prompt sheet and start collecting the human-typed set in parallel.
5. Implement loaders, metrics and noise operators with pytest; then the BiLSTM+attention baseline and the reproduction gate (D13).
6. Only after the gate passes: C3 sizes and tuning, C1 noisy sets, C2 augmentation, on Leica.
7. Draft the IEEE LaTeX skeleton in `paper/` with `refs.bib`.

### Gotchas
- Dakshina is not chat text; say "informal romanized Tamil" (D5).
- Aksharantar's "Roark 65.7" is a dev number placed in a test table; do not use it as a test baseline.
- Dakshina has about 0.35% bad lexicon pairs, 15 sentences in both dev and test, and a misdocumented `split.tsv` (7 columns).
- Never train on IndicXlit sentence pairs, `gowtham58` sets, Mendeley or sanujen (D12). Use only `tam_test.no_dakshina.tsv` as the independent Aksharantar set.
- Aksharantar train breaks Dakshina's lemma-disjointness (97.1% stem-prefix overlap with Dakshina test words); separate condition only.
- IndicXlit's word dictionary covers 98.7% of Dakshina test words in its top 200k, so any lexicon gain on Dakshina is optimistic.
- Leica: do not reboot; GPU works only on kernel 6.17.0-22; PyTorch needs CUDA 12.8+ (D15, `docs/infrastructure.md`).
- The laptop GPU is the RTX 4050 6 GB; the 5070 is in Leica (an early note had this wrong).
- Home upload is slow (about 36 KB/s): commit small results only, never checkpoints.
- Cite only papers in `refs.bib`; every number in the paper must trace to a logged run.
- Agent chatter: idle notifications from helper agents are noise; do not relay them unless actionable.
- The Hugging Face token Lebi pasted in chat was never used; it is in no file; Lebi should revoke it. Two passwords from the lab session are also unrotated.
- The Word2Vec CBOW/Skip-gram assignment (posted Oct 16) is separate from this project and still pending.
- Use they/them or Lebi for Lebi. Address Lebi by name in chat.

### Commits so far
`090d4f2` planning and literature, `ec69268` dataset survey, `7522579` GPU fix, plus the documentation expansion commit (see `git log`).

---
## Previous versions
### v1, 2026-10-18 (earlier the same day)
Planning complete, no code yet. IA3 deep learning project, topic #34, team of 3 (Lebi + 2), deadline about 2026-11-01 (to confirm). Research and decisions done; Phase 1 setup next. Next steps then: ask Lebi the open items, build the environment for RTX 5070 (sm_120), fetch Tamil files from Dakshina, start the human typing set. Gotchas then: frame as informal romanized Tamil; Aksharantar dev/test mix-up; Dakshina quirks; cite only refs.bib; the Word2Vec assignment is separate.
