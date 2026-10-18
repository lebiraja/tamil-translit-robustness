# Bahdanau, Cho, Bengio 2015 — Neural Machine Translation by Jointly Learning to Align and Translate

**Citation.** Dzmitry Bahdanau, KyungHyun Cho, Yoshua Bengio. 2015. "Neural Machine Translation by Jointly Learning to Align and Translate." *ICLR 2015*. arXiv:1409.0473 (v7). Read in full (main text; appendix architecture details skimmed).

## Content
Removes the fixed-vector bottleneck: BiRNN encoder produces annotations h_j = [→h_j; ←h_j]; at each decoder step i an MLP **alignment model** e_ij = a(s_{i−1}, h_j) is softmax-normalised into α_ij and the context c_i = Σ_j α_ij h_j feeds the GRU decoder (additive attention). Soft alignment is trained jointly, not latent. En→Fr WMT'14 (348M-word selected corpus), 1000 hidden units. BLEU (Table 1, all sentences): RNNencdec-30 13.93, RNNsearch-30 21.50, RNNencdec-50 17.82, RNNsearch-50 26.75, RNNsearch-50* (longer training) 28.45; Moses 33.30 (no-UNK subset: RNNsearch-50* 36.15 vs Moses 35.63). RNNsearch shows no degradation for sentences ≥50 words.

## Relevance to us
Our main recurrent model is a char-level BiLSTM/GRU encoder–decoder with Bahdanau (additive) attention. Transliteration alignments are near-monotonic; the learned α matrix is a free diagnostic (we can visualise roman-letter ↔ Tamil-grapheme alignments, e.g. "zh"→ழ, and check whether noisy inputs break alignment).
