# Kim & Rush 2016 — Sequence-Level Knowledge Distillation

**Citation.** Yoon Kim, Alexander M. Rush. 2016. "Sequence-Level Knowledge Distillation." *Proc. EMNLP 2016* (venue per standard citation; arXiv:1606.07947v4 PDF used). Read in full.

## Content
Word-level KD (match teacher's per-token distribution), **Sequence-level KD (Seq-KD)**: train the student on the teacher's beam-search outputs; Seq-Inter: fine-tune toward the beam candidate closest to the gold. Seq-KD makes the student's distribution peaked so **greedy decoding nearly matches beam search** (argmax mass 16.9% vs 0.9% baseline for 2×500 En→De).
- En→De: student 2×500 LSTM is +4.2 / +1.7 BLEU over a no-KD baseline (greedy / beam).
- Speed (Table 2, words/s, greedy): 4×1000 teacher 425.5 GPU / 15.0 CPU / could not load on phone; 2×500 student 1051.3 / 63.6 / 8.8 on Samsung Galaxy 6.
- Pruning on top (Table 3): 2×500 with 80% weights pruned → 17M params, 19.1 BLEU vs teacher 19.5 (221M), 13× smaller; 90% pruned → 8M, 18.5.

## Relevance to us
Recipe for the "lightweight/on-device" angle: distil a strong teacher (e.g. our best Transformer + LM-reranked system, or IndicXlit outputs on Tamil native text) into a tiny char-BiLSTM, then measure CER/latency/model size and whether robustness to noisy input survives distillation (inference: untested for transliteration as far as I found). Greedy-decoding parity from Seq-KD directly reduces on-device latency.
