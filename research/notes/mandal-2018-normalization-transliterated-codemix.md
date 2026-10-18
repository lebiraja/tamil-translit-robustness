# Mandal & Nanmaran 2018 — Normalization of Transliterated Words in Code-Mixed Data Using Seq2Seq & Levenshtein Distance

**Citation.** Soumil Mandal, Karthick Nanmaran. 2018. "Normalization of Transliterated Words in Code-Mixed Data Using Seq2Seq Model & Levenshtein Distance." arXiv:1805.08701 (published at the W-NUT 2018 workshop per its arXiv listing; venue not printed in the PDF). Read in full. **Language pair is Bengali–English, not Tamil** (authors are at SRM, Chennai).

## Problem
Phonetic typing variants of romanized Bengali in code-mixed social media; normalise to a canonical ITRANS form (and thereby back-transliterate).

## Method
1. Rule pre-normalisation: digits → spoken form ("ek" for 1); character elongation >2 trimmed to 2 ("baaaad"→"baad").
2. Char-level seq2seq (stacked LSTM, no attention, latent 128, one-hot input over 26 letters, max length 14, rmsprop lr 1e-3, batch 64, 100 epochs) mapping user spellings → ITRANS, trained on a 6,000-pair parallel lexicon.
3. **Snap to lexicon**: nearest entry (Levenshtein) in a 21,850-word ITRANS dictionary; "modified" LD treats {a,o} and {b,v} as identical.

## Results
Word-level accuracy on 905 test tokens (Table 1): LD only 58.78; LD-modified 61.10; seq2seq + LD 89.72; **seq2seq + LD-modified 90.27**. Seq2seq alone: 51.04%. 92% of remaining errors are OOV (slang, joined words); mean LD of those to the reference 1.89. Downstream sentiment accuracy 80.97 → 82.47 after normalisation.

## Limitations
Tiny data; no attention; closed-vocabulary snapping fails on OOV; Bengali only.

## Relevance to us
- Strong, simple evidence that **lexicon-constrained post-processing** (nearest valid word) converts a weak seq2seq (51%) into a strong system (90%) for noisy romanization — motivates our lexicon/trie-constrained beam search, and a hard vs soft constraint ablation (Tamil's agglutination makes closed vocab risky; cf. Roark 2020's finding that noisy-channel closed-vocab models lose on Tamil/Malayalam).
- Their pre-normalisation rules (elongation trimming) are cheap robustness tricks worth including as a baseline preprocessing step for WhatsApp-style Tanglish ("superrrr", "semmaaaa").
- Phonetically motivated substitution equivalence classes ({a,o}, {b,v}) parallel the Tamil-specific classes we would define (e.g. {l, zh, L}, {n, N}, {t, th, d}).
