# Sennrich, Haddow, Birch 2016 — Neural Machine Translation of Rare Words with Subword Units (BPE)

**Citation.** Rico Sennrich, Barry Haddow, Alexandra Birch. 2016. "Neural Machine Translation of Rare Words with Subword Units." *Proc. ACL 2016* (venue per standard citation; arXiv:1508.07909v5 PDF used). Read in full.

## Content
Byte-pair encoding adapted to word segmentation: iteratively merge the most frequent adjacent symbol pair (Algorithm 1 gives a minimal Python implementation); independent vs **joint** BPE over source+target vocabularies (joint improves consistency; for En–Ru they transliterate Russian to Latin to learn joint merges). Motivation explicitly includes names "via character copying or transliteration". German corpus stats (Table 1): characters → 550M tokens / 3,000 types / 0 UNK; BPE → 112M tokens / 63,000 types / 0 UNK. WMT'15 En→De/En→Ru: up to +1.1 / +1.3 BLEU over back-off dictionary baseline; gains concentrated on rare and OOV words (unigram F1).

## Relevance to us
- Standard citation for the subword alternative in our **char vs subword** ablation. For single-word transliteration the expected trade-off: BPE shortens sequences (faster) but splits romanized words inconsistently across spelling variants (e.g. "kanakkil" vs "kankl" share few merges), which should hurt noisy-input robustness — consistent with ByT5's findings (Xue et al. 2022). Dakshina itself used single characters for word-level and 32k wordpieces only for sentence-level models (Roark 2020).
- Inference: a joint BPE over Latin+Tamil is not meaningful (disjoint scripts); use separate source/target vocabularies if tested.
