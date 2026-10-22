# HANDOVER

> Version: v4 · Last changed: 2026-10-22 (evening)

## Current (v4)
### Where we are
Research, experiments, final model, typing demo and a full IEEE paper draft all exist. 110 models were trained and analysed (`docs/results.md`); the final model is a full fine-tune of the best A4 Transformer (`models/v2-ft-transformer-3m.pt`, 12.6 MB, one file; `docs/model-card.md`); the demo runs with `.venv/bin/python app/server.py` (`docs/demo.md`); the paper is in `paper/` (9 pages, builds clean; `paper/README.md`).

### Read first
1. `STATUS.md` top entries, `DECISIONS.md` (D19 to D22 are new), `docs/results.md`, `docs/model-card.md`.
2. `docs/paper-claims-map.md` (every paper number and its source) and `docs/reproducibility.md`.
3. `paper/sections/*.tex` for what the paper claims; `FIXES.md` F3 for the duplicate-worker incident.

### What is left
1. **Lebi:** verify `data/private/wa_verify.tsv` (413 real-chat words); decide who types the human set (`docs/human-typing-protocol.md`, `scripts/make_human_prompts.py`).
2. **Then:** evaluate the verified chat set and the human set on v1/v2 and the 110 checkpoints (checkpoints in `runs/` on Leica or the private Hugging Face repo) to answer RQ2, add a Results subsection and update Limitations and the abstract; re-decide gate 4 (D20).
3. Paper (authors and affiliation done; v1 and v2 PDFs in `paper/releases/`): check the venue page limit, add missing venues to a few arXiv-only references, proofread, optional ablation on how colloquial forms fail.
4. Optional: upload v2 to the private Hugging Face repo; improve colloquial-form accuracy (chat-style training data, self-training on DravidianCodeMix), lexicon/LM reranking (C4).
5. Housekeeping: revoke the GitHub and Hugging Face tokens and rotate the two passwords (pasted in chat); delete `~/work/git.txt` and `~/work/hug.txt` on Leica; remove the supervisor/dashboard cron jobs on Leica when finished; remove the Excel from the repo before any public release.

### Gotchas
- v2's noise numbers are not held-out (trained on all six operators). Real chat sits near CER 25 (preliminary, unverified labels).
- Build the paper with XeLaTeX + biber (Tamil font path `/usr/share/fonts/noto/` is set in `main.tex`; change it on another machine).
- Never reboot Leica (kernel 6.17.0-22 pin); Leica is reachable at 10.42.0.226 via `ssh airoot` when on the same network; dashboard at :8383.
- Leica pushes cannot reach GitHub without a token: pull over ssh (`git fetch ssh://airoot/home/lebiraja/work/tamil-translit-robustness main`).

---
### Previous version: v3 (2026-10-22 morning, written by the Leica session)

All experiments are finished and analysed on Leica; the paper is next. Read `docs/results.md` first (tables, answers to RQ1/3/4, limitations), then `STATUS.md` top entry and `FIXES.md` F3.

### State
- Tuning 120/120, C3 30/30, C2 80/80 done; per-item evaluation and aggregation done (`results/summary/`). Every number in `docs/results.md` comes from `results/summary/*` which come from `results/c3`, `results/c2` run JSONs (config, seed, commit, data checksums inside).
- Not done: RQ2 (human-typed set and private WhatsApp set, evaluate on the laptop; checkpoints are in `runs/<name>-s<seed>/best.pt` on Leica, about 1.8 GB, never push them), the IEEE paper in `paper/`, push to GitHub (local commits are ahead of origin; no token stored).
- Open decision for Lebi: retrain the 32 C2 runs that overlapped with duplicate processes (FIXES F3)? Evidence suggests not needed; one run was already retrained.

### How the unattended layer works (on Leica)
`scripts/supervisor.py` (user cron: @reboot and every 10 min, flock) relaunches tuning, C3, C2, parallel evaluators and aggregation; training saves `last.pt` per epoch and resumes; `run_matrix.py` locks per run; `evaluate_ckpt.py` locks per model and logs mismatches to `logs/eval_mismatch.txt`. Dashboard on port 8383 (Plan tab = checklist and clock), cron-restarted. After `logs/AUTOPILOT_DONE` the supervisor exits. See `AUTOPILOT.md` section 8.

### Gotchas
- Dakshina is formal text; say "informal romanized Tamil" (D5). RQ2 is unanswered until the human/WhatsApp sets are scored.
- Leica: never reboot (kernel 6.17.0-22 only), no sudo, no GRUB/Docker/Swarm.
- `quarantine/` holds the broken checkpoint run's JSON and note (not deleted); `runs/` and `results/items/` are gitignored.
- A GitHub token and a sudo password were pasted in chat on 2026-10-21/22: rotate both. Nothing is stored in files.
- The Word2Vec CBOW/Skip-gram assignment is separate and was pending.
- Use they/them or Lebi for Lebi.

---
## Previous versions
### v2, 2026-10-18 (Current until 2026-10-22) · addendum 2026-10-21
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


### v1, 2026-10-18 (earlier the same day)
Planning complete, no code yet. IA3 deep learning project, topic #34, team of 3 (Lebi + 2), deadline about 2026-11-01 (to confirm). Research and decisions done; Phase 1 setup next. Next steps then: ask Lebi the open items, build the environment for RTX 5070 (sm_120), fetch Tamil files from Dakshina, start the human typing set. Gotchas then: frame as informal romanized Tamil; Aksharantar dev/test mix-up; Dakshina quirks; cite only refs.bib; the Word2Vec assignment is separate.
