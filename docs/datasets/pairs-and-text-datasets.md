# Latin↔Tamil transliteration pairs, native Tamil text and lexicons

Status: verified 2026-10-18 by download and direct inspection. Numbers marked *measured* were computed by me from the local files using the scripts in `docs/datasets/pairs_scripts/`. I ran them with `python -I` in a throwaway venv (huggingface_hub 0.26.2, pyarrow 18.1.0, remotezip 0.12.3, aksharamukha 2.3, indic_transliteration 2.3.69). Licences and provenance are quoted from the source card, paper or README. Inference is marked *inference*. Dakshina itself is in `research/DATASET.md`; informal Tanglish corpora are in `docs/datasets/informal-tanglish-datasets.md`.

All local data lives under `data/` (gitignored). Overlap checks compare **NFC-normalized native words** against the Dakshina Tamil lexicons (train 25,000 / dev 2,500 / test 2,500 words). For those checks I used local copies fetched by byte range from the official tar (`research/DATASET.md` §2).

## 0. Bottom line

1. **Only one independent, human-made word-level test set exists besides Dakshina: the non-Dakshina part of the Aksharantar Tamil test.** The HF `tam_test.json` has 11,499 rows and **contains all 6,864 Dakshina-test pairs**. 6,846 of them carry `source=Dakshina`, and 18 are duplicated inside the NE subsets. After removing every row whose native word appears in any Dakshina split, **4,335 rows / 3,707 words** remain: AK-Freq 2,608, AK-NEI 1,013 and AK-NEF 714. This file is `data/aksharantar-tamil/tam_test.no_dakshina.tsv`. AK-Freq has zero overlap with Dakshina and includes colloquial forms (`தெரிஞ்சவங்களும்`). The HF release has no AK-Uni subset and differs from the paper's counts.
2. **Aksharantar train (3.23M pairs) is word-disjoint from Dakshina dev/test, but it breaks Dakshina's lemma-disjointness.** 97.1% of Dakshina-test words share a near-full stem prefix with some Aksharantar-train word, against 33.7% for Dakshina train (crude proxy, §2.1). Training on it changes the generalisation claim from "unseen stems" to "unseen inflections". If it is used, report it as a separate condition.
3. **Several "other" pair sets are Dakshina in disguise.** IndicXlit `transliteration-sentence-pairs.json` (Tamil) is 4,802 Dakshina test sentences. `gowtham58/Tamil_Thanglish_English_lexicon` is Dakshina train, re-split, with English glosses. `gowtham58/Tamil_Thanglish_English` has 9,839 Dakshina dev+test sentences. **Never train on the last one.**
4. **Machine-made synthetic pairs are available at scale.** Sangraha-synthetic Tamil is doc-aligned native↔romanized text (romanized by a word-mapping lookup seeded from Aksharantar plus IndicXlit; IndicLLMSuite §4.5). It has exactly 1 romanization per word, and that romanization matches a Dakshina human variant for 78.6% of Dakshina-test words. Rule-based romanizers (Aksharamukha ISO/IAST) match a human variant only about 21% of the time. They are poor stand-ins for human typing.
5. **For LM / lexicon work, the IndicXlit unigram dictionary is the best single resource.** It has 9.48M Tamil types with probabilities, and its top 200k types cover 98.7% of Dakshina-test words. This is the dictionary behind Aksharantar's 68.1 → 78.5 rerank. The high coverage also means a lexicon constraint is close to a closed-vocabulary oracle on Dakshina. State this when reporting C4 gains.
6. **Not obtained:** NEWS 2012/2018 En-Ta (provider licence agreements), Brahmi-Net corpus (CFILT server returns HTTP 502), OSCAR (manual gating), CC-100 and the full Tamil Wikipedia dump (not needed, covered by the samples below and Dakshina's own wiki text). Details are in §4.

Disk used by this task: about 0.84 GB (9 folders). The whole `data/` folder, including other agents' folders, is 965 MB, well under the 3 GB budget.

## 1. Method notes

- **Fetching only Tamil.** `word_prob_dicts.zip` is 850 MB, but I streamed only the Tamil member via explicit HTTP ranges with `pairs_scripts/rzip.py`. GitHub's release CDN rejects suffix ranges. For Sangraha I read row groups 0–9 of shard 0 with `HfFileSystem` + pyarrow. For IndicCorpV2 I fetched only the first 200 MB of `ta.txt` (byte range). No HF token was needed: everything here is ungated.
- **Checksums.** Aksharantar `tam.zip` sha256 `d019cffc…eb313a2` and FineWeb-2 parquet `bba0eb72…c96d1` match the HF LFS sha256. No other source publishes checksums. For those I record my own sha256 and verify that every record parsed.
- **Encoding.** Every text file below is UTF-8. Native strings are NFC-normalized before comparison. Romanized sides are lowercased.

## 2. Datasets downloaded

### 2.1 Aksharantar, Tamil (Madhani et al., Findings EMNLP 2023), primary extra pairs + independent test

- **Link:** https://huggingface.co/datasets/ai4bharat/Aksharantar (`tam.zip`)
- **Licence (HF card):** "Manually collected data: CC-BY. Mined dataset (from Samanantar and IndicCorp): CC0. Existing sources: CC0."
- **Local:** `data/aksharantar-tamil/raw/tam.zip` (97.1 MB, sha256 `d019cffcdc2264870a96b8ffaea0b66a3b175c8c7d56c095d9f6dd4bbeb313a2`, matches HF). It is converted to `tam_train.tsv.gz`, `tam_valid.tsv` and `tam_test.tsv`, with columns `native, roman, source, score`. I deleted the extracted 555 MB JSON, which is reproducible from the zip. The derived file is `tam_test.no_dakshina.tsv`.
- **Contents:** JSONL rows of `unique_identifier, native word, english word, source, score`. `score` is present only for IndicCorp-mined rows: a negative value, median −0.074 (*inference*: a mining log-score; it is not documented on the card).

| Split | Rows | Native types | Rom./word | Sources (rows) | Overlap with Dakshina (native words) |
|---|---|---|---|---|---|
| train | 3,230,902 | 3,175,646 | 1.017 | IndicCorp 3,133,651; Dakshina 60,210; Samanantar 34,447; Existing 1,545; AK-Freq 776; Wikidata 273 | train 24,165 (all 60,210 Dakshina-train pairs are inside, from 24,014 words); **dev 0, test 0**; also 0 Dakshina dev/test *roman strings* (*inference*: deliberately decontaminated) |
| valid | 8,824 | 4,497 | 1.96 | Dakshina 4,718; IndicCorp 3,733; Samanantar 355; Wikidata 18 | **all 2,500 Dakshina-dev words / 6,826 pairs**; train 19; test 1 |
| test | 11,499 | 6,493 | 1.77 | Dakshina 6,846; AK-Freq 2,608; AK-NEI 1,216; AK-NEF 829 | **all 2,500 Dakshina-test words / 6,864 pairs**; train 263; dev 23 |

- **Test subsets after decontamination** (`tam_test.no_dakshina.tsv`; rule: `source ≠ Dakshina` and the native word is in no Dakshina split):

| Subset | Rows kept | Words kept | Removed | What it is (paper §4) |
|---|---|---|---|---|
| AK-Freq | 2,608 | 1,999 | 0 (no overlap at all) | frequent IndicCorp words, manually romanized |
| AK-NEI | 1,013 | 1,002 | 203 rows (175 train + 11 dev + 11 test words) | Indian named entities |
| AK-NEF | 714 | 709 | 115 rows (91 + 12 + 9 words) | foreign named entities |
| **Total** | **4,335** | **3,707** | | |

  183 kept rows have a roman string that also occurs in Dakshina, always with a different native word. These are homographs, not leakage. The paper's Tamil test is 4,682 (AK-Freq 1,467, AK-Uni 1,141, AK-NEF 828, AK-NEI 1,246; `research/DATASET.md` §8). The HF file has **no AK-Uni** and 2,608 AK-Freq rows, so it is a different release from the paper's table. data-researcher reached the same counts independently.
- **Lemma leakage proxy** (`aksh2.py`). For each Dakshina-test word I took its first `max(4, len−2)` code points (cap 12) and checked whether that prefix starts any training word. Against Aksharantar train: **2,427/2,500 (97.1%)**. Against Dakshina train: 843/2,500 (33.7%). This is a crude stem proxy, not Morfessor (*inference*). It shows that adding Aksharantar train re-introduces lemmas that Dakshina's split withholds.
- **Examples (measured):**
  ```
  ஜானகிக்குத்தான்	jaanakikkuththaan	AK-Freq   (test)
  தெரிஞ்சவங்களும்	therinjavangalum	AK-Freq   (test; colloquial)
  மேனேஜ்மெண்ட்	management	AK-NEI    (test)
  விண்மணி	vinmani	IndicCorp score −0.141 (train)
  கேமிங்கிறான	kemingiraana	IndicCorp score −0.102 (train)
  ```
- **Known problems:** the mined pairs are about 80% accurate for Tamil on a human check (paper Table 3; `research/notes/madhani-2023-aksharantar.md`). There is about 1 romanization per word (1.017), so the data is not variation-rich. The train file is 97% mined. All roman strings are lowercase a–z (measured; 0 violations).
- **Use in our project:** (a) **held-out robustness test**: `tam_test.no_dakshina.tsv`, reported per subset; AK-Freq is the cleanest. (b) Optional **extra training** condition (Dakshina + Aksharantar train), reported separately because of the lemma leakage above. Optionally filter mined rows by `score`. (c) Never use `tam_valid`/`tam_test` as-is for model selection, because they *are* Dakshina dev/test.

### 2.2 IndicXlit sentence pairs (`transliteration-sentence-pairs.json`), Tamil part = Dakshina test sentences

- **Link:** https://github.com/AI4Bharat/IndicXlit/releases/download/v1.0/transliteration-sentence-pairs.json. The release page states no licence. Dakshina is CC BY-SA 4.0.
- **Local:** `data/aksharantar-sentence-pairs/raw/transliteration-sentence-pairs.json` (40.6 MB, all 20 languages, sha256 `6fa2c65a…feb9`). Tamil is extracted to `data/aksharantar-sentence-pairs/ta_sentence_pairs.tsv` (`id, native, roman`).
- **Measured:** 55,821 sentences in total, **4,802 Tamil**. Every Tamil row has `source = "Dakshina"`. 4,800 of them are verbatim Dakshina sentence-**test** natives, and 40 also match dev (the known dev/test duplicates). There are 4,767 unique natives and 9.9 tokens per sentence. This reproduces Bhasha-Abhijnaanam's filtered count (5,001 → 4,802).
- **Example:** `டாப்ளர் தனது பெயரை கிறிஸ்டியன் டாப்ளர் எனக் கூறிக்கொண்டார். ||| Topler thanathu peyarai Christian Topler enak koorikkondaar.`
- **Use:** none beyond Dakshina. It is **not independent**. Use it only to reproduce IndicXlit's sentence-level evaluation subset.

### 2.3 IndicXlit Tamil word-probability dictionary (unigram LM used for Aksharantar re-ranking)

- **Link:** https://github.com/AI4Bharat/IndicXlit/releases/download/v1.0/word_prob_dicts.zip, member `word_prob_dicts/ta_word_prob_dict.json` (1.04 GB JSON, 104.5 MB compressed). Licence: none stated on the release. *Inference*: it is derived from IndicCorp, whose licence is CC0 for the mined Aksharantar packaging. Treat it as research use and cite Madhani 2023.
- **Local:** `data/indicxlit-wordprob-tamil/ta_word_prob.tsv.gz` (84.5 MB, `word \t prob`, sorted by probability, descending).
- **Measured:** **9,483,041 types**. Probabilities sum to 1.000. The minimum probability of 2.12e-9 implies about 471M tokens (*inference*, assuming count 1 at the floor). All entries are in the Tamil block. 11,150 types start with a dependent vowel sign or virama, which makes them malformed.
- **Coverage of Dakshina words (exact match):**

| Top-N types | Dakshina test | dev | train |
|---|---|---|---|
| 50k | 66.4% | 66.0% | 73.5% |
| 200k | **98.7%** | 98.6% | 99.0% |
| 1M | 100.0% | 99.9% | 100.0% |

- **Head:** `ஒரு 0.00664`, `என்று 0.00649`, `இந்த 0.00632`, `மற்றும் 0.00401`, `என 0.00372`.
- **Use:** word-unigram prior for **beam re-ranking (C4)** and **lexicon-constrained decoding / nearest-lexicon snapping**, which reproduces the Aksharantar 68.10 → 78.53 setting. **Caveat:** at 200k+ types it contains essentially every Dakshina-test word. Any lexicon gain on Dakshina is therefore an upper bound with an in-vocabulary target. Real informal input contains colloquial forms that are likely rarer (*inference*). Report lexicon size and OOV rate together with any gain.

### 2.4 Sangraha-synthetic Tamil (Khan et al. 2024, IndicLLMSuite), doc-aligned machine-romanized text

- **Link:** https://huggingface.co/datasets/ai4bharat/sangraha, `synthetic/tam_Taml/` (64 files, 19.3 GB) and `synthetic/tam_Latn/` (64 files, 12.6 GB). **Licence: CC BY 4.0** (card).
- **Provenance (paper §3.2, §4.5):** English Wikimedia was machine-translated into Tamil, then romanized by Setu-Transliterate. That is a word-replacement pass using "a continuously updating mapping of Indic words to their Roman counterparts", initialised from Aksharantar, with unseen words transliterated by IndicXlit. *Inference*: the target-side Tamil is machine-translated, so it is fluent but MT-flavoured.
- **Local sample:** `data/sangraha-synthetic-tamil-sample/sangraha_synth_tam_shard0_rg0-9.jsonl.gz` (31.9 MB; 10,000 docs; `doc_id, native, roman`; doc_ids asserted equal row by row). It is word-aligned into `word_pairs.tsv.gz` (`native, roman, count`).
- **Measured:** 64,434 lines, **100% token-count aligned**, 2.07M tokens and 188,291 word pairs. There is **exactly 1.000 romanization per native type**, which makes it a deterministic romanizer.
  - Overlap with Dakshina: **63.2% of Dakshina-test words** (1,581) already appear in this 10k-doc sample, along with 66.2% of train and 64.4% of dev.
  - For those words, the romanization equals some Dakshina human variant 78.6% of the time and the *top* human variant 54.6% of the time.
  - Agreement with Aksharantar: 84.9% identical to an Aksharantar-train romanization, 80.3% to valid and 65.2% to test. *Inference*: Aksharantar test/Dakshina-test pairs were probably not in the lookup table, but I cannot rule that out.
- **Examples:** `மற்றும் mattrum 50206`, `ஒரு oru 40128`, `ரஸ்ஸெல் russell 22`, `நழுவுதல் nazhuvuthal 2`, `புராணக்கதையைக் puraanakkathaiyaik 1`. Doc text: `krishna oru inthiya nadigar aavaar, avar mukkiyamaaga malaiyaala thiraiyulakil thoandrugiraar.`
- **Use:** (a) **clean-side source for synthetic sentence pairs** and for back-transliteration-style augmentation: native text plus a machine-romanized input, onto which our noise operators can then be applied. (b) A native-script LM sample. **Leakage:** it contains most Dakshina-test words with near-human romanizations. If it is used for training, filter out all Dakshina dev/test native words, and report it as a separate data condition.
- **Problems:** one romanization per word, so no variation (Benton 2025's point: 1-best synthetic ≪ k-best). Only 1 of 64 shards was sampled.

### 2.5 Tamil Wiktionary (kaikki.org extract, Wiktextract)

- **Link:** https://kaikki.org/dictionary/Tamil/kaikki.org-dictionary-Tamil.jsonl (last-modified 2026-10-03). **Licence:** Wiktionary content is CC BY-SA 4.0 / GFDL (*inference*: the standard Wiktionary terms; kaikki redistributes it under the same terms).
- **Local:** `data/wiktionary-tamil-kaikki/kaikki.org-dictionary-Tamil.jsonl` (88.9 MB, sha256 `6c34b416…a28b6`; resumed download, all 13,855 lines parse as JSON). Derived files are `tamil_wiktionary_wordlist.txt` (279,592 Tamil-block words) and `headword_romanization.tsv` (10,610 headwords with their Wiktionary romanization).
- **Measured:** 13,855 entries (nouns 8,841, verbs 2,138, names 1,198), 10,650 Tamil headwords and 277,162 inflected forms from the inflection tables. Coverage of Dakshina test is **39.8%** with forms included, and 12.0% for headwords only.
- **Examples:** `அடைக்கலம் aṭaikkalam`, `அடைச்சு aṭaiccu`, `அகரம் akaram`.
- **Use:** (a) a small, **clean, morphologically generated lexicon** for lexicon-snapping ablations (precision over recall). (b) Inflection tables for error analysis. The romanizations follow ISO 15919 with diacritics, a scholarly scheme rather than how people type. Do **not** use them as human-romanization training pairs.

### 2.6 Kaniyam Foundation `all_tamil_words`, word list + per-source frequency lists

- **Link:** https://github.com/KaniyamFoundation/all_tamil_words. **Licence (README): "Public Domain".**
- **Local:** `data/kaniyam-tamil-words/raw/{words_and_frequency.tar.bz2 (sha256 36e34057…94b6), unique_sorted_words.txt.tar.bz2 (sha256 9c4d9d67…c78c)}`, extracted into `words_and_frequency/` (8 CSV-style `word,count` lists) and `unique_sorted_words_in_all_words_20200604-133955.txt`.
- **Measured coverage of Dakshina-test words:**

| List | Types | Dakshina-test coverage | Note |
|---|---|---|---|
| unique_sorted_words (all sources) | 2,576,079 | 89.5% | **not frequency-sorted**; 671 malformed |
| ta_dedup (*inference*: a CC-100/OSCAR-style web dump) | 549,630 | 87.8% | best-ranked list |
| wiki | 273,953 | 82.8% | |
| Dinamalar news 2009–19 | 169,487 | 65.6% | |
| sirukathaigal.com (short stories) | 254,577 | 63.8% | literary, closer to spoken Tamil (*inference*) |
| solvanam | 127,296 | 58.7% | |
| Tamilmurasu | 15,626 | 18.9% | |
| azhiyasudargal, gurunithya | 2,677 / 3,062 | 1.5% / 3.8% | **garbage**: tokenizer split on vowel signs (`கள,35693 டர,14290 அழ,13424`) |

- **Use:** a secondary frequency source. One option is a story/blog-register prior from `sirukathaigal` for colloquial input. The IndicXlit dictionary (§2.3) dominates it for coverage. Drop the two broken lists.

### 2.7 FineWeb-2 Tamil (`tam_Taml`, test split), web-register native LM sample

- **Link:** https://huggingface.co/datasets/HuggingFaceFW/fineweb-2 `data/tam_Taml/test/000_00000.parquet`. **Licence: ODC-By 1.0** (card), with the usual Common Crawl terms.
- **Local:** `data/fineweb2-tamil-sample/tam_Taml_test_000_00000.parquet` (71.5 MB, sha256 `bba0eb72…c96d1`, matches HF LFS).
- **Measured:** 41,100 docs, 110.5M chars, 11.81M Tamil-script tokens and 868,078 types. 84.2% of characters are in the Tamil block, with 0 replacement characters. It covers 99.3% of Dakshina-test words.
- **Example:** `‘ஹலோ கலெக்டர் சாரா… சரக்கு வேணும்… கடை எப்ப திறப்பீங்க?’`. This is colloquial forms in native script, which Dakshina's Wikipedia text lacks.
- **Use:** a **char/word LM in a more informal register** than Dakshina's Wikipedia text, for C4 re-ranking and an LM-domain ablation (Gulcehre 2015: fusion gains depend on LM domain match). The full train split is 9.4 GB and was not fetched.

### 2.8 IndicCorpV2 Tamil (Doddapaneni et al. 2023), first 200 MB, news-register native LM sample

- **Link:** https://huggingface.co/datasets/ai4bharat/IndicCorpV2 `data/ta.txt` (11.79 GB in total). Licence: none stated on the HF card. *Inference*: AI4Bharat released IndicCorp v2 for research, and the Aksharantar card's CC0 claim covers only the mined pairs, so check before redistributing.
- **Local:** `data/indiccorpv2-tamil-sample/ta_head200MB.txt` (bytes 0–209,715,199 of `ta.txt`, fetched in resumed range chunks, with 6 stitch regions byte-compared against the remote, all identical; trimmed to the last full line, 209,712,961 bytes, sha256 `8e3af0d1…bcd5ef`).
- **Measured:** valid UTF-8, with 255,309 non-empty lines (one sentence per line, blank lines between documents), 78.1M chars, 8.30M Tamil-script tokens and 745,575 types. 22 lines contain a literal U+FFFD from the source. It covers 99.6% of Dakshina-test words. Example: `இதுகுறித்து அமெரிக்கன் ஏர்லைன்ஸ், ஒழுங்குமுறை மற்றும் சர்வதேச விவகாரங்களின் துணைத் தலைவர் மோலி வில்கின்சன் கூறுகையில், …`
- **Use:** a news-register LM and the same source IndicXlit's mining used. *Inference*: it is the head of the file, not a random sample, so its topic mix may be skewed.

### 2.9 Wikidata person names (Tamil label ↔ English label)

- **Source:** a SPARQL query on query.wikidata.org on 2026-10-18 for humans (Q5) with citizenship India / Sri Lanka / Singapore / Malaysia, a Tamil label and an English label. **Licence: CC0** (Wikidata).
- **Local:** `data/wikidata-tamil-names/persons_in_ta_lk_sg_my.tsv` (21,974 labels; **partial**, because the query hit the 60 s server timeout and returned a truncated result, from which I removed the stack-trace lines). `person_name_word_pairs.tsv` holds token-aligned word pairs (`native, roman, count`). Only label pairs with equal token counts are included (19,839 labels), giving 17,906 pairs over 15,106 native types.
- **Overlap:** 165 native types are in Dakshina test, 151 in dev and 1,605 in train.
- **Examples:** `சிங் singh 808`, `குமார் kumar 410`, `ரெட்டி reddy 184`, `மாசுகரெங்காசு mascarenhas 1`. Noise: `சுதாகர் betha` (name-order swap) and the label `கால்பந்து வீரர` ("footballer") recorded as a person's name.
- **Use:** a **named-entity probe**: English-spelling input, NEWS-like. It could also supplement AK-NEI. Wrong pairs need filtering, for example by length ratio and agreement with the model's own back-transliteration. These are standard English spellings, not informal romanization.

### 2.10 Pair sets downloaded by the informal-Tanglish agent and documented here

| Dataset (HF id) | Local path | Measured | Overlap / verdict |
|---|---|---|---|
| `gowtham58/Tamil_Thanglish_English_lexicon` (2024; no licence) | `data/gowtham58-ta-tng-en-lexicon/` | train 67,535 rows / 24,938 words (2.71 rom./word); "test" 683 rows | **Every row is a Dakshina-train pair** (67,535/67,535 and 683/683 exact pairs; 0 dev/test). It is Dakshina train with an English-gloss column (`ராமையா raamaiyaa "Rami"`; the glosses are poor). **Redundant**; its "test" is not a test set |
| `gowtham58/Tamil_Thanglish_English` (2024; no licence) | `data/gowtham58-ta-tng-en/` | train 9,804, test 100 sentences (`ta, tng, en`) | train contains **4,920 Dakshina dev + 4,919 test sentences**, and its test contains 47 dev + 55 test. These are Dakshina romanized sentences with an MT English column. **Leaks Dakshina test; do not train on it** |
| `polyglots/Tamil-NER-Transliterated` (2025; no licence) | `data/polyglots-tamil-ner-transliterated/` | 3,068 sentences (Sri Lankan government text), token lists `input`/`transliterated_input` (32 misaligned). 18,126 word pairs / 14,556 words (1.25 rom./word) | 351 native words in Dakshina test, 371 dev, 4,481 train. Romanization equals a Dakshina human variant for 74% of overlapping words (3,861/5,203). Provenance of the romanizer is undocumented (*inference*: machine). Sri Lankan Tamil register (`முகாமையாளர் mugaamaiyaallar`). Minor use: a small out-of-domain *synthetic* probe |
| `sanujen/Legacy-Font-and-Romanized-Tamil-Corpus` (Apache-2.0) | `data/sanujen-legacy-romanized/` | 10,158 train / 2,032 test rows `word,type` | **No native-script targets** (romanized/legacy-font words with a class label: `lighta,1`, `bgm,1`). Not a pair set. Usable only as a list of real romanized tokens |
| Mendeley "Transliteration Sentence Dataset" (38y7g2fcny) | `data/mendeley-transliteration-sentence/transliteration.csv` (16 MB, `text,label`) | first `tamil`-labelled row is romanized **Sinhala** (`mema paryeshanathmaka kruthiya…`). The informal-Tanglish doc found 8/12 sampled `tamil` rows were Sinhala | **No native targets, mislabelled. Do not use** |

## 3. Synthetic-pair generators (tools, not data)

| Tool | Version / licence | Agreement with Dakshina-test humans (2,500 words; after stripping diacritics) | Verdict |
|---|---|---|---|
| Aksharamukha `Tamil→ISO` / `IAST` / `HK` | 2.3, **AGPL-3.0** | any variant 20.8% / 20.8% / 19.0%; top variant 10.8% / 10.8% / 10.2% | Scholarly schemes (`அம்சங்களில் → amcaṅkaḷil`). Using them needs a rewrite layer (c→s/ch, ṅk→ng, ḷ→l, long vowel→doubled). The AGPL matters only if we redistribute code that links it |
| indic_transliteration `sanscript` ITRANS / OPTITRANS | 2.3.69, MIT | 3.5% / 2.9% | Imposes Sanskrit voicing (`அமைத்துத் → amaidhdhudh`). **Unsuitable** |
| IndicXlit Indic→En model (`indicxlit-indic-en-v1.0.zip`, 124.5 MB; `pip install ai4bharat-transliteration`) | MIT (repo) | not measured (not installed: needs fairseq). *Inference*: it is about 79% like Sangraha's romanizations (§2.4), which IndicXlit partly produced | **Best generator**: it supports beam k-best, which allows Benton-2025-style sampled variation. Install in Docker if needed |
| Sangraha mapping (§2.4) | CC BY 4.0 | any variant 78.6%, top 54.6% (1,581 overlapping words) | A ready-made 1-best generator for the words it covers |

*Inference for C2*: a learned romanizer (IndicXlit k-best, or our own Tamil→Latin model trained on Dakshina train) gives far more human-like clean inputs than rule-based schemes. Noise operators should be applied on top of it. Our Tamil→Latin model is lemma-safe; IndicXlit was trained on Aksharantar.

## 4. Checked and not downloaded

| Resource | Finding | Why not |
|---|---|---|
| NEWS 2012 / NEWS 2018 M-EnTa (English→Tamil names) | NEWS 2018 report (Chen et al. 2018, §6): "Some of the datasets for the shared task are available under specific licensing agreements that have to be undertaken directly by the participants from the data providers". The workshop site (workshop.colips.org) did not resolve today. I found no official open mirror | **Licence-gated.** Unofficial GitHub copies were not used. It covers names in standard English spelling, so it is low value for informal input anyway |
| Brahmi-Net mined corpus (Kunchukuttan et al. 2015) | Tamil–English mined pairs are only about 3.5k (Table 1, `research/notes/kunchukuttan-2015-brahminet.md`). `cfilt.iitb.ac.in/brahminet/` returns HTTP 502 | Server down. Tiny and ILCI-domain |
| OSCAR-2301 | HF gating `manual` (needs approval) | Gated. FineWeb-2 + IndicCorpV2 cover the web/news text |
| CulturaX | HF gating `auto` | Not needed; it overlaps with OSCAR/mC4 |
| CC-100 `ta.txt.xz` | 1.38 GB xz at data.statmt.org | Not needed (redundant with FineWeb-2); could be streamed if required |
| Tamil Wikipedia dump / `wikimedia/wikipedia 20231101.ta` | 278 MB bz2 / 266 MB parquet | Dakshina already ships 1.14M filtered Tamil-Wikipedia sentences (`research/DATASET.md` §4.3) |
| Sangraha verified/unverified Tamil | 18.7 GB / 6.0 GB parquet | Not needed beyond the synthetic sample |
| Samanantar (ta) | CC BY-NC 4.0; translation pairs | Only a mining source; Aksharantar already contains its mined pairs (34,447 rows) |
| neechalkaran/Tamil-corpus (Winslow, Fabricius, TVA terminology, Wiktionary CSVs) | No repo licence; the README lists mixed per-source licences, including NC and "unlicenced" | **Licence unclear.** kaikki Wiktionary (§2.5) replaces its Wiktionary CSV |
| Tamil Virtual Academy / Madras University Tamil Lexicon | Website / DSAL browse only, no bulk download found | Not downloadable |
| google/transliteration repo | Apache-2.0, archived; contains ar/ja/ipa only | No Tamil |
| Leipzig Corpora Tamil, HPL isolated-word Tamil (lipitk) | Leipzig is a sentence corpus (CC BY); HPL is handwriting | Not needed / off-task |

## 5. Leakage summary against the Dakshina test (2,500 words / 6,864 pairs)

| Resource | Contains Dakshina-test words? | Safe as training data? |
|---|---|---|
| Aksharantar train | 0 words, 0 roman strings; 97% stem-prefix overlap (proxy) | Yes for word-disjointness, **no** for lemma-disjointness; report separately |
| Aksharantar valid | 1 word | It is Dakshina dev, so do not tune on it *and* on Dakshina dev as if they were separate |
| Aksharantar test | **all of it** | Use only `tam_test.no_dakshina.tsv` |
| IndicXlit sentence pairs (ta) | it **is** the Dakshina sentence test | No |
| gowtham58 sentences | 4,919 + 55 Dakshina-test sentences | **No** |
| gowtham58 lexicon | 0 (Dakshina train copy) | Redundant |
| Sangraha synthetic | 63% of test words in a 10k-doc sample, near-human romanizations | Only after filtering out Dakshina dev+test words |
| polyglots NER | 351 test words | Filter first |
| Wikidata names | 165 test words | Filter first |
| LM / lexicon resources (IndicXlit dict, FineWeb-2, IndicCorpV2, Kaniyam, Wiktionary) | yes, as native words, not as pairs | Fine for an LM/lexicon (this is standard; Madhani 2023 does the same), but **report OOV rates**: coverage is 98–100%, so lexicon results on Dakshina are optimistic |

## 6. Recommended usage

| Resource | Train | Augment (synthetic) | Held-out test | LM / re-rank | Lexicon constraint | Notes |
|---|---|---|---|---|---|---|
| Dakshina lexicon (`research/DATASET.md`) | **primary** | source for noise ops | **primary clean test** | | | baseline |
| Aksharantar `tam_test.no_dakshina.tsv` | | | **yes**: report AK-Freq / AK-NEI / AK-NEF separately | | | only independent human-made word test |
| Aksharantar train | optional separate condition | | | | | lemma leakage; mined, ~80% precision |
| IndicXlit `ta_word_prob` | | | | **yes** (unigram rerank, C4) | **yes** (top-200k) | the strongest prior; optimistic on Dakshina |
| FineWeb-2 Tamil sample | | | | **yes** (informal-register LM) | vocab | ablate against the Wikipedia LM |
| IndicCorpV2 head | | | | yes (news LM) | vocab | head of file, not random |
| Sangraha synthetic sample | after Dakshina dev/test filtering | **yes** (clean romanized source + noise) | | yes | | 1-best machine romanization |
| Wiktionary (kaikki) | | | | | small clean lexicon ablation | ISO romanization ≠ typing |
| Kaniyam lists | | | | secondary | secondary | drop the 2 broken lists |
| Wikidata names | | NE augmentation (filtered) | NE probe (filtered) | | | English spellings, noisy |
| IndicXlit indic→en model | | **best generator** (k-best) | | | | needs fairseq; Docker |
| Aksharamukha | | baseline generator only with a rewrite layer | | | | ~21% human match |
| IndicXlit sentence pairs, gowtham58 ×2, Mendeley, sanujen | | | | | | **do not use** (Dakshina copies / no targets / mislabelled) |
| polyglots NER | | | minor OOD synthetic probe | | | undocumented romanizer |
