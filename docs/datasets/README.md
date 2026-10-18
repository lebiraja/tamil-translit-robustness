# Datasets: index and usage rules

Everything under `data/` is gitignored (about 965 MB, 28 folders, downloaded 2026-10-18). Dakshina itself is NOT yet downloaded; fetch only its Tamil files (about 23 MB) with the byte ranges in `research/DATASET.md`.

## Detailed documents
| Document | Covers |
|---|---|
| `research/DATASET.md` | Dakshina v1.0 Tamil: URL, size, license, layout, statistics, quirks, baselines, evaluation protocol |
| `research/DATASET_QUESTIONS.md` | Open dataset decisions (item 11 on Aksharantar overlap is resolved) |
| `pairs-and-text-datasets.md` | Latin-Tamil pair sets, native Tamil text and lexicons, synthetic-pair generators, leakage summary, usage table |
| `informal-tanglish-datasets.md` | Real informal Tanglish and code-mixed corpora, measurements, verdict on public gold |
| `informal-tanglish-measurements.json`, `tanglish_measure.py` | Raw measurement numbers and the script that produced them |
| `pairs_scripts/` | 15 scripts reproducing the pair-set numbers (run with `python -I`) |

## Quick table of what to use for what
| Role | Dataset | Local path | Status |
|---|---|---|---|
| Train and clean test | Dakshina Tamil lexicon (25,000 / 2,500 / 2,500 words) | `data/dakshina-ta/` (to fetch) | primary |
| Independent test | Aksharantar Tamil non-Dakshina rows, 4,335 rows (AK-Freq 2,608, AK-NEI 1,013, AK-NEF 714) | `data/aksharantar-tamil/tam_test.no_dakshina.tsv` | use; report subsets separately |
| Optional extra training (separate condition) | Aksharantar Tamil train (3.23M pairs) | `data/aksharantar-tamil/tam_train.tsv.gz` | lemma-leakage caveat (97.1% of Dakshina test words share a stem prefix) |
| Real informal text for noise calibration | DravidianCodeMix-Tamil (44,020 comments), HopeEDI-Tamil (18,178), Tanglish-Corpus-185k (174,424) | `data/dravidiancodemix-zenodo/`, `data/hopeedi-tamil/`, `data/vishnu-tanglish-corpus-185k/` | calibration only, no gold |
| Real-typing test | our human-typed set (about 1,500 words) | `data/human-typed/` (to create) | the only paired real-typing gold |
| LM, lexicon, rerank (C4) | IndicXlit unigram dictionary (9.48M Tamil types), FineWeb-2 Tamil, IndicCorpV2 Tamil head | `data/indicxlit-wordprob-tamil/`, `data/fineweb2-tamil-sample/`, `data/indiccorpv2-tamil-sample/` | optional; coverage of Dakshina test is 98 to 100% so gains are optimistic |
| Synthetic pairs (A3) | Sangraha-synthetic Tamil (1-best machine romanization, 78.6% match a human variant), IndicXlit indic-to-en model | `data/sangraha-synthetic-tamil-sample/` | after filtering Dakshina dev/test words |
| Small lexicons | Wiktionary (kaikki), Kaniyam word lists, Wikidata names | `data/wiktionary-tamil-kaikki/`, `data/kaniyam-tamil-words/`, `data/wikidata-tamil-names/` | minor; filter Dakshina words first for pairs |

## Do NOT train on
- IndicXlit `transliteration-sentence-pairs.json` (Tamil part is the Dakshina test sentences).
- `gowtham58` Tamil_Thanglish_English (contains 4,919 plus 55 Dakshina test sentences) and its lexicon (a copy of Dakshina train, redundant).
- Mendeley transliteration set (no Tamil-script targets; contains romanized Sinhala labelled as Tamil) and `sanujen` (no Tamil-script targets).
- Any dataset containing Dakshina dev/test words, unless filtered first.
- Duplicate sets: TamilMixSentiment, offenseval_dravidian, Tngarg, IsaacRodgz are copies or subsets of DravidianCodeMix-Tamil; cite DravidianCodeMix once.

## Folder inventory (size, content)
| Folder | Size | What it is |
|---|---|---|
| `aksharantar-tamil` | 165 MB | Aksharantar Tamil train/valid/test (HF), plus our filtered `tam_test.no_dakshina.tsv` |
| `aksharantar-sentence-pairs` | 41 MB | Aksharantar sentence pairs (inspect before use; Tamil part overlaps Dakshina sentences) |
| `indicxlit-wordprob-tamil` | 81 MB | Unigram word probabilities, Tamil member of `word_prob_dicts.zip` |
| `sangraha-synthetic-tamil-sample` | 33 MB | Machine-romanized Tamil documents, row groups 0 to 9 |
| `wiktionary-tamil-kaikki` | 95 MB | Tamil Wiktionary extract |
| `kaniyam-tamil-words` | 149 MB | Tamil word lists with frequency lists |
| `fineweb2-tamil-sample` | 69 MB | Web-register native Tamil sample (`tam_Taml`, test split) |
| `indiccorpv2-tamil-sample` | 200 MB | First 200 MB of IndicCorpV2 Tamil news text |
| `wikidata-tamil-names` | 3.7 MB | Person names, Tamil and English labels (partial: query timed out) |
| `dravidiancodemix-zenodo`, `hf-isaacrodgz-dravidiancodemix`, `hf-tamilmixsentiment`, `tamilmixsentiment-github`, `offenseval-dravidian-tamil`, `tngarg-codemix-tamil-english` | 45 MB, 2.9 MB, 708 KB, 4 KB, 2.6 MB, 1.8 MB | DravidianCodeMix-Tamil and its copies/subsets |
| `hopeedi-tamil` | 1.8 MB | HopeEDI Tamil (independent second YouTube source) |
| `vishnu-tanglish-corpus-185k`, `vishnu-tanglish-sts` | 27 MB, 56 KB | Tanglish-Corpus-185k (weak provenance, internal use), TanglishSTS (authored) |
| `tamhatex-mendeley`, `krishan-tamil-hate-speech` | 3.2 MB, 1.3 MB | Hate-speech sets, mostly Tamil script, little use |
| `entacs-langid` | 19 MB | Token-level language tags (weak gold, no licence) |
| `karky-lyrics-tanglish-tamil` | 2.1 MB | Line-aligned rule-romanized lyrics (not typed, copyright) |
| `gowtham58-ta-tng-en`, `gowtham58-ta-tng-en-lexicon`, `mendeley-transliteration-sentence`, `sanujen-legacy-romanized`, `polyglots-tamil-ner-transliterated` | 2.3 MB, 2.8 MB, 16 MB, 144 KB, 848 KB | Pair sets assessed as Dakshina copies, unusable, or minor probes |
| `kannanrbk-tanglish`, `sharchan-tanglish-and-tamil`, `aafrinaaysha-dravidian-codeswitch` | 704 KB, 3.7 MB, 12 KB | Small authored or synthetic sets, no use |

## Not obtained (and why)
NEWS 2012/2018 En-Ta (provider licence agreements), Brahmi-Net corpus (server returned HTTP 502), OSCAR (manual gating), CC-100 and the full Wikipedia dump (not needed), TAMZHI (unreleased), Hellsten 2017 and Wolf-Sonkin 2019 test sets (proprietary), FIRE 2014/2015 Tamil back-transliteration gold (not public), HASOC and FIRE 2021 (login required).

## Licenses to remember
Dakshina CC BY-SA 4.0 (share-alike for derived releases). DravidianCodeMix and HopeEDI CC BY 4.0. Tanglish-Corpus-185k licence claim is doubtful (internal use only). Karky lyrics are copyrighted (internal sanity checks only). See the two detailed docs for each source.
