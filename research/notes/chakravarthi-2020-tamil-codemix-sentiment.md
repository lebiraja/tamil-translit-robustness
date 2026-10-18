# Chakravarthi et al. 2020 — Corpus Creation for Sentiment Analysis in Code-Mixed Tamil-English Text

**Citation.** Bharathi Raja Chakravarthi, Vigneshwaran Muralidaran, Ruba Priyadharshini, John P. McCrae. 2020. "Corpus Creation for Sentiment Analysis in Code-Mixed Tamil-English Text." arXiv:2006.00206; published at the SLTU–CCURL 2020 workshop (LREC 2020) — venue from the arXiv listing, not printed on this PDF. Read in full (benchmark table skimmed).

## What it is
**TamilMixSentiment**: 15,744 YouTube comments (from 2019 movie trailers) in Tanglish, sentiment-labelled (Positive 10,559; Negative 2,037; Mixed 1,801; Neutral 850; Other language 497). 169,833 tokens, **vocabulary 30,898**, ~10 tokens/post (Tables 2–3). Filtered from 184,573 scraped comments via langdetect (monolingual Tamil/English removed) and a 5–15-word length filter. Splits 11,335 / 1,260 / 3,149. Krippendorff's α 0.6585 (nominal). Repo: github.com/bharathichezhiyan/TamilMixSentiment.

## Characterisation of real Tanglish (quotable)
"Due to their pervasiveness of English online, code-mixed Tamil-English (Tanglish) sentences are often typed in Roman script." Observed inter-sentential, intra-sentential and tag switching; most comments in Roman script with Tamil grammar + English lexicon or vice versa. Examples: "Intha padam vantha piragu yellarum Thala ya kondaduvanga", "Trailer late ah parthavanga like podunga", "Enna bgm da saami", "sivakarthickku hero getup set aagala".

## Results
Sentiment baselines (LR, RF best; micro-avg F ≈ 0.68). Not transliteration.

## Limitations
No native-script references → cannot directly evaluate transliteration; domain is movie-trailer comments; no word-level language tags.

## Relevance to us
- Best open source of **naturally occurring Tanglish** I found. The examples show phenomena absent from Dakshina: English words inside Tamil morphology ("sivakarthickku", "getup set aagala"), colloquial (spoken) Tamil forms ("parthavanga", "podunga", "kondaduvanga") rather than written forms, particles ("ah", "da"), and abbreviations ("bgm", "omg").
- Feasible contribution (inference): sample ~500–1,000 Tamil-origin tokens from this corpus and have the 3 team members (native speakers) annotate native-script targets → a small **real-Tanglish test set** to measure the Dakshina→wild domain gap. Licence of the scraped comments must be checked before redistribution (not verified here).
- Caution: many Tanglish words are *colloquial* Tamil whose "correct" native spelling is itself non-standard (e.g. spoken -nga endings), so references need an annotation guideline (write colloquial form in Tamil script vs normalise to literary Tamil). Dakshina references are literary/Wikipedia Tamil.
