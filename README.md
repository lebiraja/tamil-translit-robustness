# Tamil transliteration robustness (IA3 Deep Learning, topic #34)

How robust is character-level neural transliteration of romanized Tamil ("Tanglish") to informal typing? A paired noise benchmark, a human-typed test set, an augmentation study and a matched-budget BiLSTM vs Transformer comparison, written up as an IEEE conference paper.

**Status (2026-10-22):** 110 models trained and analysed, final model fine-tuned (`models/v2-ft-transformer-3m.pt`, 12.6 MB), typing demo built (`app/`), IEEE paper draft written (`paper/`, 9 pages). Open: real-typing evaluation (RQ2), co-authors, proofreading.

## Start here
| File | Purpose |
|---|---|
| `PROJECT_INTRO.md` | What the project is, the gap, contributions, research questions |
| `DECISIONS.md` | Locked decisions D1 to D17 and open items |
| `HANDOVER.md` | Where we are and what to do next |
| `STATUS.md` | Dated log of work, newest first |
| `FIXES.md` | Documentation and bug fixes |
| `CHECKLIST.md` | Phased task list |
| `CLAUDE.md` | Rules for working in this repo |
| `docs/` | Session log, experiment plan, human-typing protocol, paper outline, architecture, docker, infrastructure, glossary, dataset docs |
| `paper/` | IEEE paper (XeLaTeX), figures and tables generated from `results/` |
| `app/`, `models/` | Typing demo and the final model (weights gitignored) |
| `results/`, `logs_archive/` | Run JSONs, summaries, statistics; Leica logs |
| `research/` | 32 papers with notes, knowledge base, novelty candidates, `refs.bib`, Dakshina report |

## Data
All datasets live in `data/` (gitignored, about 965 MB). Index and usage rules: `docs/datasets/README.md`. Dakshina is still to be fetched (Tamil files only, about 23 MB).

## Compute
Development on the laptop (RTX 4050, 6 GB); long runs on the lab server Leica (`ssh airoot`, RTX 5070, 12 GB). See `docs/infrastructure.md` before touching Leica (its GPU works only on kernel 6.17.0-22).

## Privacy note
`Projects_with_Team_Members.xlsx` contains other students' names and register numbers. This repo is private; remove the file before any public release.
