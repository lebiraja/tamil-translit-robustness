# Gulcehre et al. 2015 — On Using Monolingual Corpora in Neural Machine Translation (shallow/deep fusion)

**Citation.** Caglar Gulcehre, Orhan Firat, Kelvin Xu, Kyunghyun Cho, Loïc Barrault, Huei-Chi Lin, Fethi Bougares, Holger Schwenk, Yoshua Bengio. 2015. "On Using Monolingual Corpora in Neural Machine Translation." arXiv:1503.03535 (v2, preprint). Read in full.

## Method
Integrate a target-side RNN LM (trained on monolingual data) into attention NMT (Bahdanau et al.):
- **Shallow fusion**: at each beam step rescore candidate next tokens with log p(y_t) = log p_TM(y_t) + β·log p_LM(y_t); β tuned on dev.
- **Deep fusion**: concatenate LM and decoder hidden states into the output layer, with a learned sigmoid **controller gate** on the LM state (bias init −1, gate ≈0.26); fine-tune only output parameters.

## Results
Tr-En (IWSLT'14): deep fusion up to +1.19 BLEU over NMT; overall up to +1.96 over phrase-based baseline. Zh-En chat/SMS: up to +1.59 (deep). De-En / Cs-En (WMT'15, Table 4): shallow +0.02/+0.08 and +0.48/+0.29, deep +0.37/+0.39 and +1.02/+0.47 (test columns as printed: NMT 25.51/23.61 → deep 25.88/24.00 for De-En; 21.47/21.89 → 22.49/22.36 for Cs-En). Gains depend on domain similarity between LM corpus and test domain (Table 5 perplexities); deep fusion more robust to mismatch.

## Relevance to us
- The standard formulation for **LM-constrained/fused decoding**. For transliteration, the analogue is fusing a Tamil character (or wordpiece) LM trained on Dakshina's 1.1M native Tamil sentences into the char seq2seq beam search: score = log p_xlit + β·log p_charLM (+ length normalisation). Cheap and needs no extra parallel data.
- Their domain-mismatch finding mirrors Kirov 2024 (mC4 LM hurts Tamil): the LM must match the target register (Wikipedia Tamil vs colloquial chat Tamil) — a tension for Tanglish where intended outputs are often colloquial.
