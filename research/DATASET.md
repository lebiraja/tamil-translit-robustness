# Dataset: Google Dakshina (Tamil subset)

Status: verified 2026-10-18 against the official README, the LREC 2020 paper, and direct inspection of the Tamil files. I read those files with HTTP range requests into the official tarball, so I did not download the full archive. Everything stated as "measured" was computed by me from the actual files. Everything stated as "paper" or "README" is quoted or paraphrased from that source. Inference is marked as such. Baseline numbers are in more detail in `notes/roark-2020-dakshina.md`, `notes/madhani-2023-aksharantar.md`, `notes/kirov-2024-context-aware-transliteration.md` and `notes/azam-2025-llm-transliteration-benchmark.md`. This file covers the data.

## 1. Bottom line

- **Use the Tamil romanization lexicon (`ta/lexicons/`) as the primary train/dev/test data for a char-level seq2seq.** Train has 25,000 Tamil words and 68,218 (native, romanized) pairs. Dev and test each have 2,500 words, with 6,827 pairs in dev and 6,864 in test. The splits are word-disjoint and lemma-disjoint.
- **Use the 10,000 romanized Wikipedia sentences (`ta/romanized/`, 5,000 dev and 5,000 test) only for sentence-level evaluation.** There is no human sentence-level *training* data.
- **Key caveat:** the data is Wikipedia Tamil romanized by native speakers on request. No romanization standard was imposed, so the spelling variation is real. However, the content is formal, written, encyclopaedic Tamil, and it was typed carefully, word by word or sentence by sentence. It is **not** organic WhatsApp or social-media "Tanglish". It lacks colloquial spoken forms, vowel-dropping shorthand, Tamil+English morphology mixing and chat-style code-switching. Claims must be scoped as "romanized Tamil (Dakshina)", and a "Tanglish" claim needs a separate real-world test set (see section 8).

## 2. Access, size, licence, citation

| Item | Value | Source |
|---|---|---|
| Download | `https://storage.googleapis.com/gresearch/dakshina/dakshina_dataset_v1.0.tar` | README "Data links" |
| Version / date | v1.0, released 05/27/2020 (only release) | README |
| Size | **2,008,340,480 bytes (1.87 GiB)**, an *uncompressed* tar of all 12 languages. The inner Wikipedia files are gzipped. | measured (HTTP `content-length`) |
| Checksum | MD5 `a560868b1d6702602c4ea4e83794fa26` (GCS `x-goog-hash`, base64 `pWCGix1nAmAsTqToN5T6Jg==`) | measured (HTTP headers) |
| Tamil subtree | 298.6 MB total. Of this, lexicons are 3.3 MB and romanized sentences 19.9 MB. Most of the rest is Wikipedia text. | measured (tar index) |
| Licence | **CC BY-SA 4.0** (dataset). Any redistributed derivative, e.g. cleaned splits, must also be CC BY-SA. The *paper PDF* carries a separate CC BY-NC notice from ELRA. | README "License"; paper p. 2413 header |
| Repo | https://github.com/google-research-datasets/dakshina. When fetched today, the page reported the repo as archived/read-only. I did not verify this beyond that page. | GitHub |
| HF / TFDS | I found no official Hugging Face or TFDS copy of Dakshina-Tamil. Community mirrors exist for other languages, e.g. `vrclc/Dakshina-romanized-ml` for Malayalam. Use the GCS tar. | web search, not exhaustive |

Citation (README bibtex):

```bibtex
@inproceedings{roark-etal-2020-processing,
  title     = "Processing {South} {Asian} Languages Written in the {Latin} Script: the {Dakshina} Dataset",
  author    = "Roark, Brian and Wolf-Sonkin, Lawrence and Kirov, Christo and Mielke, Sabrina J. and
               Johny, Cibu and Demir{\c{s}}ahin, I{\c{s}}in and Hall, Keith",
  booktitle = "Proceedings of The 12th Language Resources and Evaluation Conference (LREC)",
  year      = "2020",
  url       = "https://www.aclweb.org/anthology/2020.lrec-1.294",
  pages     = "2413--2423"
}
```

### Fetching only the Tamil files (~23 MB instead of 1.87 GiB)

The tar is uncompressed, so each member is a contiguous byte range. I computed these offsets by walking the tar headers with range requests. The parsed contents were clean: 0 malformed rows, and all splits matched each other.

| File (under `dakshina_dataset_v1.0/`) | Byte range (`curl -r`) | Bytes |
|---|---|---|
| `ta/lexicons/ta.translit.sampled.train.tsv` | 1319252480-1322024075 | 2,771,596 |
| `ta/lexicons/ta.translit.sampled.dev.tsv` | 1322024960-1322285488 | 260,529 |
| `ta/lexicons/ta.translit.sampled.test.tsv` | 1322286080-1322551609 | 265,530 |
| `ta/romanized/ta.romanized.rejoined.tsv` | 1605396480-1608790816 | 3,394,337 |
| `ta/romanized/ta.romanized.rejoined.dev.native.txt` | 1615184896-1616387954 | 1,203,059 |
| `ta/romanized/ta.romanized.rejoined.dev.roman.txt` | 1601454080-1601932790 | 478,711 |
| `ta/romanized/ta.romanized.rejoined.test.native.txt` | 1616611328-1617836361 | 1,225,034 |
| `ta/romanized/ta.romanized.rejoined.test.roman.txt` | 1611207680-1611695212 | 487,533 |
| `ta/romanized/ta.romanized.rejoined.aligned.cased_nopunct.tsv` | 1601933312-1605395821 | 3,462,510 |
| `ta/romanized/ta.romanized.split.tsv` | 1611696128-1615183999 | 3,487,872 |
| `ta/romanized/ta.romanized.split.validation.edits.txt` | 1616388608-1616610565 | 221,958 |
| `ta/native_script_wikipedia/ta.wiki-filt.train.text.shuf.txt.gz` (optional, for an LM) | 1499789312-1558219990 | 58,430,679 |

Example: `curl -r 1319252480-1322024075 -o ta.translit.sampled.train.tsv <URL>`. If the team prefers fewer moving parts, downloading the full tar (2 GB) once is the safe fallback.

## 3. Directory layout (Tamil)

```
dakshina_dataset_v1.0/ta/
├── lexicons/
│   ├── ta.translit.sampled.train.tsv        # native \t roman \t attestation_count
│   ├── ta.translit.sampled.dev.tsv
│   └── ta.translit.sampled.test.tsv
├── romanized/
│   ├── ta.romanized.rejoined.tsv            # native_sentence \t roman_sentence (10,000 lines)
│   ├── ta.romanized.rejoined.{dev,test}.{native,roman}.txt   # 5,000 + 5,000 line-parallel
│   ├── ta.romanized.rejoined.aligned.tsv    # token-aligned, one token pair per line, </s> separators
│   ├── ta.romanized.rejoined.aligned.cased_nopunct.tsv  # same, roman lower-cased, punctuation removed
│   ├── ta.romanized.split.tsv               # long strings split for annotation (10,088 lines, 7 columns)
│   ├── ta.romanized.split.validation.native.txt   # round-trip re-transcription by 2nd annotators
│   └── ta.romanized.split.validation.edits.txt    # LINE REF SUB DEL INS per split line
└── native_script_wikipedia/                 # Tamil Wikipedia text, split train/valid by page
    ├── ta.wiki-filt.{train,valid}.text.shuf.txt.gz   # one sentence per line (train 58 MB gz)
    ├── ta.wiki-filt.{train,valid}.{text,info}.sorted.tsv.gz
    └── ta.wiki-full.*  (unfiltered text/info, urls, omitted pages/sections)
```

Formats are from the README and were checked by me. Two exceptions:
- **`split.tsv` has 7 tab-separated columns, not the 2 the README describes.** The measured layout is `native, native_word_count, roman, roman_word_count, "", "", ""`. In 211 lines, columns 5–7 are non-empty and hold what look like extra native fragments, e.g. `வுட்சு (உச்சு).`. This is undocumented, and my interpretation is a guess. Use `rejoined.tsv` or the dev/test `.txt` files instead.
- `aligned.cased_nopunct.tsv` has 104,792 lines over 10,000 sentences. 145 lines are not 1:1, meaning several tokens share one line. This matches the README's description.

## 4. Measured statistics (Tamil)

### 4.1 Lexicon (word level), the main training resource

| Split | Native word types | (native, roman) pairs | Distinct roman strings | Romanizations / word (mean, median, max) | Words with only 1 romanization |
|---|---|---|---|---|---|
| train | 25,000 | 68,218 | 66,288 | 2.73, 2, 51 | 6,344 (25.4%) |
| dev | 2,500 | 6,827 | 6,806 | 2.73, 2, 27 | 645 (25.8%) |
| test | 2,500 | 6,864 | 6,833 | 2.75, 2, 28 | 615 (24.6%) |

- These match the paper's Table 1: 25,000 train, 5,000 dev+test, 2.7 entries per type.
- **Splits are disjoint by native word.** The measured overlap is 0 for all three pairs of splits. The paper also states that dev/test words share **no lemma** with train words, using Morfessor FlatCat (§3.2). The test therefore measures generalisation to unseen stems, which is harder than a random split.
- **Attestation count** (column 3) is "the number of times the romanization was elicited from an annotator", "not a frequency of usage" (paper §3.2). Measured: every word has a total of ≥3 attestations, with a mean of 4.27. The most common romanization covers on average 63% of a word's attestations. In 5,703 of 25,000 train words (22.8%), the top two romanizations are tied.
- Roman side: only lowercase `a–z` (26 symbols), with no digits, punctuation or capitals. Native side: 46 distinct code points, all in the Tamil Unicode block. All dev/test native code points occur in train (README). Mean length is 9.1 native code points and 10.1 Latin characters, with a maximum of 26 and 30 respectively (train).
- **Direction matters for ambiguity.** Our task is roman → Tamil. In that direction most inputs have a single reference. Only 29 of 6,833 test roman strings (0.42%) map to more than one native word, and the figure for train is 2.5%. The multiplicity sits on the *input* side: each Tamil word arrives spelled 2–3 different ways. The model must map many spellings to one target, so "multiple references" matters much less here than in Tamil→roman. 330 test roman strings also occur in train, but always paired with a *different* native word, because the native words are disjoint. These are cross-word homographs.
- **Noise.** I ran a heuristic check that flags romanizations whose normalized edit distance to every sibling romanization exceeds 0.6. It flagged 0.35% of train pairs (237), 0.26% of dev and 0.36% of test. Manual inspection of the flagged items shows a mix of real annotation errors, which look like translations or wrong words, and legitimate variants. Short words are false positives. Examples are in section 5. This is a rough lower-bound estimate, not a validated error rate.
- English loanwords are common. The paper notes that the English spelling is "typically the most commonly attested romanization" (§3.2, e.g. `டெம்பிள் temple 3 / tempil 1`). So some inputs are English words that the model must render in Tamil script. Inference: this is the only "code-mixing" in the lexicon.

### 4.2 Romanized sentences (sentence level), evaluation only

| Item | Value |
|---|---|
| Sentences | 10,000 total = **5,000 dev + 5,000 test**. These are random halves of the same pool and are line-parallel. |
| Words / sentence | 9.49 native and 9.49 roman tokens on average. The maximum is 84 tokens. The token count differs between the two sides in 90 sentences. |
| Origin | Random sentences from the Wikipedia *validation* pages, so they are page-disjoint from the Wikipedia training text. They were romanized by native speakers, one romanization per sentence. Sentences of 30 or more tokens were split into halves for annotation and then rejoined (paper §3.3). |
| Annotator instructions | Annotators were told to "write the given sentences as they would if they were writing them in the Latin script". Latin and out-of-block text was passed through. "Beyond this, we provided no specific guidance on romanization strategy" (paper §3.3). |
| Round-trip validation | Second annotators transcribed the romanizations back to Tamil script. **Tamil's CER was 0.04, the lowest of all 12 languages** (paper §3.3). My measurement from `split.validation.edits.txt` is a micro-average of 3.66%. Inference: about 4% character disagreement is the human floor for sentence-level roman→Tamil. |
| Roman side | Mixed case: 5,599 of 10,000 strings contain capitals. It also has punctuation, digits, and a few stray non-ASCII characters (`ñ ḻ · … ”`), plus Tamil characters `ஃ க்` leaked into the *roman* side. |
| Native side | 211 strings contain Latin letters, e.g. `(MLA)`. 1,476 contain ASCII digits. |
| Duplicates | 76 repeated native strings in the 10,000, e.g. boilerplate cricket sentences. **15 native sentences appear in both dev and test.** |
| Misaligned pairs | I found **at least 5 pairs where the romanization belongs to a different sentence**. They appear to be a short run of off-by-one shifts, e.g. the roman for `முகலாய பேரரசு…` sits next to the native of `ஃபுட்பாண்டா…`, with round-trip CER 0.73–0.97 on `split` lines. Example: native `அதே மாதத்தில் தனது முதலாவது தேர்வுப் போட்டியில் …` is paired with roman `Amerikka ulnaattup pork kaalathil, …`, which is the romanization of `அமெரிக்க உள்நாட்டுப் போர்க் காலத்தில் …`. At least one of these is in dev at line 3. In total, 14 split lines have round-trip CER > 0.5 and 193 have CER > 0.2. The pairing is identical in `rejoined.tsv` and the dev/test files, so this comes from the source data, not from file mixing. |

### 4.3 Native Wikipedia text (optional)

Tamil has 1,144.4k training sentences and 26.2k validation sentences, at 9.6 words per sentence (paper Table 1). It is useful for a character or word LM for reranking, or for synthesising extra (roman, native) training pairs by back-transliteration as in Roark §4.3. It is not needed for the core seq2seq.

## 5. Ten example rows (real data, test lexicon `ta.translit.sampled.test.tsv`)

Format: `native \t roman \t attestations`. The first six are consecutive rows from the top of the file. Rows 7–10 come from a random sample with seed 0.

```
ஃபார்ம்	faarm	1
ஃபார்ம்	farm	2
ஃபார்ம்	form	1
ஃபார்ம்	hpaarm	1
ஃபேஸ்	face	3
ஃபேஸ்	pace	2
செய்யப்பட்டவை	seiyappattavai	3
அறிவின்	arivin	3
கேட்டதும்	ketadhum	1
அஇஅதிமுக	aiathimuka	1
```

These show the English-loanword pattern (`farm`, `face`, plus phonetic `hpaarm`), the ambiguity of a target with several spellings, and Tamil-specific conventions such as `dh` for intervocalic த in `ketadhum`.

Noise examples from the same file, which the heuristic flagged and I checked by eye: `நதி → moolam (2)` (*nadhi* means river and *moolam* means source, so this is a wrong word). `வாங்க → pecalam (3)` (not a romanization of *vaanga*). `சாவி → key/kei/qey` (a translation, not a transliteration). `திமுக → dmk (2)` (an acronym, which is realistic Tanglish but impossible to learn character by character).

Sentence-level example (`ta.romanized.rejoined.tsv`, line 1):

```
ரேடியோ அதிர்வெண் முடுக்கிகள், துகள்கள் நேரடியாக முடுக்குகிறது.	Radio athirven mudikkigal, thugalkal neradiyaga mudukukirathu.
```

## 6. Does this represent "Tanglish"?

| Property | Dakshina-ta | Real Tanglish (e.g. TamilMixSentiment / DravidianCodeMix YouTube comments) |
|---|---|---|
| Who typed it | Native-speaker annotators, on request | Ordinary users, spontaneously |
| Romanization standard | None imposed, so the variation is genuine (2.7 spellings per word) | None |
| Register | Written/literary Tamil from Wikipedia: encyclopaedic, named-entity-heavy | Colloquial spoken Tamil (`parthavanga`, `podunga`), particles (`ah`, `da`) |
| Code-mixing | Only English loanwords written in Tamil script, plus Latin pass-through tokens (`Delhi`, `MLA`) | Intra-sentential switching, English words with Tamil suffixes (`sivakarthickku`, `getup set aagala`), abbreviations (`bgm`) |
| Shorthand / vowel dropping | Essentially absent. Annotators wrote full forms, though I did not quantify this. | Common (`Kankl` for கணக்கில், see `notes/herath-2024-tamzhi-shorthand-tamil.md`) |
| Casing / punctuation | Lexicon: lowercase a–z only. Sentences: natural case and punctuation. | Arbitrary |

Sources: Roark et al. 2020 §1, §3.2–3.3, and the measurements above. The right column comes from Chakravarthi et al. 2020 (`notes/chakravarthi-2020-tamil-codemix-sentiment.md`) and Herath & Sumanathilaka 2024.

**Implication for our claim (inference).** The paper itself motivates Dakshina by informal WhatsApp/SMS romanization (§1), but the data is elicited romanization of formal text. We can honestly claim "transliteration of romanized Tamil as typed by native speakers without a standard". We cannot claim "Tanglish/chat transliteration" without evaluating on chat-like input. Bhasha-Abhijnaanam reports that IndicLID scores 95.96% on machine-romanized text versus 80.40% on human-romanized text for the same sentences. That is evidence that synthetic or clean inputs overstate real-world performance (`notes/madhani-2023-bhasha-abhijnaanam-lid.md`).

## 7. Published results on Dakshina Tamil (word level, roman→Tamil)

Details and caveats are in the notes files. Note the dev/test distinction: Roark 2020 reported **dev only**.

| System | Split | CER % | Top-1 acc % | Source |
|---|---|---|---|---|
| Pair 6-gram WFST | dev | 9.3 | 63.2 (WER 36.8) | Roark 2020 Table 2 |
| Char Transformer (small) | dev | 9.4 | 65.7 (WER 34.3) | Roark 2020 Table 2 |
| **BiLSTM + attention seq2seq** | dev | **8.4** | 65.3 (WER 34.7) | Roark 2020 Table 2 |
| Re-implementations (Pair 6g / Transformer / LSTM / ByT5), 25 runs | held-aside 2,500 words | 9.4 / 8.2 / 8.6 / **7.9** | — | Kirov et al. 2024 (CL 50(2)) Table 2 |
| Transformer, Dakshina-only, monolingual | test | — | 56.0 (top-3 75.0, top-5 79.2) | Madhani 2023 (Aksharantar) Tables 4, 13 |
| Transformer, Dakshina-only, multilingual | test | — | 63.5 (top-3 79.8, top-5 83.2) | same |
| IndicXlit (3.2M Tamil pairs, 11M params) | test | — | 68.1 (top-3 82.0, top-5 85.9); 78.5 with unigram-LM rerank | same, Tables 4, 13 and re-ranking table |
| IndicXlit / GPT-4o / GPT-4.5 / GPT-4o-FT | test (n = 6,847) | 11.7 / 10.8 / 9.6 / 10.4 | 67.97 / 70.44 / 76.61 / 72.84 | Azam et al. 2025 (arXiv preprint) Table 3 |

**Conflict to note.** Aksharantar's Table 4 lists "Roark et al. (2020)" Tamil as 65.7 on the *test* set. That value equals 100 − Roark's *dev* transformer WER, so the comparison mixes dev and test (inference, also flagged in `notes/madhani-2023-aksharantar.md`). Azam et al. report 6,847 Tamil test items, while I count 6,864 pairs in the test file. Their filtering is unexplained.

Sentence level (WER %, Tamil): the Roark 2020 dev results (Table 4, whitespace eval) are 30.7 for word-by-word pair 6g, 19.3 for the noisy channel and 18.9 for the full transformer. The best Kirov 2024 dev result is 14.8 (Table 8, ensemble). Kirov 2024 *test* results are 17.3 non-contextual and 14.7 contextual (Table 16). Kirov states that these are the first published test-partition sentence results.

Realistic target for a Dakshina-only char LSTM seq2seq (inference): CER of about 8–10% and top-1 of about 56–66% on the lexicon test.

## 8. Other Tamil romanization data (for robustness / extra training)

| Dataset | Tamil size | Native-script references? | Licence | URL | Notes |
|---|---|---|---|---|---|
| **Aksharantar** (Madhani et al. 2023) | 3,231k train pairs (3,202k mined from IndicCorp), 9k valid, **test 4,682** (AK-Freq 1,467, AK-Uni 1,141, AK-NEF 828, AK-NEI 1,246) | yes (word pairs) | Manual data CC-BY; mined and existing data CC0 (HF card) | https://huggingface.co/datasets/ai4bharat/Aksharantar (`tam.zip`, 97.1 MB, JSON: `unique_identifier, native word, english word, source, score`) | The training data *includes Dakshina* (source field "Dakshina Dataset"). Mined pairs are about 80% accurate for Tamil on human check (paper Table 3). **The released HF `tam_test` is not the paper's test set** (measured from `data/aksharantar-tamil/tam_test.tsv`, 11,499 rows). It holds 6,846 rows with source=Dakshina, which are the Dakshina *test* pairs (6,846 of 6,864), plus AK-Freq 2,608, AK-NEI 1,216 and AK-NEF 829. It has **no AK-Uni**. The paper's Table 1 instead lists AK-Freq 1,467 and AK-Uni 1,141. Overlap of the non-Dakshina rows with Dakshina: for AK-Freq, 0 native words are in Dakshina train and 0 in dev. For AK-NEF, 93 native words are in train and 13 in dev. For AK-NEI, 181 are in train and 11 in dev. These counts were taken without NFC; with NFC on both sides they are NEF 91/12 and NEI 175/11, plus 9 and 11 native words in Dakshina test. 18 NE pairs are identical to Dakshina test pairs. **Use only the 4,653 non-Dakshina rows, minus the overlapping NE words, as a robustness set.** |
| Aksharantar sentence-level test pairs | not checked per language | yes | not stated on the GitHub page | https://github.com/AI4Bharat/IndicXlit/releases/download/v1.0/transliteration-sentence-pairs.json (40.6 MB, all languages) | I have not inspected the Tamil content. |
| **Bhasha-Abhijnaanam** (Madhani, Khapra, Kunchukuttan 2023) | romanized Tamil about 4.8k sentences | yes | CC0 (HF card) | https://huggingface.co/datasets/ai4bharat/Bhasha-Abhijnaanam | **For Tamil this is a filtered copy of the Dakshina test set** (5,001 → 4,802, paper Table 2), so it is *not* independent. My PDF extraction of the paper's Table 1 shows 4,767, which conflicts. |
| TamilMixSentiment (Chakravarthi et al. 2020) | 15,744 YouTube comments (11,335 / 1,260 / 3,149) | **no** | HF card says "unknown". Check the GitHub repo. | https://huggingface.co/datasets/community-datasets/tamilmixsentiment | Real Tanglish: mostly Latin script, code-mixed. It would need our own annotation of Tamil-script targets. |
| DravidianCodeMix (Chakravarthi et al. 2022, LRE) | ~44k Tamil-English comments | **no** | Not confirmed. An HF mirror of the offensive subset states CC BY 4.0. | Zenodo record 4750858 | Superset of the above. It has the same need for annotation. |
| Naamapadam | — | — | — | — | An Indic **NER** dataset, *not* transliteration. Not relevant. |
| Samanantar | — | — | — | — | A translation corpus. Used only as a *mining source* inside Aksharantar. Use Aksharantar rather than re-mining. |
| IndoNLP 2025 shared task | no Tamil | — | — | — | Sinhala, Bengali, Gujarati, Hindi and Malayalam only. Its "ad-hoc typing" test design is a useful template (`notes/sumanathilaka-2025-indonlp-reverse-transliteration.md`). |

I found no public Tamil social-media corpus with Tamil-script references. A small team-annotated real-Tanglish test set is the only way to measure the chat-domain gap directly (inference).

## 9. Recommended evaluation protocol

1. **Splits:** use the official lexicon splits unchanged. Train on `train` and select models and hyper-parameters on `dev`. Evaluate on `test` **once**, at the end. Never re-split randomly by pairs. That would leak words across splits and destroy the lemma-disjointness. If a smaller train set is needed for compute, subsample by native word, keeping all of that word's romanizations.
2. **Training pairs:** use every (roman, native) pair. Roark 2020 repeats each pair as many times as it was attested (§4.2), so attestation weighting is an option to ablate. Lowercase the input, since the lexicon is already lowercase.
3. **Word-level test set:** each of the 6,864 test romanizations is an input, and its native word is the reference. This follows Roark §4.2: "for each romanization in the dev set (ignoring the number of attestations)…".
4. **Metrics:**
   - **Top-1 accuracy**, which equals 100 − word-level WER and is the primary metric (Roark, Aksharantar).
   - **CER** = (S + D + I) / reference Unicode code points. Compute it on NFC-normalized strings, over code points, not grapheme clusters, to be comparable with Roark, and state this explicitly.
   - **Top-k accuracy (k = 3, 5)** from beam search, which is comparable to Aksharantar Table 13.
   - Multiple references: for the 29 test roman strings with more than one valid native word, count a prediction as correct if it matches *any* of them. Report how many items this affects.
   - Report mean ± std over at least 3 seeds. Roark used 5 trials and Kirov used 25.
   - Optional breakdowns: accuracy per native word (macro-average over the 2,500 words); English-loanword-like inputs versus native Tamil words; input length buckets.
5. **Sentence level (optional):** use the 5,000 test sentences. Transliterate token by token with pass-through of non-`a–z` tokens and report WER with Roark's "whitespace" or "pass-through" convention (§4.3.1). Exclude or report separately the misaligned pairs (round-trip CER > 0.5) and the 15 dev/test duplicate sentences.
6. **Robustness:**
   - (a) The Aksharantar Tamil test set: the non-Dakshina rows of the HF release (AK-Freq / NEF / NEI = 4,653), with every row whose NFC native word occurs in *any* Dakshina split removed. That is `data/aksharantar-tamil/tam_test.no_dakshina.tsv`, with **4,335 rows** (4,653 − 115 NEF − 203 NEI; filter by pairs-researcher, arithmetic checked). 183 kept rows share a roman string with Dakshina, but always paired with a different native word, so this is not leakage. Report each subset separately.
   - (b) Paired synthetic noise applied to the Dakshina test inputs: vowel dropping, doubled letters, `zh/l` and `th/t/d` swaps, grounded in the TAMZHI pattern typology.
   - (c) If the team agrees, a small human-annotated real-Tanglish set.
   - Report (a), (b) and (c) separately from the clean test set.

## 10. Unverified / open

- How the 2,500 dev/test words per split were sampled (frequency-stratified or uniform). The paper says only that the words were "sampled from words with frequency > 1".
- How the 211 extra columns in `split.tsv` should be interpreted.
- The exact Tamil count in Bhasha-Abhijnaanam: the paper's Table 1 and Table 2 disagree in my extraction.
- The licence of the TamilMixSentiment and DravidianCodeMix raw comments.
- Resolved: the Aksharantar Tamil test does overlap Dakshina (see §8). Still unexplained: why the HF release has no AK-Uni and an AK-Freq count of 2,608 versus the paper's 1,467. Azam et al.'s n = 6,847 for the Dakshina test probably reflects this HF file (6,846 Dakshina rows); this is an inference.
- The noise estimate in §4.1 is a heuristic, not a manual audit.
