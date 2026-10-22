# docs/ index

| File | What it is |
|---|---|
| `session-log-2026-10-18.md` | Complete chronological record of the first session: what was done, by whom, results, mistakes and corrections, commits |
| `infrastructure.md` | Laptop and Leica specs, access, network, constraints (kernel/GPU fragility, Blackwell PyTorch), workflow, open items |
| `experiment-plan.md` | Research questions, data splits, noise model, models, augmentation, metrics, statistics, run matrix, risks |
| `human-typing-protocol.md` | Draft protocol for the human-typed informal test set (needs Lebi's confirmation) |
| `paper-outline.md` | IEEE paper outline, figures and tables plan, claim-to-evidence map, writing rules |
| `architecture.md` | Planned code layout and data flow (no code yet) |
| `docker.md` | Planned container and environment setup, Leica specifics |
| `glossary.md` | Plain-language terms |
| `datasets/README.md` | Dataset index, usage rules, do-not-train list, folder inventory |
| `datasets/pairs-and-text-datasets.md` | Detailed pair and text dataset documentation, leakage summary |
| `datasets/informal-tanglish-datasets.md` | Detailed real informal Tanglish dataset documentation and measurements |

Research material lives in `research/` (32 papers, 32 notes, `KNOWLEDGE_BASE.md`, `NOVELTY_CANDIDATES.md`, `refs.bib`, `DATASET.md`, `DATASET_QUESTIONS.md`). Project-level logs live in the repo root (`STATUS.md`, `FIXES.md`, `HANDOVER.md`, `DECISIONS.md`, `CHECKLIST.md`, `PROJECT_INTRO.md`).

## Added 2026-10-22
- `results.md`, `results_text.md`: results report (tables generated, prose hand-written).
- `reproducibility.md`: how to regenerate every number, table and figure.
- `paper-claims-map.md`: every paper claim -> evidence file.
- `model-card.md`: the deployed model v2 (and v1 fallback).
- `demo.md`: the typing demo. `dashboard.md`: live monitor on Leica :8383. `autopilot/`: unattended-run runbook pieces. `leica-log-commands.txt`: log commands.
