# Moran & Lignos 2020 — Effective Architectures for Low Resource Multilingual Named Entity Transliteration

**Citation.** Molly Moran, Constantine Lignos. 2020. "Effective Architectures for Low Resource Multilingual Named Entity Transliteration." *Proc. 3rd Workshop on Technologies for MT of Low Resource Languages (LoResMT 2020)*, pp. 79–86. Read in full.

## Setup
Many(591 languages)-to-English name transliteration on the Biblical names corpus (Wu et al. 2018; 279,192 training pairs, ~472/language). OpenNMT; encoders GRU / LSTM / biLSTM (2 layers, hidden 200) × decoders LSTM-with-attention+input feeding vs Transformer; Transformer enc–dec 4 layers, 8 heads, FFN 1024 (decoder 2048), relative position clipping 2, 90k updates with 10k warmup. ADADELTA, dropout 0.2, batch 64. **10 random seeds per configuration**, checkpoint by dev perplexity, **non-parametric significance testing (Kruskal–Wallis + Dunn's test with Bonferroni)**.

## Results (mean ± sd over 10 seeds)
LSTM decoder: GRU 68.66 ± .25 acc / 17.53 CER; LSTM 71.14 ± .34 / 16.10; biLSTM 71.13 ± .20 / 16.05 (Table 1).
Transformer decoder: LSTM enc 71.49 / 15.65; biLSTM 71.37 / 15.82; **Transformer enc 73.01 ± .10 / 14.73 ± .08**, mean F 93.48 (Table 2) — significantly best (p < 0.05) and **lowest seed variance**. Parameters: GRU ~1.82M, LSTM ~2.18M, biLSTM ~2.02M, Transformer ~5.84M (i.e. the Transformer had ~2.7× the parameters — the comparison is not parameter-matched). Training time on one RTX 2080 Ti: ~26 min (GRU/LSTM) vs ~98 min (Transformer). Transformer encoder handles insertions and substitutions better. Language flags for macrolanguages and Unidecode pre-romanization did not help (Table 4).

## Relevance to us
- A model **methodology template** for our architecture comparison: ≥10 seeds, report mean ± sd, non-parametric tests, error-type analysis (insert/delete/substitute). Our study can improve on it by matching parameter counts and tuning budget (they did not), and by adding the noisy-input axis.
- Contrasts with Roark 2020 (LSTM best on Tamil CER, 5 seeds) — evidence on "which architecture wins" is mixed and setup-dependent.
