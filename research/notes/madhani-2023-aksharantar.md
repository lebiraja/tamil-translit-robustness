# Madhani et al. 2023 — Aksharantar & IndicXlit

**Citation.** Yash Madhani, Sushane Parthan, Priyanka Bedekar, Gokul NC, Ruchi Khapra, Anoop Kunchukuttan, Pratyush Kumar, Mitesh M. Khapra. 2023. "Aksharantar: Open Indic-language Transliteration datasets and models for the Next Billion Users." *Findings of EMNLP 2023* (arXiv:2205.03018; the arXiv PDF read here carries no venue line — venue taken from the ACL Anthology ID 2023.findings-emnlp.4). Read in full.

## Problem
Few public training/eval sets for romanized→native Indic transliteration; Dakshina covers only frequent Wikipedia words of 12 languages.

## Data
- **Aksharantar**: 26M word pairs (26,345k unique; Table 1), 21 languages, 12 scripts. Sources: existing corpora (mostly Dakshina), Wikidata person/location labels, Samanantar parallel corpus (GIZA++ alignment + Sajjad et al. 2012 unsupervised transliteration mining), IndicCorp monolingual corpora (round-trip model scoring, threshold t = −0.35), plus manual collection (68 annotators, maker–checker on the Karya app, max 4 variants/transliterator + 2/validator, instructed "to avoid frivolous variants, like duplications of vowels").
  - **Tamil**: 3,301k total pairs, of which 3,202k mined from IndicCorp (Table 1); 3,231k train (Table 9).
- Mined-pair quality (human check, 500 pairs/language): avg 89%, min 80% (§3.5). Errors: vowel errors, suffix truncation, named-entity idiosyncrasy.
- **Aksharantar test set** (103k pairs, 19 langs) with sub-sets AK-Freq (frequent), AK-Uni (uniformly sampled across char-LM probability deciles → n-gram diversity), AK-NEF (foreign NEs), AK-NEI (Indian NEs). Tamil: 4,682 pairs. Strict no-overlap with any test/validation set incl. Dakshina, across *all* languages.

## Model (IndicXlit)
Single multilingual char-level Transformer (Fairseq), romanized input + target-language tag token. 6+6 layers, emb 256, FFN 1024, 4 heads, GELU, dropout 0.5, pre-LN + embedding LN; **11M parameters**. Input vocab 28 Roman chars, output vocab 780 Indic chars. Adam (0.9, 0.98), peak lr 1e-3, 4000 warmup, inverse-sqrt, batch 4096 pairs, temperature sampling T = 1.5, 4×A100, ≤50 epochs. Hyperparameter grid (Table 10): emb {128,256,512}, FFN {1024,2048}, layers {4,6,8}, dropout {0.2,0.36,0.5}. Decoding: beam 4; rescoring top-4 with F = α·T + (1−α)·P_unigramLM, α = 0.9.

## Results (top-1 accuracy %)
Dakshina test (Table 11), Tamil: Roark et al. 2020 = 65.70; bilingual model trained on Dakshina only = 56.04; multilingual on Dakshina = 63.56; **IndicXlit = 68.10**; IndicXlit + unigram rerank = **78.53** (Table 13). Average over 12 langs: 51.83 → 60.58 (the "15%" claim). Tamil gets the *smallest* gain of all languages (+4.6) (§7.1).

Aksharantar test, Tamil (Table 12): AK-Freq 73.76, AK-Uni 64.62, AK-NEF 39.00, AK-NEI 44.63, micro-avg 63.99. Named entities hardest; frequent words easiest.

Ablation (Table 15, Dakshina test, Tamil): Dakshina-only 56.04 → +Existing 58.58 → +Wikidata 57.16 → +Samanantar 62.14 → +IndicCorp 67.72 → +Manual 65.78. Dravidian-family model on Tamil 68.64. Unigram rerank α=0.9,k=4: 77.83; k=10: 81.66 (avg gains 12% / 14%). Rerank helps native frequent words, not named entities.

Error analysis (Table 14, 7 langs, not Tamil): vowel errors 45% (short/long vowel confusion 15%), consonant confusion 25% (e.g. ள/ல-type retroflex vs dental lateral confusion reported for Kannada/Telugu), other 15% (acronyms, gemination, valid alternatives).

## Inconsistency to flag (my inference)
The "Roark et al. (2020)" row in Table 11 equals 100 − the **dev-set** transformer WER from Roark Table 2 (e.g. ta 100 − 34.3 = 65.7; bn 100 − 50.6 = 49.4). Roark et al. did not report test-set numbers, so this comparison mixes Roark's dev with IndicXlit's test. Also, the Dakshina-only bilingual Transformer in Aksharantar (56.04 on Tamil) is ~10 points *below* Roark's Transformer (65.7 dev) — the gap is unexplained in the paper.

## Limitations (stated)
"The benchmark … for the most part contains clean words … Data from the real world might be noisy (ungrammatical, mixed scripts, code-mixed, invalid characters, etc.). A better representative benchmark might be useful." Word-level only. Annotators told to avoid "frivolous variants" — so Aksharantar, too, is cleaner than chat text.

## Relevance to us
- Strongest public Dakshina-Tamil number: 68.10 top-1 (78.53 with LM rerank) — but with 3.3M Tamil pairs and 11M params, trained on 4×A100. Our Dakshina-only models should be compared against the 56–66 range, not 68.
- Unigram-LM reranking gives +10 points on Tamil — cheap, reproducible, and a natural component of our system (lexicon/LM-constrained decoding).
- Their own limitations section explicitly names the noisy/informal-input gap we want to target.
