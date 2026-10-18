# Robustness of Character-Level Transliteration to Informal Romanized Tamil

IA3 Deep Learning project (staff topic #34, "Tanglish-to-Tamil Script Transliteration Using Character-Level Seq2Seq"), Karunya Institute of Technology and Sciences, B.Tech AI&DS, 5th semester. Deliverables: working code, trained models, a paired robustness benchmark with a human-typed test set, and an IEEE-format research paper.

## 1. The problem in plain words
Tamil speakers type Tamil on phones using English letters: *vanakkam*, *semma*, *iruku*, *kankl*. This is "Tanglish". To search, autocomplete or display it properly, software must convert the Latin text back into Tamil script (வணக்கம்). That conversion is **transliteration** (sounds to letters), not translation.

Tamil makes this hard. The Latin alphabet cannot express Tamil's vowel length (a/aa), doubled consonants (k/kk), or several of its distinct n, l and r sounds. People also type inconsistently and quickly: they drop vowels (*kankl*), collapse long vowels (*kanum* for *kaanum*), collapse doubled letters (*iruku* for *irukku*), swap digraphs (*vaazhga* typed as *vazhga* or *vaazga*), stretch letters (*semmaaaa*) and make keyboard slips. Published models are trained and tested on clean romanization. How they behave on real typing is almost unmeasured for Tamil.

## 2. What the staff asked versus what we do
The staff's topic is a character-level Seq2Seq model trained on Google Dakshina (Tamil) with a typing box as live input. We build that model as the baseline, then go further: we turn it into a **robustness study** with a paired benchmark, an augmentation comparison and an architecture comparison. The staff does not need to know the field; the work follows proper research practice (D9).

## 3. What the research found
Full detail: `research/KNOWLEDGE_BASE.md` (32 papers), `research/NOVELTY_CANDIDATES.md`, `research/DATASET.md`, `docs/datasets/`.
- **Dakshina is clean.** The Tamil part is formal Wikipedia text that native speakers romanized on request (25,000 train / 2,500 dev / 2,500 test words; about 2.7 romanizations per word). It has almost no colloquial forms or vowel-dropping shorthand.
- **Nobody has a controlled robustness benchmark for Tamil.** The closest evidence: Malayalam CER 7.4 to 22.7 when vowels are dropped (Baiju 2024); a 100-word unpaired Tamil test where every model, including GPT-4.5, falls to about 20% (Azam 2025); a shorthand-Tamil paper that tests no neural model (TAMZHI 2024).
- **LSTM versus Transformer on Tamil is contested** (Roark 2020: LSTM better, CER 8.4 vs 9.4 over 5 seeds; Kirov 2024: Transformer better, 8.2 vs 8.6 over 25 seeds; Wu 2021: depends on batch size) and has never been compared under noise.
- **Variation-aware synthetic data works for romanized language ID** (Benton 2025) but is untested for transliteration robustness.
- **No public set pairs real informal Tanglish with Tamil-script gold.** Real corpora exist (DravidianCodeMix 44,020 comments, HopeEDI 18,178, Tanglish-Corpus-185k 174,424) but have sentiment/offence labels only. Measured against Dakshina sentences, real comments show vowel dropping 3 to 5 times more often, vowel-length collapse 1.8 to 3.5 times, elongation up to about 9 times.
- **Aksharantar's Tamil test set contains all of Dakshina's test pairs**; the independent remainder is 4,335 rows. Several "other" Tanglish pair sets on the web are Dakshina copies and must not be used for training.

## 4. Contributions (locked, D2)
1. **C1, paired robustness benchmark.** A Tamil-specific noise taxonomy (vowel drop, long/short vowel collapse, geminate collapse, digraph swaps, keyboard slips, elongation, mixtures) at several severities, applied to the Dakshina test set so each noisy word is paired with its clean form and gold answer, plus a **human-typed test set** (about 1,500 words) that tests whether synthetic noise predicts real typing.
2. **C2, augmentation study.** Train with no augmentation, random character noise, Tamil-phonological noise, sampled back-transliteration and a clean-data control; test on held-out noise types and on the human set.
3. **C3, architecture comparison.** BiLSTM-attention against a small Transformer, matched for parameters and tuning budget, 5 seeds, statistical tests, clean and noisy input.
4. **C4 (optional).** Language-model reranking and lexicon priors on noisy input.

## 5. Research questions
- RQ1: How much does CER and accuracy degrade per noise type and severity?
- RQ2: Does synthetic noise predict degradation on human-typed text?
- RQ3: Which training augmentation recovers robustness without hurting clean accuracy?
- RQ4: Which architecture degrades least at matched size and tuning?

## 6. Method overview
Data: Dakshina lexicon for training, dev and clean test; Aksharantar non-Dakshina rows (4,335) as independent test; human-typed set for real typing; real comment corpora to calibrate noise rates. Models: character BiLSTM+attention and pre-LN Transformer at about 1M, 3M and 8M parameters, beam search for top-k. Metrics: top-1, top-5, MRR, CER, degradation per noise type and severity, mean and standard deviation over 5 seeds, paired bootstrap and Kruskal-Wallis with Dunn post-hoc, Spearman correlation for RQ2. A reproduction gate against published Dakshina baselines comes first. Details: `docs/experiment-plan.md`.

## 7. Why it is a good paper
It answers a concrete open question with a controlled design, adds a new public resource (paired noisy test sets and a human-typed set), resolves a literature conflict (or shows it is seed noise), and is honest about limits (formal base data, few typists, ambiguity ceiling). It is feasible: models are 1M to 8M parameters and trained in minutes to tens of minutes each on an RTX 5070.

## 8. Honest risks
- Null result in C3 (still reportable as a matched-budget replication with a robustness axis).
- The human set may be idiosyncratic with few typists.
- Typing from Tamil-script prompts may be more careful than real chat.
- Dakshina has about 0.35% label noise; Aksharantar train overlaps Dakshina stems.
- Vowel-dropped inputs are genuinely ambiguous (report top-k and oracle ceilings).
- Leica's GPU stability depends on not rebooting it (D15).

## 9. Where to look
| Need | File |
|---|---|
| Locked choices | `DECISIONS.md` |
| Experiment details | `docs/experiment-plan.md` |
| Human set protocol | `docs/human-typing-protocol.md` |
| Paper plan | `docs/paper-outline.md` |
| Machines | `docs/infrastructure.md` |
| Datasets | `docs/datasets/README.md` |
| What was done | `docs/session-log-2026-10-18.md`, `STATUS.md` |
| Next steps | `HANDOVER.md`, `CHECKLIST.md` |
