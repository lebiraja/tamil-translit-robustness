# Vaswani et al. 2017 — Attention Is All You Need

**Citation.** Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin. 2017. "Attention Is All You Need." *NeurIPS (NIPS) 2017*, pp. 5998–6008 (pages as cited by Roark et al. 2020; arXiv:1706.03762v7 PDF used). Read in full.

## Content
Encoder–decoder built only from multi-head **scaled dot-product attention** softmax(QKᵀ/√d_k)V, position-wise FFN, residual + layer norm, sinusoidal positional encodings (learned embeddings gave nearly identical results, Table 3 row E). Base: N = 6, d_model = 512, d_ff = 2048, h = 8, d_k = d_v = 64, P_drop = 0.1, label smoothing ε = 0.1, Adam with warmup_steps = 4000 then inverse-sqrt decay; ~65M params (big: 213M). Beam 4, length penalty α = 0.6, checkpoint averaging. WMT'14 En→De **28.4** BLEU, En→Fr **41.8** (big, 3.5 days on 8 P100s).

## Relevance to us
Defines our "small Transformer" baseline. For character transduction the recipe must be shrunk (Wu et al. 2021: 4 layers, d 256; Roark 2020: d 128, ff 1024, 4 heads, 4 layers; IndicXlit: 6 layers, d 256, 11M params) and its warmup/batch/label-smoothing settings matter (Wu et al. 2021). Self-attention's O(n²) cost is negligible for words (≤~30 chars), so the practical cost difference vs LSTM is parallelism and parameter count, not sequence length.
