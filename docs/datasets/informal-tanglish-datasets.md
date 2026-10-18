# Informal Tanglish (romanized Tamil / Tamil-English code-mixed) datasets

Status: verified 2026-10-18 by download and direct inspection. Every number marked *measured* was computed from the local files. Licences and provenance are quoted from the source page (Zenodo, HF card, Mendeley, GitHub). Where I infer, I say so. Pair or lexicon sets (gowtham58, polyglots, mendeley-transliteration-sentence, sanujen, Aksharantar, IndicXlit) are documented by pairs-data-researcher. They are only cross-referenced here.

## 0. Bottom line

- **Real, public, informal Latin-script Tamil exists in quantity**, all scraped YouTube/Reddit comments: DravidianCodeMix-Tamil (44k comments, CC BY 4.0), HopeEDI-Tamil (18k, CC BY 4.0) and Tanglish-Corpus-185k (174k non-DCM comments, scraped June 2026). TamilMixSentiment, offenseval_dravidian, Tngarg and IsaacRodgz are **subsets or copies of DravidianCodeMix** (measured, section 3), so they are not independent.
- **None of them has native-script gold for the romanized text.** I found no public dataset that pairs real informal romanized Tamil with a Tamil-script reference (section 5). The only paired sets are formal/elicited (Dakshina and its derivatives) or rule-generated (karky lyrics). **Our human-typed set (D4) is therefore needed.** These corpora can calibrate and validate the noise model, but they cannot be used for scoring CER.
- Measured on Latin-Tamil tokens, relative to formal Dakshina sentences (section 4): vowel-drop is about 3–5x more frequent (9.5–15% vs 3.1%). Vowel-length collapse is about 1.8–3.5x (4–7.6% vs 2.2%). Elongation of 3 or more letters is up to about 9x (0.5–2.6% vs 0.28%). Only about 31–36% of Tamil-origin tokens in the comment corpora match a Dakshina romanization exactly, compared with 49% for Dakshina's own sentences. English makes up about 30–42% of word tokens.

## 1. Measurement method (applies to all numbers below)

Script: `docs/datasets/tanglish_measure.py`, run with `python -I tanglish_measure.py data/ <dakshina-lexicon-dir> <ta.romanized.rejoined.tsv> out.json` in a throwaway venv (pandas 2.2.3, pyarrow 18.1.0, wordfreq 3.1.1). Raw output: `docs/datasets/informal-tanglish-measurements.json`. This is a heuristic measurement, not a trained model.

- **Tokens:** Tamil-block runs, Latin alphabetic runs, digit/alnum runs. Shares are over word tokens; numbers are excluded.
- **Latin LID cascade:**
  1. A forced Tamil list of about 70 short function words that collide with English strings (`da, la, na, ku, nu, ah, oru, illa, enna, vera, semma…`).
  2. English if wordfreq Zipf ≥ 4.0.
  3. Tamil if the token is in the romanized lexicon. This is the Dakshina roman side plus the Aksharantar roman side (Dakshina/IndicCorp/AK-Freq/Existing sources, 3.12M types).
  4. English if Zipf ≥ 3.0.
  5. Otherwise a char 2–4-gram naive Bayes. It is trained on 40k English wordfreq words and on Dakshina+Aksharantar roman types.
- **Validation:** against the EnTaCs manual token tags (3,259 en/ta tokens, section 2.9), agreement is **92.2%**. Gold ta→pred en: 206. Gold en→pred ta: 47. Tamil recall is about 90%, so **Latin-Tamil shares are a lower bound and English shares are slightly inflated.** Typical misses are Tamil words that are also English strings: `pole, same, Sari, Ella, than, mass`. The same cascade labels 6.9% of formal Dakshina tokens as English, and most of these are false positives. Caveat: the EnTaCs annotator states they are not Tamil-proficient.
- **Pattern classes:** computed on Latin-Tamil tokens, after squeezing runs of 3 or more to 2. A token is matched only against the **Dakshina roman lexicon** (79,221 human romanizations), and **directionally**: the observed token must be shorter than the lexicon form. The classes are checked in this order:
  - `vowel_length_collapse`: equal after collapsing vowel runs (`kanum`←`kaanum`).
  - `geminate_collapse`: equal after collapsing consonant runs (`iruku`←`irukku`).
  - `length+geminate_collapse`.
  - `h_drop`: equal after removing post-consonant `h` (`Setupati`←`sethupathi`).
  - `vowel_drop`: same consonant skeleton, fewer vowel nuclei, subsequence (`apdi`←`appadi`, `vanth`←`vantha`).
  - `in_aksharantar_only`.
  - `oov_other`.

  Independently, the script flags `elongation_3plus`, `all_caps` and `no_vowel`.
- **Known errors:** the vowel-drop matcher has false positives on short tokens (`kila`←`akila`, `pls`←`pelas`, `nu`←`anu`). Colloquial forms (`pannunga`, `irundhuchu`) are absent from the literary Dakshina lexicon and fall into `oov_other`. Treat the class rates as **relative indicators against the Dakshina baseline**, not as absolute noise probabilities. A hand-audited sample (e.g. 300 tokens) would be needed before quoting them as noise-model parameters in the paper.

## 2. Datasets (informal / code-mixed)

Local root: `/home/lebi/Projects/sem5/deeplearning/data/` (gitignored). Total `data/` = 745 MB including other agents' sets. My downloads are under 60 MB. All files are UTF-8; `file` and pandas parsed every file without decode errors.

### 2.1 DravidianCodeMix-Tamil (Chakravarthi et al., LRE 2022), primary real Tanglish source
- **Link:** https://zenodo.org/records/4750858 (`DravidianCodeMix-2020.zip`, 10.8 MB, open access). **Licence: CC BY 4.0** (Zenodo metadata). Paper: arXiv 2106.09460.
- **Local:** `data/dravidiancodemix-zenodo/DravidianCodeMix/tamil_{sentiment,offensive}_full{,_train,_dev,_test}.csv`. The Malayalam and Kannada files are also present but unused.
- **Content:** YouTube movie-trailer comments, with sentiment labels (Positive/Negative/Mixed_feelings/unknown_state/not-Tamil) and offensive labels (6 classes). This is the same data as FIRE 2021 Dravidian-CodeMix sentiment. The task site gives 35,657/3,963/4,403 and says the full data needs CodaLab registration, but the Zenodo copy is open.
- **Counts (measured):** `tamil_sentiment_full.csv` has 44,020 parsed rows (141 blank lines) and 43,563 unique texts. The offensive file has 43,458 unique texts, and 43,290 texts appear in both. **Format quirks:** `full.csv` is `label\ttext`, `_train.csv` is `text\tlabel`, and the sentiment dev/test files are `;`-separated.
- **Script/LID (measured):** 80.8% of comments are Latin-only, 14.5% Tamil-script-only and 4.5% mixed. Word tokens: Latin-Tamil 45.6%, Latin-English 29.7%, Tamil script 24.1%, alnum 0.6%. On Latin text only, Tamil:English is about 61:39. This agrees with EnTaCs, which reports 62.8% Tamil and 30.2% English tokens on its romanized subset.
- **Examples (seed 0, `label text`):**
  ```
  Positive  Enna Acting da en Thalaivan SURIYAAAAA
  unknown_state  Paaahhhh Yuvan BGM than trailer la theeikuthu nu soldravanga like podunga evlo per nu paapom
  Positive  Tirunelveli slang..kekrapa evlo alaga iruku
  Positive  Handsome Hunk Surya
  not-Tamil  Lalettan fans ഇവടെ come on
  Positive  Hip Hop Tamizha வின் மூன்றாவது திரைப்படம்.அருமையாக உள்ளது ட்ரெயிலர்...
  Negative  Engada nivetha pethuraj.. Oru scene la matu potu emathitinga..
  Mixed_feelings  Saathi veri pudichu alaiyiringaleda en saadhi dhan perusu nu trainlayo bus la vizhunthu ...
  Positive  lovely bro.. vijay anna.. love u anna. semaaaaaaaaaaaaaaa
  unknown_state  Keke beke short film ah mothhama copy adichu oru full flim ah eduthu vechirukingale da...
  ```
- **Use for us:** the main **noise-calibration** corpus (pattern rates in section 4) and the source pool for an optional colloquial probe (NOVELTY C8). It has no native targets.
- **Limitations:** one domain (2019 film trailers). Fan names dominate the frequent tokens (`thala, surya, vijay, rajini`). Some rows are not Tamil (Malayalam, Hindi, French). The sentiment labels are irrelevant to us.
- **Ethics:** public YouTube comments with usernames sometimes embedded in the text. There is profanity and caste/communal content. Do not redistribute raw comments in the paper, only short quoted tokens. Cite the LRE paper.

### 2.2 TamilMixSentiment (Chakravarthi et al., SLTU-CCURL 2020), subset of 2.1
- **Link:** https://huggingface.co/datasets/community-datasets/tamilmixsentiment (parquet). GitHub `bharathichezhiyan/TamilMixSentiment` holds only a README and code. Its README points to the FIRE 2020 Drive files and Zenodo 4015253 "by emailing author". **Licence:** the HF card says "unknown". Inference: the superset 2.1 is CC BY 4.0.
- **Local:** `data/hf-tamilmixsentiment/` (708 KB) and `data/tamilmixsentiment-github/README.md`.
- **Counts (measured):** 11,335/1,260/3,149 = 15,744 rows and 15,546 unique texts. **100.0% of the unique texts occur in DravidianCodeMix-Tamil.** 99.0% of comments are Latin-only. Word tokens: Latin-Tamil 58.5%, English 40.5%, Tamil script 0.2%. The 2020 release filtered out Tamil-script comments; inference from the measured 0.2%.
- **Use / limits:** the same as 2.1. Use 2.1 instead and do not count both. It is convenient as a Latin-only slice.

### 2.3 offenseval_dravidian (Tamil), IsaacRodgz/DravidianCodeMix-Dataset, Tngarg/Codemix_tamil_english, all copies
- `community-datasets/offenseval_dravidian` (tamil config, **CC BY 4.0** per card; DravidianLangTech-EACL 2021 offensive task) has 35,139 train + 4,388 val. **100% of its unique texts are in DCM-offensive.** Local: `data/offenseval-dravidian-tamil/`.
- `IsaacRodgz/DravidianCodeMix-Dataset` (no card) has 43,919 rows, which are DCM-offensive train/dev/test (100% overlap). Local: `data/hf-isaacrodgz-dravidiancodemix/`.
- `Tngarg/Codemix_tamil_english` (licence "other", no card) has 26,102 rows and 15,546 unique texts, i.e. **TamilMixSentiment with duplicates** (100% overlap). Local: `data/tngarg-codemix-tamil-english/`.
- **Use:** none beyond 2.1. They are kept only so the overlap is documented.

### 2.4 HopeEDI-Tamil (Chakravarthi, PEOPLES 2020; LT-EDI 2021 hope-speech task), independent second YouTube source
- **Link:** HF loader `dravidianlangtech/hope_edi`. Its data lives on Google Drive (ids from the loader; anonymous download worked). **Licence: CC BY 4.0** (loader `_LICENSE`).
- **Local:** `data/hopeedi-tamil/tamil_hope_first_{train,dev}.csv` (`text\tlabel\t`). 16,160 + 2,018 = 18,178 rows and 17,156 unique texts. **0% overlap with DCM** (measured).
- **Content:** 2020 YouTube comments on social topics (COVID, the TikTok/China-app ban, Madan's channel). Labels: Hope_speech / Non_hope_speech / not-Tamil.
- **Script/LID (measured):** 84.1% of comments are Latin-only, 8.4% Tamil-only and 7.5% mixed. Word tokens: Latin-Tamil 41.6%, English 37.6%, Tamil script 20.4%.
- **Examples:**
  ```
  Ennadhu idha pathi entha newsumae varala	Hope_speech
  China ku sooru podalam 1st india la irukara 80% of middle class & poverty la kastapadaravangaliku podunga 1st	Non_hope_speech
  Ne video podura YouTube Kuda China app tah	Non_hope_speech
  Tna tan indian tiktok	not-Tamil
  Bro ethuvum vena uc is my best	Non_hope_speech
  Yaga college la kuda vaccination nu potagala	Non_hope_speech
  Thalaivare..neengale inum one plus mobile vachurukinga...adha udachurunga	Non_hope_speech
  Annee varanda thondai.. corona virus affect pannum.. neenga pathukonga. Pause koduth pasuga anne.	Hope_speech
  சீனா பெரிய ஆப்பு இல்லை இந்தியா அமெரிக்கா வைச்ச செம ஆப்பு....	Non_hope_speech
  இன்னாயோட 2020-க்கு (1) ஃபர்ஸ்ட் ஹாஃப் முடியுது...nநாளைருந்து (2) செகண்ட் ஹாஃப் க்கு ரெடி பண்ணிடானுக...	Non_hope_speech
  ```
- **Use:** a **second, domain-different calibration corpus**, to check that pattern rates are not a film-fan artefact. It shows the highest vowel-drop rate of the labelled sets (13.4%).
- **Limits / ethics:** some `not-Tamil` labels are wrong (`Tna tan indian tiktok`). There are `@user` mentions, and literal `n` artefacts from stripped newlines (`...nநாளை`). The ethics note from 2.1 applies.

### 2.5 Tanglish-Corpus-185k (vishnu-n, HF, 2026), largest, most recent, weakest provenance
- **Link:** https://huggingface.co/datasets/vishnu-n/Tanglish-Corpus-185k (`tanglish_corpus.jsonl`, 27.9 MB). The card claims **CC BY 4.0**, but the uploader scraped third-party comments; see ethics.
- **Local:** `data/vishnu-tanglish-corpus-185k/`. **Counts (measured):** 185,973 rows. Sources are youtube 174,331 (5,863 distinct video ids), dravidiancodemix 11,549 and reddit 93. **92.6% of the `dravidiancodemix` rows match DCM** (the rest are presumably normalised copies; inference). The non-DCM rows have 0% overlap with DCM. Below I use only the 174,424 non-DCM rows.
- **Construction (card):** YouTube comments from about 11 channels (cooking, cricket, tech, news) plus r/TamilNaduDiscussion, "scraped June 2026". The card says rows were *filtered* to Latin script only (more than 10% Tamil Unicode dropped). It also says each kept row had to hit a 1,018-token Tamil lexicon and match at least one of 27 morphological patterns (`-ku`, `-la`, `pannu`, `aagiduchu`, `eh`). It reports a 10.3% yield from 1.8M raw comments.
- **Script/LID (measured):** 100% Latin. Word tokens: Latin-Tamil 57.1%, English 42.2%. This is 1.63M Latin-Tamil tokens, which is ~8x DCM.
- **Examples (source, text):**
  ```
  youtube/qK5b7qurlYI  Nice madan na.. nenga ??? Ila ???? Yesterday na news la oru video pathan athula irunthu enaku entha doubt uh..
  youtube/Vm0-TvkTZBc  Savukku pinnadi police poitu irukanga
  youtube/Zz9Ak_13PJg  Anna ennoda samsung galaxy book 2 pro sethupochu anna. Warranty mudinju 1 month la pochu.
  youtube/3B67M5E-XE0  Bro neenga paaka eraserhead padam hero maari irukinga
  youtube/yRqHeBTsDgU  Gommala like ah paarunga ji
  youtube/vhxvC84tjjM  S24 ultra la orange vandhurichi bro adhukappuram tha iPhone 17 prola kondu vandhanga
  youtube/Ako4XU95SIM  Ethana peruku aavara add varadhu kadupa irku
  youtube/EOqz7Rxk8Uo  Spider-Man Brand New Day paakanum na, indha padam lam paakanum. All MCU Spider-Man movies must paakanum
  youtube/hU05D2E5IFk  Ivan panra alla video kum only like mattum dhaan vardhu people innum thirundhala
  youtube/umktkdW4d24  A2d paththi nee sollum bodhu rendu pearaiyum subscribe panni vachu irukka Naa enna pannuvean bro
  ```
- **Use:** the best **large-scale calibration** corpus, because it is recent, multi-domain and phone-typed (`irku`, `vardhu`). It has the highest vowel-drop rate (14.9%). It is also a candidate *unlabelled* pool for back-transliteration ideas, but D2 does not cover that. Report it **separately from DCM**, since the lexicon/pattern filter **biases the sample toward Tamil-dense, suffix-marked comments**. Its Tamil:English ratio is therefore not representative.
- **Limits / ethics:** this is an unpublished single-uploader dataset with no paper. The CC BY 4.0 claim cannot override YouTube/Reddit terms or the commenters' rights. Inference: use it for internal measurement only, never redistribute it, and quote only individual tokens. The README's showcase sentences ("Bro office ku late ah vanthen…") look authored, not sampled. The actual rows look like real comments, but I did not audit them beyond random samples.

### 2.6 TanglishSTS (vishnu-n, HF, 2026), authored, not organic
- **Link:** https://huggingface.co/datasets/vishnu-n/TanglishSTS. **CC BY 4.0** (card). 325 sentence pairs with 0–5 human similarity scores. Local: `data/vishnu-tanglish-sts/`.
- **Measured:** 0 of 650 sentences occur in Tanglish-Corpus-185k. The sentences look composed for the benchmark (`Naan internship ku select aayiten || Intern role ku en selection confirm aayiduchu || 5`). Word tokens: Latin-Tamil 49%, English 51%.
- **Use:** none for transliteration. It is too small, has no native script and was written by one person (inference).

### 2.7 TamHateX v4 (Mendeley Data, 2026)
- **Link:** https://data.mendeley.com/datasets/rr8s9v3kg9 (version 4). **CC BY 4.0.** Local: `data/tamhatex-mendeley/` holds the final/train/validation/test CSVs and the label dictionary. **SHA-256 checked against `SHA256SUMS.txt`: all four CSVs match.**
- **Content (card):** 5,313 YouTube comments (Sep 2025–Mar 2026), privacy-masked, with 5-level hate annotation by three annotators. It contains "Tamil-script, Romanized Tamil, and Tamil-English code-mixed text".
- **Measured:** 77.0% of comments are Tamil-script-only, 21.2% mixed and **only 1.9% Latin-only**. Word tokens are 94.6% Tamil script, with only 1,461 Latin-Tamil tokens. 0% overlap with DCM.
- **Examples:** `NON-HATE  Sirikathenga pa it's serious harrassment oru ponnu andha edathula irundha epdi react pannuvengalo apdi react pannunga...` and `NON-HATE  Nega ipdiyae iruga bro ,nega marakudathu. gents Ah tha irukanum`. The rest is Tamil script. Several rows are abusive, so I have not reproduced them here.
- **Use:** marginal. Its Tamil-script comments are a source of **colloquial native-script spellings** (`சொல்லுக`, `பண்ணது`), which could guide an annotation guideline for colloquial targets (C8). It is not a romanized resource.
- **Ethics:** sexual, gendered and LGBTQIA+-directed abuse, and caste content. The text is privacy-masked by the authors.

### 2.8 Tamil_Hate_Speech (krishan-CSE, HF, 2024)
- **Link:** https://huggingface.co/datasets/krishan-CSE/Tamil_Hate_Speech. The card says Apache-2.0 and gives **no provenance or paper.** Local: `data/krishan-tamil-hate-speech/`, with train 4,677 (label 0: 3,037, label 1: 1,640) and test 826.
- **Measured:** 54.0% of comments are Tamil-only, 29.0% Latin-only and 16.4% mixed. Word tokens: Tamil script 73.5%, Latin-Tamil 11.6%, English 14.9%. 0.1% overlap with DCM.
- **Use:** none beyond a cross-check. Its source is unknown (Sri Lankan political content suggests a YouTube/Facebook scrape; inference), so it should not be cited as data.

### 2.9 EnTaCs token-level LID tags (Bontempo, arXiv 2603.26587, 2026)
- **Link:** https://github.com/paulbontempo/en-ta-cs. **No licence file** (GitHub API `license: null`), so treat it as research-use and do not redistribute. Local: `data/entacs-langid/` holds `train.conll` and `val.conll` (manual tags, about 3.5k tokens, `en/ta/na`), `langid_predictions.json` (XLM-R tags for 35,650 romanized DCM comments, 19 MB) and `stats.json`.
- **Paper (via arXiv HTML):** one annotator, "not Tamil-proficient", labelled about 3,500 tokens. A fine-tuned xlm-roberta-base reached 93.3% token accuracy, but Tamil F1 was only 0.638. The paper reports a mean of 62.8% Tamil and 30.2% English tokens.
- **Use:** an **independent check of our LID cascade** (92.2% agreement, section 1). It could later give a second estimate of the Tamil:English share. Its gold is weak, which limits it.

### 2.10 karky.in lyrics (Deepakvictor/tanglish-tamil, HF), parallel but rule-generated
- **Link:** https://huggingface.co/datasets/Deepakvictor/tanglish-tamil (`tamengl.csv`; card licence "openrail"; source credited to https://karky.in/). `pavithrasaike/tanglish-tamil` is a re-upload with the same card and file name (not byte-compared). Local: `data/karky-lyrics-tanglish-tamil/`.
- **Measured:** 597 songs, and all 597 have line-aligned Tamil and Tanglish lyric lists (22,694 Tanglish lines). It is **the only line-aligned real-world Latin↔Tamil set here**, but the romanization is a **systematic, case-coded scheme**: `oar urasalil en vaergaL chilirkka`, `chiRidhu keeRavaa`. Uppercase marks retroflex/alveolar consonants, and ஏ is always written `ae` and ஓ `oa`. Inference: it was generated by karky.in's rule-based transliterator or a trained lyricist, not typed informally. Vowel-drop is 3.7% and length-collapse 0.6%, both at or below the Dakshina baseline.
- **Use:** an optional sanity test for "systematic but non-Dakshina" romanization (scheme shift, not noise). It is not an informal probe. **Licence/ethics:** song lyrics are copyrighted, and "openrail" is a model licence that the uploader cannot grant for third-party lyrics. Use internally only and do not redistribute.

### 2.11 Synthetic / instruction sets, checked and rejected
- `kannanrbk/tanglish` (`data/kannanrbk-tanglish/`, 1,648 chat pairs "Translate English to casual Tamil Tanglish"): LLM-style SFT pairs (`Later check panren.`). No provenance or licence. Synthetic.
- `Sharchan/tanglish_and_tamil` (`data/sharchan-tanglish-and-tamil/`, 13,906 rows, 2026): **only 2,000 rows are non-empty**, and the samples are Tamil-script instruction/answer text with a `[Style: …]` tag. No licence. Not romanized, not organic.
- `aafrinaaysha/dravidian-codeswitch` (`data/aafrinaaysha-dravidian-codeswitch/`): 16 + valid utterances, token tags, mixed Tamil/Telugu/Malayalam toy data with Windows audio paths as ids. Unusable.
- The other HF "tanglish/thanglish" repos (about 50, e.g. `HEMASENTHIL/*`, `PA0703/English-to-Thanglish-dataset`, `peteparker456/english-to-tanglish-translation-dataset`) are, judging by names and cards, English→Tanglish translation or chatbot SFT sets. They are mostly tiny and undocumented. I did **not** download them. Inference: they are synthetic and have no native-script gold.
- `vishnu`'s and others' Tanglish **models** (e.g. `vishnuexe/Morgan-Tanglish-v7`) are not datasets.

## 3. Checked but not downloaded (gated, unavailable, out of scope, or overlapping)

| Resource | Finding | Action |
|---|---|---|
| FIRE 2021 Dravidian-CodeMix sentiment (Tamil) | dravidian-codemix.github.io/2021: "To get full data register at Codalab". It is the same comments as 2.1 (35,657/3,963/4,403) | Skipped (login). Use the Zenodo copy (2.1) |
| HASOC-DravidianCodeMix FIRE 2021 (Tamil, Tamil-English offensive) | Data behind CodaLab competition 31146 participation | Skipped (login). Not verified whether it is distinct from 2.1 |
| FIRE 2020 Dravidian-CodeMix | Google Drive links on the task site = TamilMixSentiment | Covered by 2.2 |
| FIRE 2013/2014 transliterated search, FIRE 2015 MSIR subtask 1 | FIRE 2015 overview (MSR PDF, Table 1): Tamil-English word-level language labelling, 342 utterances / 6,000 tokens dev and 25 / 1,036 test. "Unlike last year … we did not ask for the back-transliteration of the Indic words in the native scripts". The 2014 track did require back-transliteration, but I could not confirm 2014 Tamil data. The only public FIRE page (IIT-KGP) hosts **Hindi-English 2013 only** | **Not found publicly.** This is potentially the only historical Tamil informal-roman→native gold; it would need emailing the MSR organisers |
| TAMZHI (Herath & Sumanathilaka 2024) | Its social-media romanized sentences were "manually translated into matching Tamil sentences" (per search snippet of the paper), but no repo or dataset is linked from the paper, ICTer or the author's pages that I found | Not public. Could email the authors |
| Hellsten 2017 / Wolf-Sonkin 2019 typed test sets | Proprietary Google data (`research/notes/hellsten-2017-…`, `wolfsonkin-2019-…`) | Not available |
| Bhasha-Abhijnaanam (Madhani 2023) | Tamil romanized portion is a filtered copy of the Dakshina test sentences (`research/DATASET.md` §8) | Not independent of Dakshina; owned by the pairs/Dakshina docs |
| IndoNLP 2025 reverse-transliteration task | No Tamil (Sinhala, Hindi, Bengali, Gujarati, Malayalam) | n/a |
| Naamapadam | Indic NER in native script, not romanized | n/a |
| Indi-RomCoM (arXiv 2606.30790, 2026) | LLM instruction benchmark with *controlled* code-mixing intensity; whether it includes Tamil was not confirmed | Synthetic-controlled, not organic. Not downloaded |
| Mendeley "Transliteration Sentence Dataset" (38y7g2fcny) | Owned by pairs-data-researcher. Note: in a 12-row random sample of its `tamil` label, 8 rows were **romanized Sinhala** | Do not use as Tamil |
| Kaggle "TamilSentiMix" mirrors | Re-uploads of 2.2; Kaggle needs login | Skipped |
| LT-EDI homophobia/transphobia, DravidianLangTech abusive-comment Tamil-English sets | Same organisers and YouTube source as 2.1/2.4; distribution via CodaLab/Drive on request | Not pursued. Likely small additional calibration value only (inference) |

No HF token was needed: every downloaded set was ungated.

## 4. Measurements: script mix and informal-pattern rates

### 4.1 Token shares (% of word tokens; Latin LID per section 1, Tamil share is a lower bound)

| Dataset | Texts | Word tokens | Latin-Tamil | Latin-English | Tamil script | Latin-only texts |
|---|---|---|---|---|---|---|
| DravidianCodeMix-Tamil | 44,020 | 451,017 | 45.6 | 29.7 | 24.1 | 80.8% |
| TamilMixSentiment (⊂ DCM) | 15,744 | 133,415 | 58.5 | 40.5 | 0.2 | 99.0% |
| HopeEDI-Tamil | 18,178 | 158,415 | 41.6 | 37.6 | 20.4 | 84.1% |
| Tanglish-Corpus-185k (non-DCM) | 174,424 | 2,853,672 | 57.1 | 42.2 | 0 (filtered) | 100% |
| TamHateX v4 | 5,313 | 66,895 | 2.2 | 3.2 | 94.6 | 1.9% |
| Tamil_Hate_Speech (krishan) | 5,503 | 68,991 | 11.6 | 14.9 | 73.5 | 29.0% |
| TanglishSTS (authored) | 650 | 3,914 | 49.0 | 51.0 | 0 | 100% |
| karky lyrics (rule-based) | 22,694 lines | 73,921 | 90.1 | 9.9 | 0 | 100% |
| *Dakshina romanized sentences (formal baseline)* | 10,000 | 93,927 | 92.8 | 6.9* | 0.01 | 100% |

\*Mostly LID false positives on Tamil words (`pala`, `sila`), plus real Latin pass-through (`MLA`, `Delhi`). Read about 5–7 points of every English column as cascade error.

### 4.2 Informal-pattern rates on Latin-Tamil tokens (% of Latin-Tamil tokens)

| Dataset | in Dakshina lex | vowel drop | vowel-length collapse | geminate collapse | len+gem | h-drop | elongation ≥3 | ALL CAPS | no vowel | OOV other |
|---|---|---|---|---|---|---|---|---|---|---|
| DravidianCodeMix-Tamil | 35.7 | 10.3 | 7.1 | 2.5 | 0.4 | 0.4 | 2.4 | 2.1 | 0.6 | 32.0 |
| TamilMixSentiment | 35.3 | 9.8 | 7.6 | 2.6 | 0.3 | 0.5 | 2.6 | 1.9 | 0.3 | 32.3 |
| HopeEDI-Tamil | 30.7 | 13.4 | 5.8 | 2.7 | 0.5 | 0.4 | 0.8 | 0.9 | 0.5 | 34.0 |
| Tanglish-Corpus-185k | 30.9 | 14.9 | 4.6 | 3.7 | 0.5 | 0.4 | 0.5 | 0.4 | 0.5 | 32.8 |
| TamHateX (Latin part) | 45.5 | 9.5 | 4.0 | 1.1 | 0.3 | 0.3 | 1.9 | 1.9 | 1.0 | 26.1 |
| karky lyrics | 42.9 | 3.7 | 0.6 | 1.1 | 0.1 | 0.2 | 0.1 | 0 | 0 | 37.9 |
| *Dakshina sentences (baseline)* | 48.7 | 3.1 | 2.2 | 2.1 | 0.3 | 0.9 | 0.3 | 0.0 | 0 | 30.6 |

The remaining mass is `in_aksharantar_only` (11–13% everywhere). **Reading (inference):**
- Real comments exceed the formal baseline mainly on **vowel drop (×3–5)**, **vowel-length collapse (×1.8–3.5)**, **elongation (×1.7–9)** and **capitalisation**.
- **Geminate collapse is only mildly elevated (×1.2–1.8).** One caveat: colloquial single-consonant spellings (`iruku`) are often absent from Dakshina's literary lexicon, so they end up in `oov_other`. The geminate class is therefore under-counted.
- **h-drop is *lower* than in Dakshina.** This suggests digraph variation (`th/t`, `dh/d`) is a two-way swap, not a deletion, and the noise operator should be symmetric.
- Elongation is domain-dependent: 2.4–2.6% in fan comments versus 0.5% in the 2026 multi-domain corpus.
- `no_vowel` tokens are mostly acronyms and chat abbreviations (`DMK, BGM, pls, jst, tym`). These are a separate operator class from Tamil vowel dropping.

### 4.3 Twenty real Tanglish tokens with their Dakshina-lexicon counterpart

Pairs come from the matcher's samples and were spot-checked by me. Unmatched (`—`) tokens are classed by eye.

| Observed (source) | Dakshina form | Pattern |
|---|---|---|
| `iruku` (TamHateX) | irukku | geminate collapse |
| `unaku` (TMS) | unakku | geminate collapse |
| `inum` (HopeEDI) | innum | geminate collapse |
| `Kanuku` (185k) | kannukku | geminate collapse (×2) |
| `nadakum` (STS) | nadakkum | geminate collapse |
| `kanum` (DCM) | kaanum | vowel-length collapse |
| `vazhga` (DCM) | vaazhga | vowel-length collapse |
| `arumaiyana` (TMS) | arumaiyaana | vowel-length collapse |
| `kidaikkadha` (HopeEDI) | kidaikkaadha | vowel-length collapse |
| `matri` (HopeEDI) | maattri | length + geminate collapse |
| `yaruku` (TamHateX) | yaarukku | length + geminate collapse |
| `apdi` (TamHateX) | appadi | vowel drop + geminate collapse |
| `valrathu` (TamHateX) | valaraathu | vowel drop + length collapse |
| `irku` (185k) | — (irukku) | vowel drop + geminate collapse |
| `Setupati` (DCM) | sethupathi | th→t digraph |
| `koodadu` (DCM) | koodadhu | dh→d digraph |
| `vaazga` (185k) | vaazhga | zh→z digraph |
| `semaaaaaaaaaaaaaaa` (DCM) | — (semma) | elongation + geminate collapse |
| `Vanthuteeeeen` (HopeEDI) | — | elongation (colloquial வந்துட்டேன்) |
| `jst`, `tym`, `pls` (DCM/HopeEDI) | — | English chat abbreviations (no vowels) |

## 5. Is there a public real-informal test set with native-script gold?

**No, as far as I could find.** Search covered HF (about 15 keyword queries), Zenodo, Mendeley, the FIRE/Dravidian-CodeMix/HASOC task pages, ACL Anthology and arXiv up to 2026-10-18.
- Every real informal corpus (2.1–2.8) carries only classification labels.
- Every Latin↔Tamil paired resource is either elicited from formal text (Dakshina; Bhasha-Abhijnaanam = Dakshina test; Aksharantar), rule- or machine-generated (karky lyrics; pair sets documented by pairs-data-researcher), or proprietary (Hellsten 2017, Wolf-Sonkin 2019).
- The two historical candidates are not public: FIRE 2013/2014 back-transliteration gold for Tamil is unconfirmed and unpublished, and TAMZHI's manually translated social-media sentences are unreleased.

Our **human-typed set (D4) is needed** and remains the only way to answer RQ2 with paired gold. A complementary option is a **small annotated colloquial probe**: about 300–500 Latin-Tamil tokens sampled from DCM + HopeEDI + 185k, given Tamil-script targets by the team under a written guideline (C8). It would measure real-domain error even though its targets would be colloquial and partly ambiguous. Licence: DCM and HopeEDI are CC BY 4.0, so releasing token-level annotations with attribution is compatible (inference; quote tokens, not whole comments).

## 6. Recommended usage

| Dataset | Noise calibration | Real test probe | Validate synthetic noise | Error analysis | Notes |
|---|---|---|---|---|---|
| DravidianCodeMix-Tamil (2.1) | **Yes (primary)** | Only via own annotation (C8 pool) | Yes: compare pattern rates of synthetic vs real (section 4.2) | Yes: OOV/colloquial forms | CC BY 4.0; film domain |
| HopeEDI-Tamil (2.4) | **Yes (2nd domain)** | Annotation pool | Yes | Yes | CC BY 4.0; independent of DCM |
| Tanglish-Corpus-185k (2.5) | Yes (large, recent; report separately) | No (licence/provenance) | Yes (distributional) | Token frequency lists | Filter-biased; internal use only |
| TamilMixSentiment / offenseval / Tngarg / IsaacRodgz (2.2–2.3) | No (duplicates of 2.1) | No | No | No | Cite DCM instead |
| TamHateX v4 (2.7) | No (2% Latin) | No | No | Colloquial Tamil-script spellings for the guideline | CC BY 4.0; abusive content |
| krishan Tamil_Hate_Speech (2.8) | No | No | No | No | Unknown provenance |
| EnTaCs tags (2.9) | LID check only | No | No | No | No licence; weak gold |
| karky lyrics (2.10) | No | Optional scheme-shift sanity test (paired) | No | Case-coded scheme vs Dakshina | Copyright; internal only |
| TanglishSTS, kannanrbk, Sharchan, aafrinaaysha (2.6, 2.11) | No | No | No | No | Authored/synthetic |
| **Our human-typed set (D4)** | Yes (per-typist rates) | **Yes (only paired gold)** | **Yes (RQ2)** | Yes | Needed |

Concrete calibration suggestion (inference, to be checked against a hand audit):
- Set the operator *relative* frequencies from the DCM/HopeEDI/185k vs Dakshina excess in section 4.2: vowel drop > vowel-length collapse > elongation ≈ geminate collapse > digraph swap.
- Model digraphs as **symmetric swaps**, not deletions.
- Treat acronyms/abbreviations (`no_vowel`) and English tokens as **pass-through**, outside the Tamil noise model.
