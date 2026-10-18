# Belinkov & Bisk 2018 — Synthetic and Natural Noise Both Break Neural Machine Translation

**Citation.** Yonatan Belinkov, Yonatan Bisk (equal contribution). 2018. "Synthetic and Natural Noise Both Break Neural Machine Translation." *ICLR 2018*. arXiv:1711.02173. Read in full.

## Problem
Character/sub-word NMT models are brittle to noise humans read easily.

## Method
Noise on the source side of IWSLT 2016 TED data (Fr/De/Cs→En): **natural** errors harvested from edit corpora (Wikipedia edits etc.) and **synthetic**: Swap (adjacent letters), Mid (scramble all but first/last), Rand (full scramble), Key (replace one letter with a keyboard-adjacent key, "noise→noide"). Models: char2char (Lee et al. 2017), Nematus (BPE), charCNN, and meanChar (average of char embeddings, scramble-invariant). Robustness via black-box adversarial training: train on noised data, single noise or mixtures.

## Results (Table 3, BLEU, trained on clean)
German: charCNN vanilla 34.79 → Key 6.40, Nat 14.02, Rand 1.02; char2char 29.97 → Key 2.96, Nat 12.68; Nematus 34.22 → Key 0.61, Nat 10.68. French charCNN 42.54 → Key 8.26, Nat 17.42.
- Training on a noise type yields robustness mainly to **that** type; scrambling, Key and Nat "are not mutually-beneficial"; "only models trained on natural noise can reasonably translate natural noise".
- Training on a **mixture** (Rand+Key+Nat) is not best on any single type but best on average, and keeps decent clean performance.
- Natural German noise (~40 examples analysed): **phonetic/phonological phenomena 34%, character omissions 32%** — "not directly captured by our synthetic noise generation… good synthetic errors will likely require more explicit phonemic and linguistic knowledge."
- Spell-checking before Google Translate helps (+~5 BLEU Fr/De) but does not close the gap.

## Limitations
MT, not transliteration; European languages; natural-noise sets limited.

## Relevance to us
- Canonical citation for: (i) clean-trained char models collapse under noise; (ii) noise-type–specific augmentation does not transfer; (iii) mixture training is the robust compromise; (iv) **realistic noise must be phonologically motivated** — exactly the case for Tanglish (vowel omission, aspiration dropping, l/zh/L merging), which are phonological, not random typos.
- Suggests our experimental grid: train {clean, keyboard-typo, phonological-variation, mixture} × test {clean, each noise type, real Tanglish}.
