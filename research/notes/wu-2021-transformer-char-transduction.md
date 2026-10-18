# Wu, Cotterell, Hulden 2021 — Applying the Transformer to Character-level Transduction

**Citation.** Shijie Wu, Ryan Cotterell, Mans Hulden. 2021. "Applying the Transformer to Character-level Transduction." *Proc. EACL 2021* (main volume). arXiv:2005.10213 (v2, Jan 2021; venue per arXiv comments/ACL Anthology 2021.eacl-main.163 — the PDF itself carries no venue line). Read in full.

## Problem
Transformers had underperformed RNN seq2seq on character-level tasks (inflection, g2p, transliteration, normalisation) with ~10k training examples.

## Method
Small Transformer: 4 enc + 4 dec layers, 4 heads, d_model 256, d_FF 1024, pre-LN, ~7.37M params (excl. embeddings/output layer), greedy decoding. Adam lr 1e-3, inverse-sqrt with 4k warmup, 20k updates, best of 50 checkpoints, **single random seed**. "Feature-invariant" position/type embeddings for feature-guided tasks.

## Key finding
**Batch size is the decisive hyperparameter**: the Transformer only beats the RNN baseline (Wu & Cotterell 2019, 8.66M params) when batch size ≥ 128 (Fig. 1); they use 400 (~4% of a 10k training set). Label smoothing 0.1 and Adam β2 = 0.98 also help slightly (Table 1). Giving the RNN the same LR schedule does not close the gap. Transformer advantage shrinks for longer output words (Fig. 3).

## Results
- Morph. inflection (SIGMORPHON 2017, 52 langs) test ACC 95.59 vs best prior 95.32 (ensemble).
- G2P (CMUDict/NETtalk) WER 27.63 vs 28.20.
- **Transliteration (NEWS 2015, dev only — "We do not have access to the test set")**: ACC 43.39 (dropout 0.3) vs 41.20 (Wu & Cotterell 2019); MFS 0.897 vs 0.895 (Table 4).

## Limitations
Single seed (no variance reported); transliteration result is dev-only and the averaged NEWS 2015 language set is not broken down; no Indic-romanized task.

## Relevance to us
- The most direct prior on our "char-level Seq2Seq vs small Transformer" question: the comparison is **hyperparameter-sensitive** (batch size, warmup, label smoothing, dropout). A fair comparison must tune both under equal budget; a naïve small-batch Transformer will lose.
- Combined with Roark 2020 (LSTM best on Tamil CER) and Kirov 2024 (Transformer best with 25 seeds), this frames a genuine open question we can test rigorously: under matched parameters, batch size and seeds, which wins on Dakshina Tamil — and which degrades more gracefully under noisy input?
- MFS (mean F-score) is the NEWS metric; see Chen et al. 2018 note.
