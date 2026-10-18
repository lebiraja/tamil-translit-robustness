# Madhani, Khapra, Kunchukuttan 2023 — Bhasha-Abhijnaanam: Native-script and Romanized LID for 22 Indic Languages

**Citation.** Yash Madhani, Mitesh M. Khapra, Anoop Kunchukuttan. 2023. "Bhasha-Abhijnaanam: Native-script and Romanized Language Identification for 22 Indic Languages." *Proc. ACL 2023 (Volume 2: Short Papers)*, pp. 816–826 (venue as cited in the Aksharantar paper; arXiv:2305.15814v3). Read in full (main text; appendices skimmed).

## Problem / method
LID for 22 Indian languages in native and Roman script. No romanized training corpora exist publicly ("CC-100 has romanized versions for 4 Indian languages, but a manual analysis suggested that it contains a lot of profane content"), so **romanized training data is synthesised** by transliterating native text with IndicXlit (Indic→En). Classifiers: FastText (8-dim) + IndicBERT-v2 fine-tuned, cascaded by confidence threshold 0.6.

## Data facts relevant to us
- Dakshina romanized sentence test sets contain short named-entity / loanword-only sentences; ~7% filtered after manual validation. **Tamil: 5,001 → 4,802 (3.98% filtered)** (Table 2).
- New romanized test sets: annotators given no transliteration guidelines ("free to transliterate in the most natural way").

## Results
Romanized LID: IndicLID-FTR acc 71.49; IndicLID-BERT 80.04; ensemble 80.40 (Table 4). Most confusion for short inputs (<10 words).
**Synthetic vs real gap (Table 5)**: same test sentences machine-romanized by IndicXlit → accuracy **95.96** vs **80.40** on human romanizations (F1 93.43 vs 74.72). "The data characteristics of the synthetic test set are much closer to the training data than the original test set."

## Relevance to us
- Strong citable evidence that **machine-generated romanization is systematically cleaner/more regular than human romanization**, so evaluating on synthetic noise alone will over-estimate robustness. Our robustness study should (a) use a noise model grounded in observed human variation (TAMZHI survey, Wolf-Sonkin typology, Dakshina's multiple attested variants), and (b) include at least a small human-written test set.
- Supports the synthetic-data-generation route (native text → romanizer) for augmentation — but with this caveat.
