# Rosca & Breuel 2016 — Sequence-to-sequence neural network models for transliteration

**Citation.** Mihaela Rosca, Thomas Breuel. 2016. "Sequence-to-sequence neural network models for transliteration." arXiv:1610.09565 (preprint, Google; no venue). Read in full.

## Problem / method
Compares two neural approaches to monotone transduction: (1) **epsilon insertion + CTC** — insert ε symbols into the source (3 per char) so a (bi)LSTM tagged with CTC can emit longer outputs; (2) Bahdanau-style attentional seq2seq (GRU/LSTM, uni/bidirectional encoder, reversed input as in Sutskever 2014). 1,000 random hyperparameter configurations per model family, best on eval set reported on test.

## Data
EN→JA (16,356 pairs), AR→EN (15,898, new Wikipedia-name dataset released), EN→IPA (CMUdict, 123,892). Unicode code points in/out.

## Results (test CER / WER %)
- EN→JA: best EI-CTC 2-layer biLSTM **18.1 / 51.1**; best seq2seq 2-layer GRU 20.2 / 50.2 (Table 2).
- AR→EN: CTC 2-layer biLSTM 22.5 / 78.5; seq2seq 2-layer GRU 22.4 / 77.1 (Table 3).
- EN→IPA: seq2seq ~7.0 / 26.2 vs EI 8.1 / 34.2 (Table 4).
- Conclusion: attentional seq2seq "generally seem[s] to perform better, but not uniformly"; CER and WER "appear to vary independently".
- Error analysis: vowel confusion most common (AR→EN).

## Stated limitations / gaps
Datasets list each pair once regardless of frequency; contain unlearnable exceptions; multiple valid transliterations are scored as errors. Suggests combining network cost with a target-LM cost.

## Relevance to us
- Early evidence that CTC-style monotone models are competitive with attention for transliteration — motivates a CTC (non-autoregressive, fast) variant as a lightweight baseline.
- Their warning that CER and WER move independently → we must report both, plus top-k.
- Hyperparameter search breadth (1,000 configs) is a reminder that architecture comparisons are confounded by tuning budget; we should equalise tuning budget across LSTM and Transformer.
