# CLAUDE.md

IA3 Deep Learning project (staff topic #34): robustness of character-level romanized/Tanglish Tamil to Tamil-script transliteration, on Google Dakshina plus our own paired benchmark. Team of 3, B.Tech AI&DS, Karunya. Goal: working code plus an IEEE-format research paper with proper experiments, statistics and citations. Soft internal target about 2026-11-01 (Lebi said the deadline does not matter).

## Start of session
Read `HANDOVER.md`, the top of `STATUS.md`, `DECISIONS.md`, `CHECKLIST.md`. Address the user as Lebi. Use they/them if a pronoun is needed.

## Rules
- Decisions in `DECISIONS.md` are locked. Do not change scope, models or framing without asking; supersede with a new row.
- **Do not start setup, code or training until Lebi says go** (D14). Dataset downloads into `data/` were requested and are done.
- Research honesty: cite only papers in `research/refs.bib` that were actually read; never invent numbers; mark inference as inference. Every number in the paper must trace to a logged run (config, seed, commit, data checksums).
- Frame the topic as "informal romanized Tamil"; Dakshina is formal, not chat text (D5).
- Data rules (D12): never train on IndicXlit sentence pairs, `gowtham58` sets, Mendeley, sanujen; independent Aksharantar test = `data/aksharantar-tamil/tam_test.no_dakshina.tsv` only; Aksharantar train is a separate condition. See `docs/datasets/README.md`.
- Reproduction gate (D13): match published Dakshina Tamil baselines before any novelty run.
- Python: type hints, Pydantic configs, venv or Docker only, pinned versions, never global pip. Tests with pytest for noise operators, metrics and loaders.
- Compute: laptop RTX 4050 6 GB for dev; lab server Leica (`ssh airoot`, RTX 5070 12 GB Blackwell sm_120, 15 GB RAM) for long runs. Lab docs: `/home/lebi/workspace/networks/dscs-lab/`; our notes: `docs/infrastructure.md`. Leica's GPU works only on kernel 6.17.0-22: never reboot it or touch GRUB, Docker or Swarm without asking Lebi; check `uname -r` and `nvidia-smi` before jobs; PyTorch needs CUDA 12.8+. Do not disturb other projects on Leica (ENDCORE may use it).
- Keep pushed artifacts small (slow home upload): results as JSON/CSV, never checkpoints.
- Paper: LaTeX, IEEEtran, in `paper/`; use the `research-paper` skill; compile cleanly before committing paper changes.
- No secrets in files. Hugging Face tokens or passwords given in chat are used via environment variables only and never stored.
- Docs sync: keep `docs/` in step with the code (architecture, docker, experiment plan). After a feature, fix, decision or blocker, prepend `STATUS.md`. After a real bug fix, prepend `FIXES.md`. Before editing HANDOVER, move "Current" into "Previous versions".
- Commits: conventional (`feat:` `fix:` `docs:` `refactor:` `chore:`). Repo is private on GitHub: `lebiraja/tamil-translit-robustness`.
- Helper agents: relay only actionable news to Lebi, not idle or duplicate notifications.

## Layout
- Root: `DECISIONS.md` `PROJECT_INTRO.md` `CHECKLIST.md` `STATUS.md` `FIXES.md` `HANDOVER.md` `README.md`
- `docs/`: session log, infrastructure, experiment plan, human-typing protocol, paper outline, architecture, docker, glossary, `datasets/` (index, two dataset docs, scripts)
- `research/`: 32 papers, 32 notes, `KNOWLEDGE_BASE.md`, `NOVELTY_CANDIDATES.md`, `refs.bib`, `DATASET.md`, `DATASET_QUESTIONS.md`
- `data/` (gitignored): downloaded datasets (about 965 MB)
- Planned: `src/translit/`, `configs/`, `scripts/`, `results/`, `tests/`, `paper/`

## Startup accountability
Per global CLAUDE.md: Lebi's startup (`/home/lebi/start-it-up`, deadline 2026-12-31) still waits (open Q15, Q16, Q18). One nudge per session at most.
