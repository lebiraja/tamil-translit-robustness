# Knowledge Base — Tanglish → Tamil Script Transliteration (char-level Seq2Seq, Dakshina)

Compiled 2026-10-18. 32 papers downloaded to `papers/`, one note per paper in `notes/` (same file stem). All numbers below were read in the papers themselves unless marked *second-hand* or *inference*. Dataset was not downloaded; no experiments were run.

---

## 1. Index

Read status: **Full** = whole paper read; **Main** = main text fully read, appendices skimmed.

| # | File stem | Citation | Topic | Read | Key fact for us |
|---|---|---|---|---|---|
| 1 | roark-2020-dakshina | Roark et al., LREC 2020 | Dataset + baselines | Full | Tamil dev CER: pair6g 9.3, Transformer 9.4, LSTM **8.4**; 2.7 romanizations/word |
| 2 | kirov-2024-context-aware-transliteration | Kirov et al., *Comput. Linguistics* 50(2) 2024 | Context, ensembles, LM, ByT5, metrics | Main | 25 seeds: Transformer **8.2** < LSTM 8.6 CER on Tamil; Tamil lexicon has label noise; word LM 27.2→17.6 sentence WER |
| 3 | madhani-2023-aksharantar | Madhani et al., Findings EMNLP 2023 | Aksharantar 26M pairs, IndicXlit | Full | Tamil Dakshina test top-1 68.10 → **78.53** with unigram-LM rerank; 11M params |
| 4 | kunchukuttan-2021-largescale-neural-transliteration | Kunchukuttan, Jain, Kejriwal, EACL 2021 | Multilingual Indic xlit | Full | Tamil script "highly under-specified"; small BiLSTM 128 units |
| 5 | kunchukuttan-2018-orthographic-similarity-multilingual-xlit | Kunchukuttan et al., TACL 2018 | Multilingual xlit | Main | en→ta bilingual 57.80 > multilingual 55.30 |
| 6 | kunchukuttan-2015-brahminet | Kunchukuttan, Puduppully, Bhattacharyya, NAACL Demo 2015 | Rule + SMT xlit system | Full | Tamil collapses voiced/aspirated plosives; top-1 vs top-5 gap |
| 7 | hellsten-2017-transliterated-keyboard-wfst | Hellsten et al., FSMNLP 2017 | On-device WFST keyboard | Full | Real typed Tamil test: WER 26.2 → 22.6, 0.2 ms/char, LM 9.8 MB |
| 8 | wolfsonkin-2019-latin-keyboards-fst | Wolf-Sonkin et al., FSMNLP 2019 | Romanization variation, keyboards | Full | Variation typology (h-dropping, vowel/geminate doubling); Gaussian tap-noise simulation |
| 9 | herath-2024-tamzhi-shorthand-tamil | Herath & Sumanathilaka, ICTer 17(1) 2024 | **Shorthand Tanglish** (vowel-dropped) | Full | 215-user typing survey; rule-generated variants; 93% char / 70% word acc on 700 items |
| 10 | sumanathilaka-2025-indonlp-reverse-transliteration | Sumanathilaka et al., IndoNLP 2025 shared task (arXiv) | Ad-hoc typing benchmark | Full | General vs ad-hoc (vowel-omitted) test split; all systems degrade |
| 11 | baiju-2024-malayalam-romanized-transliteration | Baiju et al., arXiv 2024 (IndoNLP 2025 system) | Malayalam BiLSTM | Full | CER **7.4 → 22.7** on ad-hoc input (Dravidian sister language) |
| 12 | azam-2025-llm-transliteration-benchmark | Azam et al., arXiv 2025 | LLMs vs IndicXlit | Full | Tamil Dakshina top-1: IndicXlit 67.97, GPT-4.5 76.61; noisy 100 words: ~20 |
| 13 | chakravarthi-2020-tamil-codemix-sentiment | Chakravarthi et al., arXiv / SLTU-CCURL 2020 | Real Tanglish corpus | Full | 15,744 YouTube Tanglish comments, vocab 30,898, no native refs |
| 14 | mandal-2018-normalization-transliterated-codemix | Mandal & Nanmaran, arXiv 2018 | Seq2seq + lexicon snap (Bengali) | Full | 51% → 90.27% with nearest-lexicon matching |
| 15 | madhani-2023-bhasha-abhijnaanam-lid | Madhani, Khapra, Kunchukuttan, ACL 2023 | Romanized LID | Main | Synthetic romanization 95.96% vs human 80.40% LID acc |
| 16 | benton-2025-informally-romanized-lid | Benton et al., arXiv 2025 | Variation-aware synthesis | Main | Sampling k-best romanizations ≫ 1-best; Dakshina 2.8 vs Aksharantar 1.011 romanizations/word |
| 17 | gharami-2025-romanized-hindi-bengali | Gharami et al., arXiv 2025 | LLM-generated casual romanization | Full | 150k Gemini "casual" romanizations; in-distribution eval only |
| 18 | belinkov-2018-synthetic-natural-noise | Belinkov & Bisk, ICLR 2018 | Noise robustness | Full | Noise types don't transfer; natural noise = 34% phonological, 32% omissions |
| 19 | karpukhin-2019-synthetic-noise-robustness | Karpukhin et al., arXiv 2019 (W-NUT) | Synthetic noise training | Full | 40% token noise diet; deletion most useful; no gain on social-media style variation |
| 20 | xue-2022-byt5 | Xue et al., TACL 10 2022 | Byte vs subword | Main | Dakshina macro CER ByT5-Small 9.8 vs mT5-Small 20.7; byte models robust to drop/repeat noise |
| 21 | sennrich-2016-bpe | Sennrich, Haddow, Birch, ACL 2016 | BPE subwords | Full | Subword baseline for char-vs-subword ablation |
| 22 | sennrich-2016-backtranslation | Sennrich, Haddow, Birch, ACL 2016 | Back-translation | Full | Precedent for back-transliteration augmentation |
| 23 | gulcehre-2015-monolingual-lm-fusion | Gulcehre et al., arXiv 2015 | Shallow/deep LM fusion | Full | log p_TM + β log p_LM; gains depend on LM domain match |
| 24 | kim-2016-sequence-knowledge-distillation | Kim & Rush, EMNLP 2016 | Seq-KD, pruning | Full | Student 10× faster; greedy ≈ beam after Seq-KD |
| 25 | wu-2021-transformer-char-transduction | Wu, Cotterell, Hulden, EACL 2021 | Transformer for char tasks | Full | Transformer beats RNN only with batch ≥128 |
| 26 | moran-2020-low-resource-ne-transliteration | Moran & Lignos, LoResMT 2020 | LSTM vs Transformer, 10 seeds | Full | Transformer 73.01 vs LSTM 71.49 acc, but 2.7× params |
| 27 | rosca-2016-seq2seq-transliteration | Rosca & Breuel, arXiv 2016 | CTC vs attention | Full | CTC (epsilon insertion) competitive with attention |
| 28 | chen-2018-news-transliteration-shared-task | Chen et al., NEWS 2018 | Metrics, En→Ta | Full | ACC/F-score/MRR/MAP definitions; En→Ta best ACC 0.334, F 0.85 |
| 29 | sutskever-2014-seq2seq | Sutskever, Vinyals, Le, NeurIPS 2014 | Seq2seq | Full | Encoder–decoder; source reversal |
| 30 | bahdanau-2015-attention | Bahdanau, Cho, Bengio, ICLR 2015 | Additive attention | Main | BiRNN + alignment model |
| 31 | luong-2015-attention | Luong, Pham, Manning, EMNLP 2015 | Multiplicative/local attention | Full | Dakshina LSTM baseline uses Luong attention |
| 32 | vaswani-2017-transformer | Vaswani et al., NeurIPS 2017 | Transformer | Full | Base recipe (warmup 4000, LS 0.1) |

**Not fetched (and why):** Graves et al. 2006 (CTC) — ICML paper, no arXiv/ACL open copy found, so CTC is covered via Rosca & Breuel 2016 only. Levenshtein 1966 — not open access; CER/edit distance definitions are taken from Roark 2020 / Kirov 2024. Baruah et al. 2024 (Assamese romanization; reported BiLSTM best) and IndiDataMiner (IndoNLP 2025) are known only second-hand via Gharami 2025 / Sumanathilaka 2025. Kunchukuttan et al. 2018 TACL was read in its main text; zero-shot sections only lightly.

---

## 2. State of the art (synthesised)

### 2.1 The task and the data
Dakshina (Roark 2020) is the standard benchmark: for Tamil, a 25k-train / 2.5k-dev / 2.5k-test romanization lexicon (2.7 attested romanizations per native word, lemma-disjoint splits), 10k manually romanized Wikipedia sentences (5k dev / 5k test), and 1.14M native-script Wikipedia sentences for LMs. Romanizations were *elicited* from annotators with no guidance; they show real variation (Kirov 2024: 1.9 romanizations per repeated word even inside sentences), but they are careful, out-of-context typings of encyclopaedic vocabulary. Aksharantar (Madhani 2023) adds 3.3M Tamil pairs, mostly mined, at only ~1 romanization per word (Benton 2025: 1.011 over 11 languages) and with annotators told to avoid "frivolous variants". Both papers' authors state their data is cleaner than real input (Aksharantar Limitations; Dakshina §1).

### 2.2 What works on clean Dakshina Tamil (word level)
- Small models are already strong and close to each other: pair 6-gram WFST, BiLSTM+Luong attention and a 4-layer char Transformer all lie within ~1 CER point on Tamil (Roark 2020; Kirov 2024). Large pretrained byte models (ByT5) help a little after careful data pruning (Kirov: 7.9 CER) and are unstable without it (12.7, std 3.85).
- **Data scale and LM reranking matter more than architecture.** IndicXlit's gain over Dakshina-only training comes from mined data (Tamil 56.04 → 67.72 when IndicCorp-mined pairs are added), and a unigram word-LM rerank of the top-4 adds another ~10 points (68.10 → 78.53) (Madhani 2023). In sentences, a word-level LM gives most of the benefit of context (Kirov 2024: ~80% of the relative WER reduction).
- Very large LLMs reach 76.61% top-1 (GPT-4.5) on Dakshina Tamil test (Azam 2025) — above IndicXlit without rerank, below IndicXlit with rerank (78.53, from a different paper and likely a different scoring script; not strictly comparable).

### 2.3 Tamil is a special case
Tamil script under-specifies voicing/aspiration (Kunchukuttan 2015; 2021), making Tamil→Latin one-to-many and causing Tamil to be the outlier in multilingual models (it gets the smallest IndicXlit gain, +4.6; multilingual training *hurts* en→ta in Kunchukuttan 2018). For our direction (Latin→Tamil) the hard ambiguities are short/long vowels, gemination, and the l/ḷ/ḻ, n/ṇ/ṉ, r/ṟ distinctions that Latin letters do not encode (*inference* from TAMZHI's mapping table and IndicXlit's error analysis on other languages; no paper reports a Tamil-specific confusion matrix). Tamil is agglutinative: closed-vocabulary noisy-channel models lose to neural models on Tamil/Malayalam sentences (Roark 2020), and Dravidian languages benefit least from sentence context (Kirov 2024).

### 2.4 Informal / noisy input — the robustness gap
- Evidence that clean-trained transliterators break on informal input: Malayalam BiLSTM CER 7.4 → 22.7 on vowel-omitted input (Baiju 2024); every IndoNLP-2025 system degrades on the ad-hoc split (Sumanathilaka 2025); on 100 hand-noised words per language all models including GPT-4o collapse to ~20% top-1 for Tamil (Azam 2025); real typed Tamil on a phone keyboard gives 22.6% WER even for a production WFST system (Hellsten 2017).
- What the noise looks like: systematic, phonologically motivated variation — optional aspiration 'h', optional vowel/consonant doubling (Wolf-Sonkin 2019), vowel omission/shorthand ("kankl", "yrkku" — TAMZHI's 215-user survey), implicit-vowel realisation, vowel quality and gemination (Benton 2025), plus fat-finger typos, elongation and code-mixed English inside Tamil morphology ("sivakarthickku", Chakravarthi 2020).
- What helps, from adjacent tasks: training on noise helps mostly for the *same* noise type (Belinkov & Bisk 2018); a mixed "balanced diet" of deletions/insertions/substitutions/swaps gives robustness to natural typos at <1 point clean cost (Karpukhin 2019) but **does not** help stylistic social-media variation; byte/char models are intrinsically more robust than subword models (Xue 2022); **synthetic data that reproduces human variation (sampling from romanizer k-best) beats bigger models** for romanized LID (Benton 2025); machine-romanized test data massively overstates performance (96% vs 80% LID accuracy; Madhani 2023 LID). Lexicon snapping/LM reranking also buys robustness (Mandal 2018: 51% → 90%; Vectora's dictionary+BERT system barely degrades on ad-hoc Sinhala).

### 2.5 Architecture comparison (char Seq2Seq vs Transformer) is unresolved
Roark 2020 (5 seeds): LSTM best CER on Tamil (8.4 vs 9.4, Transformer std 0.52). Kirov 2024 (25 seeds, same hyperparameters): Transformer 8.2 vs LSTM 8.6, and after 5-model ensembling LSTM = Transformer on average; LSTM k-best lists better match human variant distributions (EMD). Moran & Lignos 2020: Transformer wins significantly but with 2.7× the parameters. Wu et al. 2021: Transformers only win at large batch (≥128) — a hyperparameter confound neither Dakshina paper controls. Baruah et al. 2024 (*second-hand*): BiLSTM best on informal Assamese. No study compares them under noisy input.

### 2.6 Lightweight / on-device
Deployed systems are FST-based with ~10 MB budgets and ≤20 ms/tap (Hellsten 2017; Wolf-Sonkin 2019). IndicXlit is 11M params; char Transformers of 2–6M and BiLSTMs of ~2M are competitive (Moran 2020; Roark 2020). Seq-KD + pruning gives 13× smaller NMT students at small cost and greedy≈beam (Kim & Rush 2016). No paper reports an accuracy–size–latency Pareto for neural Tamil transliteration.

---

## 3. Baseline numbers on Dakshina **Tamil**

### 3.1 Single-word, Latin → Tamil
| System | Split | Top-1 acc % | CER % | Source |
|---|---|---|---|---|
| Pair 6-gram WFST | dev | 63.2 (WER 36.8) | 9.3 (.08) | Roark 2020 T2 |
| Char Transformer (d128, 4+4) | dev | 65.7 (WER 34.3) | 9.4 (.52) | Roark 2020 T2 |
| BiLSTM + Luong attention | dev | 65.3 (WER 34.7) | **8.4** (.12) | Roark 2020 T2 |
| Pair 6-gram (25 runs) | dev | — | 9.4 (.04) | Kirov 2024 T2/B.3 |
| Char Transformer (25 runs) | dev | — | **8.2** (.10) | Kirov 2024 T2 |
| BiLSTM (25 runs) | dev | — | 8.6 (.13) | Kirov 2024 T2 |
| ByT5-base, unpruned / pruned | dev | — | 12.7 (3.85) / 7.9 (.42) | Kirov 2024 T B.3 |
| Bilingual Transformer, Dakshina only | test | 56.04 | — | Madhani 2023 T11 |
| Multilingual Transformer, Dakshina only | test | 63.56 | — | Madhani 2023 T11 |
| IndicXlit (Aksharantar, 11M) | test | 68.10 | — | Madhani 2023 T11 |
| IndicXlit + unigram LM rerank (top-4) | test | **78.53** | — | Madhani 2023 T13 |
| IndicXlit (re-run) | test | 67.97 | 11.7* | Azam 2025 T3 |
| GPT-4o / GPT-4.5 / GPT-4o-FT | test | 70.44 / **76.61** / 72.84 | 10.8* / 9.6* / 10.4* | Azam 2025 T3 |
| Gemma-3-27B / Mistral-Large | test | 46.80 / 49.28 | 17.3* / 17.8* | Azam 2025 T3 |

\* Azam report mean per-word CER (as a fraction; converted to % here), not corpus-level CER; not comparable to Roark/Kirov CER.
Caveats: (i) Roark's "WER" is per attested romanization in the dev lexicon (top-1 acc = 100 − WER). (ii) Aksharantar's "Roark et al." row (65.70) equals 100 − Roark's **dev** WER, compared against IndicXlit **test** — a dev/test mix (*inference* from matching numbers). (iii) Aksharantar's Dakshina-only Transformer (56.04) is ~10 points below Roark's (65.7) for unexplained reasons. Ensure our evaluation script states exactly how multiple references and attestation counts are handled.

### 3.2 Native → Latin (romanization), min-CER over references
Pair 3.3, Transformer 3.1, LSTM 2.8, ByT5 2.5 (Kirov 2024 T4).

### 3.3 Full sentence, Latin → Tamil, WER %
| System | Split | WER | Source |
|---|---|---|---|
| Word-by-word pair6g / Transformer | dev | 30.7 / 31.9 | Roark 2020 T4 |
| Noisy channel (pair6g + trigram) | dev | 19.3 | Roark 2020 T4 |
| Whitespace / full-string Transformer (simulated data) | dev | 18.9 / 19.6 (pass-through) | Roark 2020 T4 |
| Word ensemble → + word-level LM | dev | 27.2 → 17.6 | Kirov 2024 T7 |
| Noisy channel (ensemble + sentence LM) | dev | 15.9 | Kirov 2024 T8 |
| NC + ByT5 + mT5 ensemble | dev / **test** | 14.8 / **14.7** | Kirov 2024 T8/T16 |

### 3.4 Tamil (or closest) under noisy / informal input
| Setting | Result | Source |
|---|---|---|
| 100 hand-noised Tamil words | top-1: IndicXlit 20, GPT-4o 19, GPT-4.5 22, GPT-4o-FT 37 | Azam 2025 T4 |
| Real phone-typed Tamil sentences (proprietary) | WER 26.2 (HMM) → 22.6 (WFST) | Hellsten 2017 T2 |
| Shorthand Tanglish (700 items, mixed Thirukkural/Dakshina) | char acc 93%, word acc 70% (hybrid rules + trigram + trie) | Herath 2024 T3 |
| Malayalam, general vs ad-hoc (vowel-omitted) | CER 7.4 → 22.7; WER 34.5 → 66.9 | Baiju 2024 T2 |

---

## 4. Conflicts in the literature (surface, don't hide)
1. **LSTM vs Transformer on Tamil**: Roark 2020 (LSTM better) vs Kirov 2024 (Transformer better) using nominally the same models and data — difference is within seed noise at 5 runs. Moran 2020 (Transformer better) confounds parameters. Wu 2021 shows batch-size dependence.
2. **"Dakshina baseline" numbers**: Aksharantar's quoted Roark baseline is dev-set; its own Dakshina-only model is far worse than Roark's.
3. **Azam 2025** abstract vs introduction disagree on whether LLMs beat IndicXlit.
4. **IndoNLP 2025** prose swaps CER/WER for the Malayalam system; Baiju 2024 confirms the table.
5. **Kirov 2024 headline**: Google Research page says 4.8% absolute / 27.1% relative WER reduction; the published paper says 3.3% / 18.6% (search snippets; the PDF read here says 3.3% / 18.6%).

## 5. Open gaps (what nobody has done, as far as I could find)
1. **No controlled robustness benchmark for Tamil romanized→native**: no paired clean/noisy versions of the same test words, no noise taxonomy with severity levels, no per-phenomenon breakdown. Closest: IndoNLP-2025 (no Tamil, unspecified augmentation), Azam 2025 (n = 100, unpaired), TAMZHI (no neural models, tiny test).
2. **No public test set of naturally typed (WhatsApp-style) Tanglish with native-script references.** TamilMixSentiment has the text but no references; Hellsten's set is proprietary.
3. **Architecture question unresolved** under matched parameters / tuning budget, and **never examined under noise**.
4. **Variation-aware augmentation for transliteration** (sampled back-transliteration, phonological noise) is untested at word level for Tamil; Benton 2025 shows it for LID; Baiju 2024 proposes it as future work.
5. **Does LM reranking / lexicon constraint recover noisy-input errors?** All reported rerank gains are on clean input.
6. **Accuracy–size–latency trade-off** for neural Tamil transliteration is unreported.
7. **Target-register mismatch**: Tanglish is colloquial Tamil, Dakshina references are literary Wikipedia Tamil; no paper addresses evaluation when the intended native form is colloquial.
8. **Label noise** in the Dakshina Tamil lexicon is documented (Kirov App. B) but its effect on small models is reported only as "robust"; not studied for noisy-input generalisation.

## 6. Metric recommendations (from the corpus)
Report, on Dakshina Tamil test (and dev for comparison with Roark/Kirov): top-1 accuracy (exact match against any attested reference, NEWS ACC definition), top-k accuracy and MRR from the beam (NEWS 2018), corpus CER (Levenshtein over Unicode code points, Kirov Eq. 1), mean ± std over ≥5 seeds (Roark/Kirov; Moran uses 10) with a non-parametric significance test (Moran 2020). For robustness: ΔCER and Δacc between paired clean/noisy inputs per noise type and severity. Optionally EMD k-best CER (Kirov) for variant-distribution quality. Normalise Unicode (NFC) before scoring (Roark 2020 §3.1).
