# Session log: 2026-10-18 (planning, research and dataset survey)

Complete record of what was done in the first working session, in order. Nothing in this session trained a model, wrote project code or touched the lab server. Times are IST and approximate (the working day ran from about 11:10 to 13:30).

## 0. Starting point
- Working directory `/home/lebi/Projects/sem5/deeplearning` contained only `Projects_with_Team_Members.xlsx` (12 KB). It was not a git repo.
- Lebi's request: choose a deep-learning IA3 project with real novelty, write a proper research paper (experiments, results, citations), and look at past projects to pick something new rather than repeat earlier work.

## 1. Startup accountability check
Per the global instructions, the top of `/home/lebi/start-it-up/STATUS.md` and `HANDOVER.md` was read. State then: day 1 of 81 to the 2026-12-31 deadline (74 days left on 2026-10-18), last startup session 2026-10-12 (six days earlier), no problem or idea chosen, open items Q15 (search budget vs field tests), Q16 (first vertical) and Q18 (parents' school intros). Lebi was told once; the startup is not part of this repo.

## 2. Reading the topic list (the Excel)
- `openpyxl` was not installed, so the workbook was unzipped and its XML parsed with `python3 -I` (shared strings plus sheet1).
- 35 projects. Columns: Project No., Title, Model, Dataset, Live Input, Team Members. Eight topics already had teams: #3 helmet violation, #8 currency recognition, #11 skin lesion, #14 electricity load, #18 review sentiment, #24 English-to-Tamil NMT, #31 road-scene U-Net, #32 grammar correction.
- The staff rule (screenshot): each team picks one topic, no duplicates, check the sheet first. A second post (Oct 16) was a separate assignment: Word2Vec CBOW and Skip-gram (references, architecture diagrams, short explanation). That assignment is NOT part of this project and is still pending.

## 3. Reading Lebi's past work
- `gh repo list` returned about 100 repos (mostly private). READMEs read for the deep-learning ones: Retinal-AI (EfficientNet-B4, 45 retinal diseases), truthpixel/AuthentiScan (EfficientNetB0 deepfake detector, 660K images, Grad-CAM, cross-dataset validation), Optical_flow (Lucas-Kanade UAV navigation), voice-id (ECAPA-TDNN speaker verification), lyra (local English and Tamil voice companion), lets-talk/iTantra (offline multilingual voice, SIH 2026), curiosity-is-all-you-need (curiosity-driven agent paper), sdct (synthetic data platform).
- The earlier startup portfolio scan `research/problems/2026-10-11-portfolio-scan.md` was also read.
- Gap found: no time-series deep learning, no seq2seq trained from scratch, no autoencoder anomaly detection, no physiological signals.
- Recommendation given: avoid CNN image classification (done before). Ranking: #34 Tanglish-to-Tamil transliteration, #21 ECG arrhythmia (inter-patient split novelty), #35 predictive maintenance (LSTM autoencoder). Lebi locked **#34**.

## 4. Research phase (two read-only research agents)
Rules given to both: no dataset download, no code, no training; honesty over completeness.

### 4.1 `lit-researcher` (literature)
- Downloaded 32 open-access PDFs into `research/papers/`, read each and wrote 32 notes in `research/notes/`.
- Wrote `research/KNOWLEDGE_BASE.md` (index of 32 papers, state of the art, Dakshina Tamil baseline tables, conflicts between papers, open gaps, metric recommendations), `research/refs.bib` (32 entries) and `research/NOVELTY_CANDIDATES.md` (8 ranked ideas C1 to C8).
- Not fetched: Graves 2006 (CTC, no open copy), Levenshtein 1966. Two cited works are known only second-hand.

### 4.2 `data-researcher` (Dakshina)
- Wrote `research/DATASET.md` and `research/DATASET_QUESTIONS.md`. Verified facts by byte-range reads of the official tar (full 1.87 GiB archive was never downloaded).
- Later corrected section 8 (Aksharantar overlap) and 9 after checking the local Aksharantar file.

### 4.3 Key findings (see KNOWLEDGE_BASE.md and DATASET.md for sources and numbers)
1. Dakshina Tamil is formal Wikipedia Tamil that native speakers romanized on request. It is not WhatsApp-style typing, so "Tanglish" cannot be claimed from Dakshina alone.
2. Lexicon: 25,000 train words (68,218 pairs), 2,500 dev (6,827 pairs), 2,500 test (6,864 pairs), about 2.7 romanizations per word, splits share no words or stems. Sentences: 5,000 dev plus 5,000 test, evaluation only.
3. Data quirks: about 0.35% wrong lexicon pairs (for example a translation instead of a transliteration), at least 5 mismatched sentence pairs, 15 sentences in both dev and test, README misdescribes `split.tsv` (7 columns, not 2).
4. Published Tamil baselines: Roark 2020 dev LSTM CER 8.4 / top-1 65.3; IndicXlit test top-1 68.1; with a unigram rerank 78.5; GPT-4.5 76.6 (preprint). Aksharantar's "Roark 65.7" row is a dev number placed in a test table.
5. Gaps: no paired robustness benchmark for Tamil romanization; no public naturally typed set with Tamil-script gold; LSTM vs Transformer contested (Roark 2020 vs Kirov 2024) and never tested under noise; variation-aware augmentation untested for transliteration robustness.

## 5. Decisions made with Lebi (via questions)
| Question | Answer |
|---|---|
| Compute | initially misreported (see section 8); final: laptop RTX 4050 6 GB for development, lab server Leica RTX 5070 12 GB for long runs |
| Paper format | IEEE conference |
| Tamil ability | all three team members can type Tamil |
| Deadline | first "within 2 weeks", later "ditch it, it doesn't matter" (soft internal target about 2026-11-01 kept) |
| Novelty scope | C1 + C2 + C3 |
| Models | BiLSTM-attention vs small Transformer, about 3M parameters, 5 seeds |
| Human test set | team members type about 500 words each (about 1,500) |
| Framing | "informal romanized Tamil", not bare "Tanglish" |
| Teammate details | Lebi declined to provide ("we can complete it by ourselves") |

## 6. Project documents created
`DECISIONS.md`, `PROJECT_INTRO.md`, `CHECKLIST.md`, `STATUS.md`, `FIXES.md`, `HANDOVER.md`, `CLAUDE.md` (all in the repo root). This session's later pass expanded all of them and added `README.md` and the `docs/` set.

## 7. Lab server review (read-only)
Read `/home/lebi/workspace/networks/dscs-lab/` (README plus files 01 to 08 and CHANGES). Nothing was run on the server. Details are in `docs/infrastructure.md`. Highlights: server nicknamed Leica, reached with `ssh airoot`, RTX 5070 12 GB, 15 GB RAM, 237 GB free after a Docker wipe, GPU only works on kernel 6.17.0-22 and the permanent pin was never applied.

## 8. Mistakes made and corrected during the session
1. **Wrong GPU attribution.** Lebi pasted the 5070 spec and said "my lab system"; I recorded it as the laptop's GPU in D7, CLAUDE.md and HANDOVER.md. After reading the lab docs (laptop = RTX 4050 6 GB, Leica = RTX 5070 12 GB) all three files were corrected. A leftover "laptop RTX 5070" in D10 was fixed in a follow-up commit.
2. **Dakshina "rubbish".** Lebi described the staff's dataset as rubbish; it was clarified that Dakshina is a good clean baseline whose limitation is that it is not real informal typing. The fix is more data, not discarding it.
3. **Agent noise.** Idle and duplicate notifications from the four agents were relayed to Lebi, which was confusing. Rule going forward: only relay actionable news.
4. **API timeouts.** Both dataset agents hit "No response from API" errors (3 min then 10 min) mid-task. One had already written its doc; the other was resumed with a narrower brief and wrote its doc in small pieces.
5. **Overlapping scope.** The two dataset agents both downloaded and documented overlapping folders; ownership was split explicitly (pair sets vs informal sets).
6. **Credential in chat.** Lebi pasted a Hugging Face token into the chat. It was passed to the agents only for env-var use and was never needed; it appears in no repo file (checked with grep). Lebi should revoke it. Two passwords from the earlier lab session are also still unrotated.

## 9. Git
- Initial commit `090d4f2` (planning, 32 papers, knowledge base, decisions); repo `https://github.com/lebiraja/tamil-translit-robustness` created private by `gh repo create`.
- `ec69268`: dataset survey docs, overlap findings, measurement scripts, STATUS and DECISIONS updates.
- `7522579`: laptop GPU fix in D10.
- This pass adds a further commit (the documentation expansion).
- `.gitignore` excludes `data/`, `.venv/`, `venv/`, `.env`, `*.pt`, `*.ckpt`, `.claude/`, `__pycache__/`, `*.pyc`.
- The Excel (with other students' names and register numbers) is in the repo. The repo is private. Remove the file before any public release.

## 10. Dataset survey (two more agents)
- `pairs-data-researcher`: pair sets and Tamil text. `informal-data-researcher`: real informal Tanglish and code-mixed sets. About 28 folders and 965 MB downloaded to `data/` (gitignored). Disk: 464 GB free on the laptop.
- Outputs: `docs/datasets/pairs-and-text-datasets.md`, `docs/datasets/informal-tanglish-datasets.md`, `docs/datasets/informal-tanglish-measurements.json`, `docs/datasets/tanglish_measure.py`, and 15 reproduction scripts in `docs/datasets/pairs_scripts/`.
- Main results (full detail in those docs and `docs/datasets/README.md`):
  - Aksharantar's Tamil test file contains all 6,864 Dakshina test pairs; the independent remainder is `data/aksharantar-tamil/tam_test.no_dakshina.tsv` (4,335 rows / 3,707 words: AK-Freq 2,608, AK-NEI 1,013, AK-NEF 714). Filter rule verified: non-Dakshina rows whose NFC native word is in no Dakshina split.
  - Aksharantar train is word-disjoint from Dakshina dev/test but 97.1% of Dakshina test words share a stem prefix with it (33.7% for Dakshina train), so it is a separate experimental condition.
  - IndicXlit Tamil sentence pairs equal Dakshina test sentences; `gowtham58` lexicon is Dakshina train; `gowtham58` sentences contain 4,919 Dakshina test sentences. Never train on these.
  - Real informal Tanglish exists (DravidianCodeMix 44,020 comments, HopeEDI 18,178, Tanglish-Corpus-185k 174,424) but with sentiment/offence labels only, no Tamil-script gold. TamilMixSentiment, offenseval, Tngarg and IsaacRodgz are copies of DravidianCodeMix.
  - Measured against Dakshina sentences: vowel dropping 3 to 5 times more frequent in real comments, vowel-length collapse 1.8 to 3.5 times, elongation up to about 9 times, h-dropping not more frequent (so digraph noise should be symmetric swaps).
  - Not obtained: NEWS 2012/2018 En-Ta (licence), Brahmi-Net (HTTP 502), OSCAR (gated), TAMZHI (unreleased), Hellsten 2017 and Wolf-Sonkin 2019 test sets (proprietary), HASOC and FIRE 2021 (login).
- The Hugging Face token was not needed for any download.

## 11. What was deliberately NOT done
- No environment setup, no Docker image, no dataset download of Dakshina itself, no code, no training (Lebi: "don't start now, I will let you know").
- No change to Leica (no reboot, no GRUB, no Docker, no Swarm).
- Human typing set not collected; prompt sheet not yet prepared.
- LaTeX skeleton not yet created.
- Word2Vec assignment not started.

## 12. State at end of session
Planning complete and documented; research and datasets in hand; waiting for Lebi's go to start Phase 1 (environment, Tamil data fetch, typing set). See `HANDOVER.md` and `CHECKLIST.md`.
