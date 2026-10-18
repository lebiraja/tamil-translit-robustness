# Sumanathilaka et al. 2025 — IndoNLP 2025 Shared Task: Real-Time Reverse Transliteration for Romanized Indo-Aryan Languages

**Citation.** Deshan Sumanathilaka, Isuri Anuradha, Ruvan Weerasinghe, Nicholas Micallef, Julian Hough. 2025. "IndoNLP 2025: Shared Task on Real-Time Reverse Transliteration for Romanized Indo-Aryan languages." arXiv:2501.05816 (v3, Feb 2025); shared-task overview for the IndoNLP workshop at COLING 2025 (venue inferred from title/workshop name; not printed on the arXiv PDF). Read in full.

## Problem
Romanized→native transliteration for *ad-hoc, informal* typing: "inputs with inconsistent or missing vowels, abbreviations, and phonetic variations", under real-time / limited-compute constraints.

## Data / design (most relevant part for us)
Training mostly Dakshina + Aksharantar (+ Swa-Bhasha for Sinhala). **Two test sets per language** (Table 1): Test 1 "General Typing Patterns" (5k–10k) and **Test 2 "Ad-hoc Typing Patterns"** (5k each), the latter "featuring ad-hoc patterns with frequent vowel omissions". Test data "created and augmented" partly from existing public datasets — augmentation procedure is not specified in detail. Languages: Sinhala, Bengali, Gujarati, Hindi, Malayalam (no Tamil). Metrics: WER, CER, BLEU.

## Results (Table 3; Test 1 → Test 2)
- Sinhala, Vectora (dictionary + rules + BERT MLM context reranking): WER 0.0886 → 0.0914 (Sinhala BERT); fine-tuned BERT 0.0850 → 0.0895.
- Sinhala, MoraCSE rule-based: WER 0.6689 → 0.6809; M2M100 fine-tuned: 0.1983 → 0.2413.
- Hindi, IndiDataMiner LLaMA-3.1-8B LoRA: WER 0.2154 → 0.2851; "proposed": 0.1892 → 0.2640.
- **Malayalam, NexText char BiLSTM+attention (word-by-word, 4.3M pairs): WER 0.3450 → 0.6690, CER 0.0740 → 0.2270** — the word-level char model nearly doubles WER and triples CER on ad-hoc input.
- "Ad-hoc typing patterns (Test 2) posed challenges for all models."

## Inconsistency to flag
The prose describing NexText says "WER of 0.074 … high CER values (0.345 and 0.669)", which swaps the columns relative to Table 3 (WER 0.3450/0.6690, CER 0.0740/0.2270). Trust the table (CER < WER is the expected ordering).

## Limitations
Very few teams (4), different languages per team → no controlled comparison; augmentation procedure for Test 2 under-specified; no Dravidian language except Malayalam; no Tamil.

## Relevance to us
- **Closest existing precedent for our robustness evaluation**: a clean vs ad-hoc (vowel-omitted) split. It shows (for Malayalam, a Dravidian sister language) that a char-level BiLSTM trained on Dakshina+Aksharantar degrades sharply on ad-hoc input. Nobody has published the equivalent controlled study for Tamil, nor compared architectures under the same noise.
- Context/dictionary reranking (Vectora) is nearly invariant to ad-hoc input → evidence that lexicon/LM-constrained decoding buys robustness.
- Mentions "TAMZHI" (Mudiyanselage & Sumanathilaka 2024), a Romanized-Tamil back-transliteration system reported at 93% character-level and 70% word-level accuracy; I could not locate or read that paper, so these numbers are second-hand.
