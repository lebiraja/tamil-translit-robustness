# HANDOVER

> Version: v1 · Last changed: 2026-10-18

## Current (v1)

### Where we are
Planning complete, no code yet. IA3 deep learning project, topic #34, team of 3 (Lebi + 2). Deadline about 2026-11-01 (confirm). Research and decisions are done; Phase 1 setup is next.

### Read first
`DECISIONS.md` (locked choices) → `PROJECT_INTRO.md` → `CHECKLIST.md` → `research/KNOWLEDGE_BASE.md`, `research/NOVELTY_CANDIDATES.md`, `research/DATASET.md`.

### Next session, do this first
1. Ask Lebi the open items in `DECISIONS.md` (due date, teammates, lab system).
2. Lebi said: do not start until told. When told, build the Docker/venv for PyTorch with a CUDA 12.8+ build for sm_120, first on the laptop (4050) for dev, then on Leica (`ssh airoot`, 5070) after checking `nvidia-smi` and `uname -r` (must be 6.17.0-22). See `/home/lebi/workspace/networks/dscs-lab/`.
3. Fetch only the Tamil files from Dakshina via the byte ranges in `DATASET.md`; verify counts (25,000 / 2,500 / 2,500 words).
4. Start human typing set collection in parallel.

### Gotchas
- Dakshina is not chat text; word it as "informal romanized Tamil" (D5).
- Aksharantar's quoted "Roark 65.7" is a dev number in a test table; do not copy it as a test baseline.
- Dakshina has ~0.35% bad lexicon pairs, 15 sentences in both dev and test, and a misdocumented `split.tsv`.
- Cite only papers in `research/refs.bib`; every number in the paper must trace to a logged run.
- The Word2Vec CBOW/Skip-gram assignment is separate from this project.
- Use they/them or Lebi for Lebi.

---
## Previous versions
_None._
