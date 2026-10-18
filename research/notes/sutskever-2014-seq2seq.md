# Sutskever, Vinyals, Le 2014 — Sequence to Sequence Learning with Neural Networks

**Citation.** Ilya Sutskever, Oriol Vinyals, Quoc V. Le. 2014. "Sequence to Sequence Learning with Neural Networks." *NeurIPS (NIPS) 2014*, pp. 3104–3112 (venue/pages as cited by Rosca & Breuel 2016; arXiv:1409.3215v3). Read in full.

## Content
Encoder LSTM maps the input to a fixed vector; decoder LSTM generates the output. WMT'14 En→Fr: 4-layer LSTMs, 1000 cells/layer, 1000-d embeddings, 160k/80k vocab, 384M parameters, 8,000-d sentence state. Ensemble of 5 reversed LSTMs with beam search: **34.81 BLEU** vs SMT baseline 33.30; reranking the SMT 1000-best: 36.5. **Reversing the source** sentence "improved the LSTM's performance markedly" by creating short-term dependencies. Beam size 1 already works well; beam 2 gives most of the benefit.

## Relevance to us
Defines the encoder–decoder framework of our "char-level Seq2Seq" baseline and teacher-forced cross-entropy training; the beam-size observation (small beams suffice) is relevant to on-device latency; source reversal is a cheap ablation for the attention-free variant (Rosca & Breuel 2016 also used it).
