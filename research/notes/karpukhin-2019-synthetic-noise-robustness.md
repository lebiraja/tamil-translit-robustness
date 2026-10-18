# Karpukhin et al. 2019 — Training on Synthetic Noise Improves Robustness to Natural Noise in MT

**Citation.** Vladimir Karpukhin, Omer Levy, Jacob Eisenstein, Marjan Ghazvininejad. 2019. "Training on Synthetic Noise Improves Robustness to Natural Noise in Machine Translation." arXiv:1902.01509 (published at W-NUT 2019 per arXiv listing; venue not printed in this PDF). Read in full.

## Method
Transformer-base NMT (6+6 layers, d 512) with Kim et al. char-CNN source encoder, Fairseq. Training-time synthetic noise, **dynamically resampled each epoch**, per token: 60% clean, 10% each of **deletion, insertion, substitution, swap** (no noise on 1-char tokens; swaps avoid first/last char). Natural noise (Wikipedia edit-log misspellings for De/Fr; corrected essays for Cs) used **only at test**, at token noise probabilities 0 / 6.25 / 25 / 100%.

## Results (Table 2, IWSLT16 BLEU, clean-trained → +synthetic noise)
de-en: clean test 34.20 → 33.53 (−0.67); 100% noise (39.36% tokens actually noised) 12.49 → **23.34 (+10.85)**. fr-en 100%: 11.48 → 19.43 (+7.95). cs-en 100%: 16.64 → 18.91 (+2.27). Recovers ~20% (Cs) to ~50% (De) of BLEU lost to natural noise, with <1 BLEU change on clean.
Ablation (Table 3, de-en): **deletion is by far the most useful noise type, then insertion** — they change character distances/length, which swap/substitution (used by Belinkov & Bisk) do not.
**Negative result**: no gain on MTNT Reddit social-media text — social media variation is "variation in writing style and vocabulary" with high edit distance (e.g. catholique→catho), not random typos.

## Relevance to us
- Directly transferable recipe: a "balanced diet" of char noise at ~40% token rate, resampled online, costs <1 point on clean data. A first baseline for Tanglish robustness.
- Deletion being most valuable aligns with Tanglish's dominant phenomenon (vowel omission: "kankl"), but their MTNT negative result warns that **stylistic/systematic variation needs a linguistically informed noise model**, not random edits — the key motivation for a Tamil-specific phonological noise model as our novelty.
