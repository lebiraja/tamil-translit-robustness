# Luong, Pham, Manning 2015 — Effective Approaches to Attention-based NMT

**Citation.** Minh-Thang Luong, Hieu Pham, Christopher D. Manning. 2015. "Effective Approaches to Attention-based Neural Machine Translation." *Proc. EMNLP 2015* (venue per standard citation; arXiv:1508.04025v5 PDF used). Read in full.

## Content
Global attention (all source states) with score functions **dot** (h_tᵀh̄_s), **general** (h_tᵀW_a h̄_s), **concat** (v_aᵀ tanh(W_a[h_t; h̄_s])) and location-based; **local attention** over a window [p_t−D, p_t+D], D = 10, with monotonic (local-m) or predictive (local-p, truncated Gaussian) alignment; **input feeding** (feed the attentional vector h̃_t into the next step). WMT'14 En→De: reversing source +1.3 BLEU, dropout +1.4, global attention +2.8, input feeding +1.3, local-p +0.9; ensemble 8 models + unk replacement 23.0 BLEU; WMT'15 En→De ensemble **25.9** BLEU (SOTA then). "dot works well for the global attention and general is better for the local attention"; concat underperformed in their implementation.

## Relevance to us
Dakshina's LSTM baseline uses Luong-style attention (Roark et al. 2020), so to reproduce it we should implement Luong (general/dot) attention; Bahdanau (additive) vs Luong (multiplicative) is a cheap ablation. **Local-m monotonic attention** is linguistically apt for transliteration (monotone alignment) and cheaper — a plausible lightweight variant.
