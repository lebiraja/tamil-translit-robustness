# Xue et al. 2022 — ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models

**Citation.** Linting Xue, Aditya Barua, Noah Constant, Rami Al-Rfou, Sharan Narang, Mihir Kale, Adam Roberts, Colin Raffel. 2022. "ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models." *Transactions of the ACL* 10 (venue per standard citation; arXiv:2105.13626v3 PDF used). Read in full (main text; appendices skimmed).

## Content
Standard T5 encoder–decoder over UTF-8 bytes (vocab 256 + specials), heavier encoder (e.g. 3:1 depth), span-corruption pretraining on mC4. Sizes Small 300M … XXL 12.9B.

## Results relevant to us
- **Dakshina single-word transliteration, macro CER, dev** (one multilingual model with language prefix; Table 5): ByT5 Small **9.8**, Base 9.9, Large 10.5, XL 10.6, XXL 9.6; mT5 Small 20.7 … XXL 16.6. Footnote: ByT5 beats Roark et al.'s char Transformer (9.6 vs 12.2 macro). Not per-language; Tamil not reported separately. Note bigger ≠ better here (Small ≈ XXL).
- Noise (Table 6, XNLI/TyDiQA): five schemes — Drop (10%/char), Repetitions (20% chance, 1–3 repeats), Antspeak, Uppercase, Random case. ByT5 degrades less than mT5 under every scheme, both when noise is seen in fine-tuning ("learnable") and unseen at test; e.g. random case: mT5 −25.7 vs ByT5 −1.5 (XNLI, learnable).
- Byte/char models are slower per input (longer sequences); ByT5 beats mT5 most clearly at small sizes.

## Relevance to us
- Strongest evidence that **character/byte granularity is the right input unit** for spelling-sensitive tasks and noisy input vs subwords; supports our char-level design and a char-vs-subword ablation (expect subword to lose, especially under noise).
- Their **noise schemes (drop, repetitions)** are directly reusable: "repetition" models WhatsApp elongation ("semmaaaa"), "drop" models vowel omission (but random, not phonologically targeted).
- A 300M-param ByT5-Small fine-tune is a feasible "large pretrained" comparison point on a student GPU only with care (Kirov 2024 found ByT5 unstable on Tamil without data pruning: CER 12.7, std 3.85).
