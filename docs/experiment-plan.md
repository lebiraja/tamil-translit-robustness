# Experiment plan (locked scope: C1 + C2 + C3; C4 optional)

Status: planned, nothing run yet. Everything here derives from `research/NOVELTY_CANDIDATES.md`, `research/KNOWLEDGE_BASE.md` and `docs/datasets/`. Parameters in square brackets are proposals to confirm after the first smoke test, not locked decisions. Locked decisions live in `DECISIONS.md`.

## 1. Task definition
Input: one romanized (Latin-script) Tamil word, lowercase a to z. Output: the Tamil-script word (NFC normalized Unicode, code-point level). Word-level transliteration. Sentence-level is out of scope (Dakshina has no human-written sentence training data).

## 2. Research questions and hypotheses
| RQ | Question | Hypothesis (to test, not assume) |
|---|---|---|
| RQ1 | How much does CER and accuracy degrade per noise type and severity? | Large drop for vowel drop (V-DROP) and geminate collapse (GEM), small for keyboard noise (KEY); degradation grows monotonically with severity |
| RQ2 | Does synthetic noise predict degradation on human-typed text? | Human-set degradation lies between the mild and the severe synthetic settings; rank correlation across systems is positive |
| RQ3 | Which training augmentation recovers robustness without hurting clean accuracy (loss <= 0.5 CER)? | Tamil-phonological noise and sampled back-transliteration beat random character noise; improvements transfer to held-out noise types and the human set |
| RQ4 | Which architecture degrades least at matched size and tuning budget? | Not predetermined. Literature conflicts (Roark 2020 LSTM, Kirov 2024 Transformer); a null result is reportable and resolves the conflict as seed noise |

## 3. Data and splits
| Role | Data | Path | Use |
|---|---|---|---|
| Train | Dakshina Tamil lexicon train (25,000 words / 68,218 pairs) | fetch per `research/DATASET.md` section 2 (about 23 MB by byte ranges) into `data/dakshina-ta/` | the only supervised training set in the main experiments |
| Dev | Dakshina lexicon dev (2,500 / 6,827) | same | early stopping, hyperparameter search, tuning alpha/beta for C4 |
| Clean test | Dakshina lexicon test (2,500 / 6,864) | same | final clean numbers, comparison with Roark 2020 / Kirov 2024 |
| Independent test | Aksharantar non-Dakshina rows | `data/aksharantar-tamil/tam_test.no_dakshina.tsv` (4,335 rows) | report AK-Freq, AK-NEI, AK-NEF separately |
| Synthetic noisy tests | noise operators applied to the Dakshina test romanizations | generated, seeded | RQ1, every noisy item paired with its clean form and gold |
| Human-typed set | about 1,500 Dakshina test words typed by the team | `data/human-typed/` (created by us; see `human-typing-protocol.md`) | RQ2, RQ3, RQ4 on real typing |
| Augmentation source | Sangraha synthetic, native Tamil text samples, IndicXlit indic-to-en model | `data/sangraha-synthetic-tamil-sample/`, `data/fineweb2-tamil-sample/`, `data/indiccorpv2-tamil-sample/` | A3 (sampled back-transliteration); filter out every Dakshina dev/test word first |
| LM / lexicon (C4 only) | IndicXlit unigram dictionary, FineWeb-2, IndicCorpV2 | `data/indicxlit-wordprob-tamil/`, etc. | rerank and shallow fusion; report OOV rates because coverage of Dakshina test is 98 to 100 percent |

Rules:
- **Never train on** IndicXlit sentence pairs, `gowtham58` sets, Mendeley or sanujen sets, or anything containing Dakshina test/dev words (`docs/datasets/README.md`).
- Aksharantar train is optional and, if used, is a **separate condition** (lemma leakage: 97.1 percent of Dakshina test words share a stem prefix with it).
- Hold-out words for the human set are sampled **from Dakshina test only**, with a recorded seed, so every human item has a gold reference and a clean counterpart.
- Normalize NFC; lowercase romanized input; log every filtering rule and the resulting counts.
- Data cleaning: remove or flag the roughly 0.35 percent suspect lexicon pairs with a logged rule (for example high-cost cross-validated pairs), and report results with and without the cleaning in an appendix; do not silently clean the **test** set.

## 4. Noise model (C1)
Operators act on the romanized input only. Each has a cited basis (see NOVELTY_CANDIDATES C1). Severity `p` in {0.1, 0.2, 0.3, 0.5} is the per-eligible-position application probability. Seeds are fixed and stored so noisy test sets are reproducible and paired.

| Op | Effect | Basis |
|---|---|---|
| V-DROP | delete non-initial vowels ("kanakkil" to "kankl") | TAMZHI 2024; Benton 2025; measured 3 to 5 times more frequent in real comments (docs/datasets/informal-tanglish-datasets.md 4.2) |
| V-LEN | collapse long vowels (aa to a, ee/ii to i, oo to o, uu to u) | Wolf-Sonkin 2019; measured 1.8 to 3.5 times |
| GEM | collapse geminates (kk to k, tt to t, pp to p, ll to l) | Wolf-Sonkin 2019; measured 1.2 to 1.8 times (under-counted) |
| DIGRAPH | symmetric swaps th/t, dh/d, ch/c/s, sh/s, zh/l/z (optional h) | Wolf-Sonkin 2019; TAMZHI; real data show h-dropping is not more frequent than in Dakshina, so make it a **two-way swap**, not a deletion |
| KEY | adjacent-key QWERTY substitution (Gaussian tap model) | Wolf-Sonkin 2019; Belinkov and Bisk 2018 |
| REPEAT | elongation of a letter ("semmaaa") | Xue 2022; Mandal 2018; up to about 9 times more frequent |
| MIX | random combination of the above | Karpukhin 2019 "balanced diet" |

Calibration (inference, to be checked): set relative frequencies from the real-vs-Dakshina excess in `docs/datasets/informal-tanglish-datasets.md` section 4.2 and **hand-check about 300 tokens** before quoting any rate in the paper. English tokens and chat abbreviations (jst, tym, pls) are pass-through, outside the Tamil noise model.

Unit tests (pytest) for each operator: determinism under a seed, idempotence where applicable, never emptying a word, preserving the Latin alphabet, pairing to the clean source.

## 5. Models (C3)
Two architectures, character-level on both sides, shared vocabulary built from training data only.
- **BiLSTM + attention:** bidirectional LSTM encoder, LSTM decoder, Luong (or Bahdanau) attention, as in Roark 2020 and Kirov 2024.
- **Small Transformer:** pre-LN encoder-decoder, label smoothing 0.1, warmup schedule (Vaswani 2017 recipe, Wu et al. 2021 caveat on batch size).
- **Size budgets:** [about 1M, about 3M, about 8M] parameters per architecture, so comparisons are matched on parameters (Moran and Lignos 2020 showed a 2.7 times parameter confound).
- **Equal tuning budget:** [20 random-search trials each] over learning rate, dropout, batch size in {64 to 512}, warmup, label smoothing, then **5 seeds** (10 if time) of the best config. Report mean and standard deviation.
- **Decoding:** beam search [k = 10] to give top-1 and top-5 and MRR. Greedy as a speed comparison.
- **Optional reference:** public IndicXlit (inference only) as an external system; ByT5-Small only if time remains (heavier).
- Mixed precision on Blackwell only after the baseline reproduces; keep bf16/fp16 as a logged config option.

## 6. Baseline reproduction gate (before any novelty experiment)
Train the BiLSTM+attention on Dakshina Tamil train with Roark's setup and confirm dev CER is near Roark 2020's 8.4 (LSTM) and Kirov's 8.6, and the Transformer near 9.4 / 8.2. Document the evaluation definition (multiple attested references, how attestation counts are used) and test it. If we cannot get within about 1 CER point, stop and debug before running C2/C3. This protects every later claim.

## 7. Augmentation study (C2)
Train each architecture (best C3 config) under:
| ID | Training data |
|---|---|
| A0 | Dakshina lexicon only (baseline) |
| A1 | A0 + random character noise diet (60 percent clean, 10 percent each deletion, insertion, substitution, swap; resampled every epoch; Karpukhin 2019) |
| A2 | A0 + Tamil-phonological noise (V-DROP, V-LEN, GEM, DIGRAPH), resampled every epoch |
| A3 | A0 + sampled back-transliteration: train a native-to-Latin model on the Dakshina lexicon (or use IndicXlit indic-to-en), romanize Dakshina-filtered Tamil words by sampling from the 8-best, add as synthetic pairs |
| A4 | A2 + A3 |
| Control | A0 + the same number of extra clean pairs (separates "more data" from "more variation") |

Evaluate on: clean test, every noise type, **held-out noise types** (train A2 without GEM, test on GEM), the independent Aksharantar set, and the human-typed set. Success criterion for RQ3: lower human-set CER than A0 and A1 with at most 0.5 CER loss on clean.

## 8. Optional C4 (only if time remains)
Beam k=10 plus unigram rerank F = alpha T + (1 minus alpha) P (Aksharantar), shallow fusion with a character LM (Gulcehre 2015), soft trie prior with OOV escape. Tune on dev; report gains separately for clean, each noise type, human set, and in-vocabulary vs OOV references. Caveat: lexicon coverage of Dakshina test is 98.7 percent (top 200k IndicXlit types), so clean-set gains are optimistic.

## 9. Metrics
- **Top-1 accuracy** (exact match against any attested reference, NEWS ACC), **top-5**, **MRR**.
- **CER** (Levenshtein over Unicode code points, corpus level; Roark 2020 / Kirov 2024 definition).
- Robustness: delta-CER and relative accuracy (noisy over clean) per noise type and severity; degradation curves.
- RQ2: rank correlation (Spearman) between systems' synthetic degradation and human-set degradation.
- Efficiency: parameters, training time, CPU latency per word (optional).
- Statistics: mean +/- sd over 5 seeds; paired bootstrap on word-level errors for system pairs; Kruskal-Wallis with Dunn post-hoc across more than two systems (Moran and Lignos 2020 methodology); report effect sizes and per-typist variance on the human set.
- Oracle top-k on vowel-dropped inputs, because "knkl" is genuinely ambiguous and the ceiling is unknown.

## 10. Run matrix and logging
| Block | Runs (estimate) |
|---|---|
| Baseline reproduction | 2 to 5 |
| Hyperparameter search | 2 archs x 3 sizes x 20 trials = 120 (short) |
| C3 final models | 2 archs x 3 sizes x 5 seeds = 30 |
| C2 augmentation | 6 conditions x 2 archs x 5 seeds = 60 |
| Noise evaluation | inference only (cheap) |
Each run writes `results/<block>/<run-id>.json` with: config, seed, git commit, data file checksums, torch and CUDA versions, GPU, wall time, metrics per test set. Configs live in `configs/` under version control. Figures and tables for the paper are generated from the JSON by scripts, never by hand.

## 11. Risks and mitigations
| Risk | Mitigation |
|---|---|
| Null result in C3 | Frame as a careful matched-budget replication plus a robustness axis; it resolves the Roark/Kirov conflict either way |
| Synthetic noise generator leaks into test | Held-out operators; human-typed set; noise seeds separate from train seeds |
| Human set idiosyncratic (few typists) | Per-typist reporting, shared overlap words, call it a probe set; more typists if possible |
| Typing from Tamil-script prompts is more careful than real chat | State as a limitation; compare pattern rates with real comments (informal doc 4.2) |
| Vowel-dropped inputs are ambiguous | Report top-k and oracle ceilings |
| Dakshina label noise (about 0.35 percent) | Do not clean the test set silently; report with and without |
| Aksharantar/Dakshina stem overlap | Separate condition, clearly labelled |
| Blackwell PyTorch issues | Smoke test first; fall back to the laptop GPU for development |
| Leica kernel/GPU breakage on reboot | Never reboot; check `uname -r` and `nvidia-smi` before jobs; pin kernel with Lebi's permission |
| Time | Scope is C1+C2+C3; C4 only if time remains; reproduction gate prevents wasted runs |
