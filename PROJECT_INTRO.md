# Robustness of Character-Level Transliteration to Informal Romanized Tamil

IA3 Deep Learning project (topic #34), Karunya Institute of Technology and Sciences. Team of three.

## What we are building
People type Tamil on phones using English letters ("Tanglish"): *vanakkam*, *semma*, *kankl*. A transliteration model turns that Latin-script text back into Tamil script (வணக்கம்). Published models are trained and tested on **clean** romanization. Real typing drops vowels, merges long and short vowels, collapses doubled consonants and repeats letters.

We train a character-level sequence-to-sequence model on Google Dakshina (Tamil), then measure how it behaves on informal input and how to improve it.

## The gap (from 32 papers, see `research/KNOWLEDGE_BASE.md`)
- No controlled, paired robustness evaluation exists for Tamil. The closest is Malayalam (CER 7.4 -> 22.7 with vowels dropped) and a 100-word unpaired test for Tamil.
- LSTM vs Transformer on Tamil is contested: Roark 2020 says LSTM, Kirov 2024 says Transformer. Nobody compared them under noise.
- Variation-aware augmentation helps language ID (Benton 2025) but is untested for transliteration robustness.
- Dakshina is formal Wikipedia Tamil romanized on request, not chat text (`research/DATASET.md`), so a real informal test set is needed.

## Contributions (locked, D2)
1. **C1 Benchmark.** Tamil-specific noise operators (vowel drop, vowel-length collapse, geminate collapse, digraph variation, keyboard errors, repetition) at several severities, applied to Dakshina test so every noisy item is paired with its clean form. Plus a **human-typed set** (~1,500 words typed by the team, WhatsApp-style).
2. **C2 Augmentation study.** Train with: none, random char noise, Tamil-phonological noise, sampled back-transliteration, and a matched clean-data control. Test on held-out noise types and the human set.
3. **C3 Architecture comparison.** BiLSTM+attention vs small Transformer at matched size and tuning budget, 5 seeds, with statistical tests, on clean and noisy input.

## Research questions
- RQ1: How much does CER degrade per noise type and severity?
- RQ2: Does synthetic noise predict degradation on human-typed text?
- RQ3: Which augmentation recovers robustness without hurting clean accuracy?
- RQ4: Which architecture degrades least at matched budget?

## Data
Dakshina v1.0 Tamil lexicon: 25,000 train words (68,218 pairs), 2,500 dev, 2,500 test; CC BY-SA 4.0. Details and quirks: `research/DATASET.md`. Not downloaded yet.

## Metrics
Top-1 accuracy, top-5, CER, per-noise degradation, mean ± sd over 5 seeds, paired bootstrap or Kruskal-Wallis for significance.

## Deliverables
Code, trained models, human-typed test set, IEEE-format paper (LaTeX), demo (optional), assignment submission.
