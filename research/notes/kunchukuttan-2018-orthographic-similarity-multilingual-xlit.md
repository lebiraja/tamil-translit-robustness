# Kunchukuttan, Khapra, Singh, Bhattacharyya 2018 — Leveraging Orthographic Similarity for Multilingual Neural Transliteration

**Citation.** Anoop Kunchukuttan, Mitesh Khapra, Gurneet Singh, Pushpak Bhattacharyya. 2018. "Leveraging Orthographic Similarity for Multilingual Neural Transliteration." *Transactions of the ACL* 6: 303–316. Read in full (main text; zeroshot and phonetic-feature sections read more lightly).

## Method
Compact multilingual char encoder–decoder (CNN encoder chosen over BiLSTM, shared attention, language-specific output layers optional) trained jointly on orthographically similar language groups (Indic, Slavic, Arabic); NEWS 2015 data plus mined Indic–Indic pairs; top-1 exact match.

## Results (Table 3, top-1 %; P = bilingual PBSMT, B = bilingual neural, M = multilingual neural)
- **en→ta: P 52.90, B 57.80, M 55.30** — multilingual training *hurts* English→Tamil (only 1.1% average gain for English→Indic overall).
- **ta→en: P 33.93, B 23.22, M 25.93** — PBSMT beats both neural models (Tamil→English is under-specified).
- Indic–Indic average gain 45.5%; Slavic–Arabic 55.8%; Arabic–Slavic 176.8%. Overall average +58% (abstract).
- Error analysis: multilingual models reduce vowel and consonant-ambiguity errors and favour **canonical** spellings over phonetically equivalent alternatives.

## Relevance to us
- Tamil is again the outlier: the source of the "Tamil-specific" handling later adopted by Kunchukuttan et al. 2021 and IndicXlit. Supports focusing on Tamil as a scientifically interesting case, not just a convenient one.
- The "canonical spelling" effect is relevant to evaluation: Tamil has some genuine native-script spelling variants (loanwords), so exact-match accuracy undercounts acceptable outputs — another reason to report CER and top-k.
- Data is NEWS named entities in standard English spelling, not informal romanization.
