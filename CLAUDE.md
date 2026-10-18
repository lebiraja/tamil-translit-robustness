# CLAUDE.md

IA3 Deep Learning project: robustness of char-level Tanglish/romanized-Tamil to Tamil-script transliteration (Dakshina). Team of 3, B.Tech AI&DS, Karunya. Goal: working code + IEEE-format research paper with proper experiments and citations. Deadline about 2026-11-01.

## Start of session
Read `HANDOVER.md`, top of `STATUS.md`, `DECISIONS.md`, `CHECKLIST.md`. Address the user as Lebi.

## Rules
- Decisions in `DECISIONS.md` are locked. Do not change scope, models, or framing without asking; add a new row when changed.
- Research honesty: cite only papers in `research/refs.bib` that were actually read; never invent numbers. Every figure in the paper must trace to a logged run (config, seed, commit).
- Frame the topic as "informal romanized Tamil"; Dakshina is not chat text.
- Python: type hints, venv or Docker only, pinned versions, never global pip. Dev on the laptop (RTX 4050 6 GB); long runs on the lab server Leica (`ssh airoot`, RTX 5070 12 GB Blackwell sm_120, 15 GB RAM). Lab docs: `/home/lebi/workspace/networks/dscs-lab/`. Leica's GPU works only on kernel 6.17.0-22; never reboot it or touch GRUB/Docker/Swarm without asking Lebi. Run our work in its own Docker container or venv and do not disturb other projects there (ENDCORE may also use it). Check the PyTorch build supports sm_120.
- Reproducibility: fixed seeds, 5 seeds per final config, configs in files, results as JSON/CSV in `results/`.
- Tests for noise operators and metrics (pytest).
- Paper: LaTeX, IEEEtran, in `paper/`; use the `research-paper` skill.
- After a feature, fix, decision or blocker: prepend `STATUS.md`. After a real bug fix: prepend `FIXES.md`. Move old HANDOVER "Current" into "Previous versions" before editing.
- Commits: conventional (`feat:` `fix:` `docs:`). Not a git repo yet; ask before `git init`.

## Layout
- `research/` papers, notes, knowledge base, refs.bib, novelty, dataset report
- `DECISIONS.md` `PROJECT_INTRO.md` `CHECKLIST.md` `STATUS.md` `FIXES.md` `HANDOVER.md`
- Planned: `src/`, `data/` (gitignored), `results/`, `paper/`, `tests/`

## Startup accountability
Per global CLAUDE.md: Lebi's startup (`/home/lebi/start-it-up`, deadline 2026-12-31) still waits. One nudge per session at most.
