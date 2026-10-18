# Roark et al. 2020 — The Dakshina Dataset

**Citation.** Brian Roark, Lawrence Wolf-Sonkin, Christo Kirov, Sabrina J. Mielke, Cibu Johny, Işın Demirşahin, Keith Hall. 2020. "Processing South Asian Languages Written in the Latin Script: the Dakshina Dataset." *Proc. LREC 2020*, pp. 2413–2423, Marseille. arXiv:2007.01176. Read in full.

## Problem
South Asian languages are routinely typed in Latin script (SMS, WhatsApp, social media) with **no standard romanization**; individuals write a "rough phonetic transcription" that varies by dialect, convention, idiosyncrasy (§1). Human-produced native/romanized parallel text does not occur naturally, so there is no licensed public data to train/validate on.

## Dataset (what we will use)
12 languages (bn, gu, hi, kn, ml, mr, pa, sd, si, **ta**, te, ur), all from Wikipedia (extracted March 2019). Three parts per language:
1. **Native-script Wikipedia text**, split train/validation *by page*. Tamil: 1,144.4k training sentences; 9.6 words/sentence (Table 1).
2. **Romanization lexicon**: native word + attested romanizations + count of attestations. Elicitation: "How would you write this word in the Latin script?" then "Can you think of any other ways…?" (§3.2). Counts are *elicitation counts, not usage frequency*. 25,000 train types and 5,000 dev/test types (split evenly, i.e. 2,500 dev / 2,500 test) for Tamil; **2.7 romanizations per native type** for Tamil (Table 1). Validation words share no lemma with training words (Morfessor FlatCat lemma separation) — so the test set measures generalisation to unseen lemmas, not memorisation.
   - Tamil examples given in the paper: அகதிகள் → agathigal (2), akathigal (1); டெம்பிள் → temple (3), tempil (1). English loanwords are frequent.
3. **Romanized Wikipedia sentences**: 10,000 sentences per language, manually romanized by native speakers with *no guidance on romanization strategy* (§3.3); split 5k dev / 5k test. Round-trip validation (re-transcribing romanized back to native) gives mean CER 0.054; **Tamil lowest at 0.04** — i.e. ~4% of characters are irreducibly ambiguous/variable even for humans.

## Metrics
CER and WER = (S+D+I)/reference tokens over minimum-edit alignment; tokens = Unicode characters (CER) or whitespace tokens (WER). Single-word: CER + WER (= 1 − top-1 accuracy); sentence: WER. Mean and std over 5 trials. LM: bits-per-character and bits-per-native-character (BPNC). Single-word evaluation is on **every attested romanization of each dev word** (attestation counts ignored), input Latin → 1-best native output.

## Baselines (dev set, NOT test)
Single-word transliteration, Tamil (Table 2), CER / WER %:
| Model | CER | WER |
|---|---|---|
| Pair 6-gram WFST (Witten-Bell) | 9.3 (.08) | 36.8 (.26) |
| Transformer (char tokens; d=128, ff=1024, 4 heads, 4+4 layers, dropout 0.36) | 9.4 (.52) | 34.3 (.78) |
| BiLSTM seq2seq + Luong attention (emb 512; enc 1 biLSTM 256 + 1 LSTM 256; dec 3×128; batch 1024; lr 0.01) | **8.4 (.12)** | 34.7 (.67) |

Across languages: all three systems within 2% absolute CER; transformer best on 8/12, LSTM best on 2 (ta, ur), pair 6g best on 2 (sd, si). Dravidian languages among easiest; Perso-Arabic hardest. **Tamil is one of only two languages where the LSTM beat the Transformer on CER** — directly relevant to our LSTM-vs-Transformer comparison. Transformer variance on Tamil (std .52 CER) is notably higher than the LSTM's (.12).

Full-sentence transliteration, Tamil (Table 4, WER %): whitespace eval — pair 6g single-word 30.7, transformer single-word 31.9, noisy channel (pair 6g + Katz trigram word LM) 19.3, whitespace transformer 18.9; pass-through eval — 30.7, 31.9, 19.9, 20.1, full-string transformer 19.6. Sentence context gives ~11–12 WER points over word-by-word. Noisy channel wins 9/12 languages; the transformer wins on "highly inflected Dravidian languages of Malayalam and Tamil" (closed-vocab LM hurts agglutinative languages).

Sentence models are trained on **simulated** romanizations: a native→Latin transformer samples from 8-best per word to romanize the native Wikipedia corpus. LM experiments show sampling ≫ Viterbi-best for simulating romanized text (Table 5) — evidence that modelling romanization *variability* matters.

## Limitations (stated or evident)
- Baselines are explicitly "not … to squeeze every last bit of accuracy"; hyperparameters tuned on a subset of languages, not per language.
- Reported numbers are on **dev**, test held in reserve — later papers report on test; be careful mixing them.
- Romanizations are elicited from Wikipedia words/sentences by annotators, i.e. careful, single-word, out-of-context typing; not naturally occurring chat text. No casing, digits or punctuation in lexicons.
- Lexicon words are sampled from Wikipedia (frequency > 1), so the vocabulary is encyclopaedic (named entities, loanwords) rather than conversational.

## Gap it leaves / relevance to us
- Defines our task, data and metrics. Our baseline table must reproduce Table 2 numbers in kind (CER, WER/top-1 on the lexicon) and report mean±std over seeds, as they do.
- Inference: Dakshina's romanizations are "informal" (no standard was imposed) but *elicited*, not organic chat text; real WhatsApp Tanglish adds abbreviation, vowel dropping, repeated letters, code-mixing and typos that the dataset does not sample. This is the robustness gap we can target.
- Their LSTM ≥ Transformer result on Tamil is a concrete, citable motivation for a careful char-level LSTM vs small Transformer comparison under matched parameter budgets.
