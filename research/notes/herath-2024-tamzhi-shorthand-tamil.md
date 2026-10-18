# Herath & Sumanathilaka 2024 — TAMZHI: Shorthand Romanized Tamil to Tamil Reverse Transliteration

**Citation.** H. M. Anuja Dilrukshi Herath, T. G. Deshan K. Sumanathilaka. 2024. "TAMZHI: Shorthand Romanized Tamil to Tamil Reverse Transliteration Using Novel Hybrid Approach." *International Journal on Advances in ICT for Emerging Regions (ICTer)* 17(1): 1–7. doi:10.4038/icter.v17i1.7271. Open access PDF from icter.sljol.info. Read in full. (The IndoNLP 2025 report cites it as "Mudiyanselage and Sumanathilaka (2024)"; the paper itself lists Herath as first author.)

## Problem
**The only paper found that targets informal/shorthand Tanglish specifically**: Tamil has 12 vowels vs 5 Latin vowel letters; social-media users drop vowels ("Kankl" for கணக்கில்), making reverse transliteration ambiguous.

## Method
Hybrid, non-neural: (1) **typing-pattern survey of 215 users** across communities, segmented/aligned to derive rules; (2) an "ad-hoc transliteration generator" with 82 vowel/consonant rules, 12 hal (pulli/virama) rules, 16 special-character rules, producing an ad-hoc Romanized Tamil dictionary; (3) NLTK unigram→bigram→trigram backoff taggers trained on 329,500 words / 10,000 phrases (author-typed text, Dakshina, YouTube comments, other online sources, plus generated data); (4) rule-based fallback for unknown tokens; (5) trie over generated variants + knowledge-base dictionaries for best-word suggestion.

Generated variant examples (Table I) — a ready-made, citable description of Tanglish shorthand:
- வாருங்கள் → Varungal, Varungl, Vrungl, Vrngal, Varngal …
- கணக்கில் → Kanakkil, Kanakkl, Kanakil, Kankl, Knakil, Knkkil, Knkil, Knakl, Knkkl, Knkl
- யாருக்கு → Yaarukku, Yarukku, Yrukku, Yrkku, Yarkku, Yarkk, Yruku, Yrk
Mapping rules (Table II) include ஆ→aa/ae, இ→i/e, த→tha/ta, ட→dha/da, ச→cha/ca, க→ka/ha, ழ→zha/la, ஓ→oo/o.

## Evaluation
Test: **200 Thirukkural records + 500 Dakshina records** (small; Thirukkural is classical poetry, not chat). Character-level accuracy **93%**, word-level accuracy **70%** (Table III); BLEU 0.86 vs 0.27 (Appicharla et al. 2021) and 0.74 (Raj & Laddagiri 2022) (Table IV) — but these comparisons are on different data and are not like-for-like.

## Limitations (my assessment)
Tiny, non-standard test set; no shorthand-specific test split reported separately; accuracy definitions are informal ("correctly suggested characters / total characters" — not edit-distance based); no neural baselines; no released benchmark that I could find; BLEU comparisons across datasets are not meaningful.

## Relevance to us
- Confirms the practical problem (vowel-dropped Tanglish) and gives an empirically grounded **typology of shorthand patterns** (215-user survey) that we can turn into a *parameterised noise generator* for robustness testing — and cite rather than invent.
- Clear gap: no neural seq2seq evaluation on shorthand Tamil, no controlled clean-vs-noisy comparison, no standard metrics. Our project can fill exactly this.
