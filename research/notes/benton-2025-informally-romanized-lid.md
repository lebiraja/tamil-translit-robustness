# Benton, Gutkin, Kirov, Roark 2025 — Improving Informally Romanized Language Identification

**Citation.** Adrian Benton, Alexander Gutkin, Christo Kirov, Brian Roark. 2025. "Improving Informally Romanized Language Identification." arXiv:2504.21540 (v3, Sep 2025; venue not printed on the PDF — I did not verify publication venue). Read in full (main text; appendices B–F skimmed).

## Problem
Romanized LID for 20 Indic languages (Bhasha-Abhijnaanam): the provided synthetic training data (IndicXlit 1-best romanization) romanizes every word identically, so it lacks the spelling variation of human romanization.

## Method
Synthesize romanized training text from native-script text with **pair n-gram WFST romanizers** (orders 2–4) trained on Dakshina or Aksharantar lexicons, either 1-best or **sampling from the global 8-best (temperature 1)**; multiple distinctly sampled copies; optionally add harvested natural text (GlotCC, MADLAD-400). Dev set = human-romanized Dakshina sentences (not the synthetic dev set, which "has a critical mismatch with the test set").

## Key facts / results
- Lexicon fertility: Dakshina training lexicons average **2.8 romanizations per word** (1.7–4.2 by language) vs **1.011** for Aksharantar's 18M words over the same 11 languages — Dakshina is the better source of *variation*, Aksharantar of *coverage*.
- 1-best synthesis does not beat the IndicXlit baseline; **sampling gives large gains**, especially for fastText; romanizers trained on Dakshina beat those trained on Aksharantar despite far less data.
- Sampled variation reproduces natural phenomena: "implicit vowel realization, variation in indicating vowel quality, and gemination are some of the most frequent variations".
- Test F1: 74.7 (prior best, pretrained neural) → **85.4** (linear model, synthetic only) → **88.2** (+ harvested GlotCC). >60% relative error reduction. A cheap linear model beats mT5 when training data has realistic variation.

## Relevance to us
- Direct, recent, same-group evidence that **modelling romanization variation in synthetic training data matters more than model capacity**. The analogous experiment for *transliteration* (train Latin→Tamil on native Tamil Wikipedia words romanized by *sampling* a native→Latin model, vs 1-best, vs lexicon-only) is, as far as I found, not reported for word-level Tamil transliteration robustness (Kirov 2024 used sampled simulation only for sentence-level fine-tuning; Roark 2020 showed sampling ≫ Viterbi only for LM). This is a strong candidate novelty.
- Suggests temperature/k as a controllable "variation dial" for a robustness curve.
