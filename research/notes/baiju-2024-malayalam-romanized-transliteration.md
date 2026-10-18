# Baiju et al. 2024 — Romanized to Native Malayalam Script Transliteration Using an Encoder-Decoder Framework

**Citation.** Bajiyo Baiju, Kavya Manohar, Leena G Pillai, Elizabeth Sherly. 2024. "Romanized to Native Malayalam Script Transliteration Using an Encoder-Decoder Framework." arXiv:2412.09957 (Dec 2024); system description for the IndoNLP 2025 shared task (team NexText). Read in full.

## Method
Word-level char model: input ≤57 chars, embedding 64, BiLSTM (256 concat) → dense 128 context → RepeatVector → LSTM decoder + attention → time-distributed softmax over 76 Malayalam symbols. Trained on 4.344M pairs (Dakshina 244k + Aksharantar 4.100M), single A100. Sentences split into words; punctuation/digits re-inserted.

## Results (IndoNLP-2025 Malayalam test sets; Table 2)
| | CER % | WER % | BLEU % |
|---|---|---|---|
| Test 1 (general typing) | 7.4 | 34.5 | 32.7 |
| Test 2 (ad-hoc, vowels omitted) | **22.7** | **66.9** | 7.5 |
(Confirms the table values in the shared-task overview; the overview's prose swaps CER/WER.)

Error analysis: confusion of phonetically similar Malayalam characters sharing one romanization. Authors argue WER/BLEU over-penalise small character errors and advocate CER.

## Stated limitations
"The training data primarily covers standard typing patterns and miss[es] the nuanced variations found in irregular typing scenarios"; no language model. Future work: fine-tune "using a diverse dataset that includes a significant proportion of adhoc typing patterns".

## Relevance to us
- **The most direct quantitative evidence of the robustness gap** in a Dravidian language: a char-BiLSTM trained on Dakshina+Aksharantar triples its CER (7.4 → 22.7) on vowel-omitted input. The authors' own proposed fix (train with ad-hoc patterns) is exactly the noise-augmentation experiment we can run for Tamil — and they did not run it, so it remains open (as of Dec 2024 for Malayalam; I found no Tamil equivalent).
- Supports CER as primary metric for sentence-level evaluation.
