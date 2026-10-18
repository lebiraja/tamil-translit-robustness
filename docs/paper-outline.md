# Paper outline (IEEE conference, IEEEtran, LaTeX)

Status: outline only; no LaTeX yet. Build with the `research-paper` skill (local TeX Live and Texpile) in `paper/`. Bibliography from `research/refs.bib` (32 entries, each read; add entries only for papers actually read). Every number in the paper must trace to a logged run in `results/`.

## Working title (framing locked in D5: "informal romanized Tamil")
"How Robust Is Neural Transliteration to Informal Typing? A Paired Noise Benchmark and Augmentation Study for Romanized Tamil"
Alternatives: "Beyond Clean Romanization: ..." / "Tanglish Is Not Dakshina: ...". Avoid bare "Tanglish" in the title unless the human-typed set is in and supports it.

## Abstract (about 150 words, written last)
Problem (informal typing), gap (no paired Tamil robustness benchmark, LSTM vs Transformer unresolved), contributions (benchmark with Tamil noise taxonomy plus human-typed set, augmentation comparison, matched-budget architecture comparison), headline numbers, release statement.

## Sections
1. **Introduction.** Tanglish usage and why Latin-to-Tamil conversion matters (keyboards, search, messaging). Clean-benchmark accuracy versus real typing. Contributions list (3 bullets). Research questions RQ1 to RQ4.
2. **Related work.** Dakshina and Aksharantar; neural transliteration (Roark 2020, Kirov 2024, Madhani 2023, Kunchukuttan 2021); keyboards and WFST (Hellsten 2017, Wolf-Sonkin 2019); informal and shorthand Tamil (TAMZHI 2024, IndoNLP 2025, Baiju 2024, Azam 2025); noise robustness (Belinkov and Bisk 2018, Karpukhin 2019, Xue 2022); synthetic variation (Benton 2025, Sennrich 2016); architecture comparisons (Moran 2020, Wu 2021). End with the gap statement from `research/KNOWLEDGE_BASE.md` section 5.
3. **Data.** Dakshina lexicon (counts, splits, quirks); Aksharantar independent set and its filtering rule; leakage handling; real comment corpora used only for noise calibration; the human-typed set (protocol, counts, per-typist stats). Table of datasets with roles.
4. **Noise taxonomy (C1).** Operators, severities, cited basis, calibration against real comments (rates in the informal-datasets measurements), pairing with clean forms, validation plan for synthetic versus human noise.
5. **Models and training (C3).** BiLSTM-attention and pre-LN Transformer, size budgets, equal tuning budget, search space, seeds, decoding, optimization, reproduction of published baselines.
6. **Augmentation (C2).** A0 to A4 and control, held-out noise types.
7. **Experiments and results.** 7.1 baseline reproduction versus Roark/Kirov; 7.2 clean accuracy; 7.3 degradation per noise type and severity (curves); 7.4 human-typed set; 7.5 synthetic-versus-human correlation (RQ2); 7.6 augmentation results; 7.7 architecture comparison with statistical tests; 7.8 (optional) LM reranking.
8. **Analysis and discussion.** Error analysis (which Tamil letters confuse under which noise; ambiguity ceiling via oracle top-k), per-typist differences, what the register mismatch (colloquial versus literary targets) implies, comparison with published numbers (state dev versus test carefully).
9. **Limitations and ethics.** Dakshina is formal and elicited; few typists; typing from Tamil-script prompts may be more careful than chat; label noise; word-level only; consent and release of the typed set.
10. **Conclusion and future work.** Sentence-level context, colloquial targets (C8), on-device Pareto (C5), CTC (C6).
11. **References** (from `refs.bib`).
Appendices: full hyperparameters and search space, noise operator pseudocode, complete per-operator tables, data cleaning and filtering rules with counts, reproduction commands.

## Figures and tables plan
| ID | Content | Source |
|---|---|---|
| T1 | Dataset roles and sizes | docs/datasets |
| T2 | Noise operators with examples | experiment-plan section 4 |
| T3 | Baseline reproduction versus published numbers | results/baseline |
| T4 | Clean and noisy accuracy, both architectures, three sizes | results/c3 |
| F1 | Degradation curves per noise type versus severity | results/c1 |
| F2 | Synthetic versus human degradation scatter, with Spearman rho | results/c1 + human |
| T5 | Augmentation matrix (clean, each noise, held-out, human) | results/c2 |
| T6 | Statistical tests (bootstrap, Kruskal-Wallis, effect sizes) | results/stats |
| F3 | Per-typist pattern rates versus real comments | human set + informal measurements |
| F4 | Error analysis (confusions by Tamil letter under V-DROP/GEM) | results/analysis |

## Claim to evidence map (fill as results arrive)
| Claim | Needed evidence | Status |
|---|---|---|
| Clean accuracy overstates real performance | T4 clean versus human-typed | pending |
| Vowel drop and geminate collapse hurt most | F1 | pending (hypothesis) |
| Synthetic noise predicts human degradation | F2 | pending |
| Phonological and sampled-back-transliteration augmentation help | T5 | pending |
| Architecture choice matters (or does not) at matched budget | T4, T6 | pending |

## Writing rules
- Cite only what was read; mark second-hand claims as such.
- Quote published numbers with split (dev or test) and source; never reuse Aksharantar's "Roark 65.7" as a test baseline.
- Tables and figures generated by scripts from `results/`.
- Honest limitations section; no "state of the art" claims without a like-for-like comparison.
- Compile cleanly before every commit that touches `paper/`.
