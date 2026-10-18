# Kirov et al. 2024 — Context-aware Transliteration of Romanized South Asian Languages

**Citation.** Christo Kirov, Cibu Johny, Anna Katanova, Alexander Gutkin, Brian Roark. 2024. "Context-aware Transliteration of Romanized South Asian Languages." *Computational Linguistics* 50(2): 475–534. doi:10.1162/coli_a_00510. Read in full (main text + Appendices A–C; Appendices D–E skimmed for structure only).

## Problem
Full-sentence Latin→native transliteration on Dakshina without sentence-level parallel training data; quantify how much of the gain comes from *context* vs better word models.

## Method
- Single-word models: pair 6-gram WFST, BiLSTM+Luong attention and char Transformer (Roark 2020 hyperparameters), and **ByT5-base** fine-tuned on a 24-task mixture (12 langs × 2 directions, prefixed e.g. "ta-Latn-Taml"). 25 training runs per model; ensembles = uniform mean of softmax-normalised k-best probabilities (Eq. 5).
- Context: (i) "noisy channel" = word lattice of k-best transliterations ∘ word→wordpiece FST ∘ 4-gram Kneser-Ney wordpiece LM (sentence-level or word-level); (ii) mT5/ByT5 fine-tuned on simulated parallel sentences (native Wikipedia romanized 10× by sampling 8-best from a ByT5+LSTM native→Latin ensemble).
- New metrics: **minCER** for one-to-many romanization (min over attested references) and **EMD k-best CER** comparing the model's k-best distribution with the empirical distribution of attested romanizations.
- Training-data pruning for ByT5: rank items by mean distance between attested romanization and a pair-4gram romanizer's output across 20 random half-splits; drop top 10%.
- Cache-based online inference (precomputed ensemble k-best for up to 1M romanizations) with CPU throughput measurement.

## Key numbers (Dakshina dev unless noted)
Single-word Latin→native CER% (Table 2; 25 runs), **Tamil**: pair 6g 9.4 (.04); Transformer **8.2 (.10)**; LSTM 8.6 (.13); ByT5 (pruned) 7.9 (.42). Roark's 5-run numbers: 9.3 / 9.4 (.52) / 8.4 (.12).
Macro-avg CER (Table 3): single models pair 13.0, Transformer 12.1, LSTM 12.5, ByT5 11.4; 5-model ensembles 13.0 / 11.8 / 11.8 / 10.9; best multi-model ensemble (ByT5+LSTM+pair) 10.4. "the LSTM ends up yielding the same CER% as transformer after single method ensembling."
Tamil pruning effect (Table B.3): ByT5 12.7 (std **3.85**) → 7.9 (.42); pair 9.4→9.3; LSTM 8.6→8.5; Transformer 8.2→8.2. Non-pretrained models are robust to the outliers; the pretrained model is not. The outliers include **annotation noise** in the Dakshina Tamil lexicon (e.g. "tikket" paired with the wrong native constituent) and hard loanwords/names (App. B).
Native→Latin minCER% Tamil (Table 4): pair 3.3, Transformer 3.1, LSTM 2.8, ByT5 2.5. Transformer "has relatively high variance for the four Dravidian languages". EMD k-best: LSTM k-best lists match the human variant distribution better than Transformer's (Table 6: 9.0 vs 9.8 single; 8.6 vs 9.4 ensembled).
Full-sentence WER% Tamil: non-contextual ensemble 27.2 → +word-level LM **17.6** (Table 7); noisy channel (sentence LM) 15.9; mT5-large 16.6; ByT5-base 19.8; full ensemble **14.8** (Table 8). **Test set** (Table 16): non-contextual 17.3, contextual 14.7. Macro: 17.9 → 14.4 (test 14.4).
Word-level LM accounts for ~80% of the relative WER reduction between word-only models and the best context-aware system. Dravidian languages benefit least from sentence context (highly inflected → many within-word dependencies).
Tamil romanizations per repeated word in dev sentences: 1.9 (Table 1). Tamil cache token coverage 79.9%; Tamil CPU throughput ≈ 0.55k chars/s without LM (among slowest).

## Limitations
Huge compute (25 runs × many models, T5 large); still Wikipedia-domain, annotator-romanized text. mC4-trained LMs *hurt* Dravidian languages (Tamil noisy channel 15.9 → 25.9 WER), attributed to domain/register mismatch. Acronyms and inflected English loans (e.g. "IASlekku") remain error sources.

## Relevance to us
1. **Directly contradicts the Roark 2020 Tamil LSTM>Transformer result** once 25 seeds are used (Transformer 8.2 vs LSTM 8.6). Lesson: the LSTM-vs-Transformer question on Tamil is within seed noise at 5 runs; our comparison must use ≥5 seeds, report std, and ideally a significance test.
2. Word-level LM rescoring is the single cheapest big win (Tamil sentence WER 27.2 → 17.6). For word-level evaluation this corresponds to unigram/wordpiece LM reranking (cf. Aksharantar +10 points).
3. minCER / EMD metrics give us a principled way to evaluate *variation-aware* behaviour — relevant to a Tanglish robustness study.
4. Evidence of label noise in the Tamil lexicon justifies a noise-robust training angle and an error-analysis section.
