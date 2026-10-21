# DECISIONS

Locked decisions. Change one only by adding a new row that supersedes it, never by silent edit. Dates are 2026-10-18 unless noted.

| # | Decision | Why / source |
|---|---|---|
| D1 | Topic: staff list #34, Tanglish-to-Tamil script transliteration, character-level Seq2Seq, Google Dakshina (Tamil) | Lebi's Tamil strength (lyra, lets-talk); new area (first seq2seq model); published baselines to compare against; not claimed by another team |
| D2 | Novelty scope: **C1 + C2 + C3** from `research/NOVELTY_CANDIDATES.md`. C4 (LM/lexicon reranking on noisy input) only if time remains | Coherent story: "clean Dakshina accuracy overstates real typing performance; how much, which architecture degrades least, how to fix it cheaply" |
| D3 | Models: character BiLSTM+attention vs small pre-LN Transformer, matched parameter budgets (about 1M, 3M, 8M), equal tuning budget (about 20 random-search trials each), 5 seeds on the final configs, statistical tests | Resolves the Roark 2020 vs Kirov 2024 conflict; both models are cheap on the RTX 5070 in Leica |
| D4 | Human-typed test set: about 1,500 Dakshina-test words typed WhatsApp-style from Tamil-script prompts by team members (about 500 each) | No public set pairs real informal typing with Tamil-script gold (docs/datasets). Details and a proposed 100-word overlap are in `docs/human-typing-protocol.md` (the overlap is a proposal, not yet confirmed) |
| D5 | Framing: "informal romanized Tamil" in the title; bare "Tanglish" only if the human-typed set supports it | Dakshina is formal Wikipedia Tamil romanized on request, not chat text (`research/DATASET.md` section 6) |
| D6 | Paper: IEEE conference format (IEEEtran), LaTeX in `paper/`, references only from `research/refs.bib` | Lebi's choice |
| D7 | Compute: laptop `rog` RTX 4050 6 GB for development; lab server **Leica** (`ssh airoot`) RTX 5070 12 GB Blackwell sm_120, i7-14700, 15 GB RAM, about 237 GB free, Ubuntu 24.04, Docker empty, no nvcc, for long runs. PyTorch on Leica needs a CUDA 12.8+ build. Source: `/home/lebi/workspace/networks/dscs-lab/` | Lebi's hardware. (An earlier note wrongly put the 5070 in the laptop; corrected, see FIXES.md F1) |
| D8 | Deadline: Lebi said to ignore it; the staff's real date is unknown. Keep a soft internal target of about 2026-11-01 so scope stays bounded | Lebi's instruction (later message superseded "within 2 weeks") |
| D9 | The staff only asks for the deliverable and may not know the field; we follow our own research method: full experiments, statistics, citations, honest limitations | Lebi |
| D10 | Long training runs go on Leica; laptop RTX 4050 for development. Lebi and Claude do the work; no teammate details are needed in the docs | Lebi ("we can complete it by ourselves") |
| D11 | Dakshina stays the clean baseline and training set. More datasets are for augmentation, independent testing and noise calibration, not replacements | Dakshina is not "rubbish": it is the only set with published baselines. Its limit (not real typing) is the paper's gap |
| D12 | Dataset usage rules (details in `docs/datasets/README.md`): never train on IndicXlit sentence pairs, `gowtham58` sets, Mendeley or sanujen sets (Dakshina copies or no targets); use only `data/aksharantar-tamil/tam_test.no_dakshina.tsv` (4,335 rows) as the independent Aksharantar test and report AK-Freq/AK-NEI/AK-NEF separately; Aksharantar train is optional and a separate condition (lemma leakage); real comment corpora only calibrate and validate noise (no gold) | Leakage audit by the dataset agents, 2026-10-18 |
| D13 | Baseline reproduction gate: before any novelty experiment, reproduce Roark 2020 / Kirov 2024 Dakshina Tamil dev CER within about 1 point and document the multi-reference evaluation definition | Protects every later claim; Aksharantar's quoted "Roark 65.7" is a dev number in a test table, do not copy it |
| D14 | Do not start setup, downloads of Dakshina, code or training until Lebi says go. (Dataset downloads into `data/` were explicitly requested and are done.) | Lebi: "don't start now, I will let you know" |
| D15 | Never reboot Leica, touch GRUB, Docker or Swarm there without asking Lebi; check `uname -r` = 6.17.0-22-generic and `nvidia-smi` before any job | The permanent kernel pin was never applied; the next reboot likely breaks the GPU |
| D16 | Repo: private GitHub repo `lebiraja/tamil-translit-robustness`; `data/`, checkpoints, `.env`, venvs are gitignored; keep pushed artifacts small (slow home upload); the Excel with other students' names is in the repo, remove it before any public release | Lebi asked for a private repo with everything committed |
| D17 | Secrets: no tokens or passwords in files. The Hugging Face token pasted in chat was never needed; Lebi should revoke it | Global sudo and secrets rules |

## Still open (need Lebi)
1. Who types the human set? Lebi said the work will be done "by ourselves" and gave no teammate details; three typists is the locked design, one typist would weaken RQ2 (see the protocol doc).
2. Apply the permanent kernel pin on Leica (needs a reboot and sudo)? Recommended before long jobs.
3. Is the NVIDIA container toolkit present on Leica, and is Leica free of other jobs during our runs?
4. Go signal for Phase 1 (environment, Dakshina Tamil fetch, typing set, LaTeX skeleton).
5. Confirm proposals not yet locked: 100-word overlap among typists, stratified word sampling, the exact size budgets, and whether to include Aksharantar train as a separate condition.
6. Hand-check about 300 tokens of the real-comment noise rates before using them to set noise frequencies.
7. The Word2Vec CBOW/Skip-gram assignment (separate from this project): when to do it.

## Resolved
- Aksharantar overlap with Dakshina: resolved 2026-10-18, see D12.
- Lab system details: resolved by reading the dscs-lab docs, see D7.

| D18 | 2026-10-21 | Lebi gave the go (D14 satisfied) and authorised Leica use and git push/pull. A3 control (CTRL) = same native words romanized greedily, to separate more data from more variation. Credentials given in chat are never stored. | Lebi |
