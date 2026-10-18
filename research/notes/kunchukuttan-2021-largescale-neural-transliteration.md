# Kunchukuttan, Jain, Kejriwal 2021 — Large-scale evaluation of neural transliteration for Indic languages

**Citation.** Anoop Kunchukuttan, Siddharth Jain, Rahul Kejriwal. 2021. "A Large-scale Evaluation of Neural Machine Transliteration for Indic Languages." *Proc. EACL 2021* (main volume), pp. 3469–3475. Read in full (short paper).

## Problem
Evaluate multilingual neural transliteration between English and 10 Indic languages, exploiting orthographic similarity among Brahmi-derived scripts.

## Data
~600k (606k) word pairs mined from 7.4M parallel sentence pairs (Moses/Sajjad et al. 2012 mining) and from monolingual vocabularies (candidate scoring by edit distance between Double Metaphone codes). Tamil: 57.1k pairs, mining accuracy 77.9% (Table 1; avg 84.18%). Test/dev: 1,500 English words common across all languages (928 foreign-origin, 572 Indian-origin), crowd-verified with 3 judges. Training set ~55% non-Indian-origin words.

Important for us: the "English" side is **standard English spelling of named entities/loanwords**, not informal romanization. So E→X here ≠ Tanglish→Tamil.

## Method
Char-level attention encoder–decoder (Marian), BiLSTM encoder, 128 units (1 layer bilingual, 2 layers multilingual), emb 128, batch 100, beam 4. Variants: all-Indic vs per-family models, disjoint vs unified (Devanagari) script vocab, source-language tag, and a **Tamil-script-pivot** model for Dravidian languages.

## Results (top-1 accuracy %, Table 2)
- Tamil is the hardest language in X→E: bilingual ta→en foreign 38.28, Indian 45.99. Authors attribute it to Tamil's "deficient orthography": "The Tamil script is highly under-specified and has fewer characters than sounds in the English language" (§3).
- E→X (en→ta) bilingual foreign-origin 67.22.
- Mapping other Dravidian scripts to Tamil script (instead of Devanagari) gives +2–5 points: en-ta foreign 73.5 → 78.8, Indian 81.72 → 83.9; ta-en foreign 44.04 → 47.37, Indian 50.6 → 53.3.
- Multilingual training: ~20% gain in X→E, 6–7% in E→X; source tags help +6–7 on divergent languages (bn, ml, ta).
- Orthographic similarity (LCSR): Tamil and Malayalam most divergent from other Indic scripts.

## Limitations
Short paper; no CER, no significance tests; only named-entity-like vocabulary; LSTMs only, no Transformer comparison.

## Relevance to us
- Gives a citable linguistic reason why Tamil is special: Tamil script under-specifies voicing/aspiration (one grapheme e.g. க for k/g/h sounds), so *Latin→Tamil* is many-to-one at the grapheme level (easier) while Tamil→Latin is one-to-many (harder). Inference: for our direction, the core ambiguity is not consonant voicing but vowel length (a/aa, i/ii…), gemination (tt vs t), and the three-way l/ḷ/ḻ and n/ṇ/ṉ/ñ distinctions that Tanglish typists often collapse.
- A small BiLSTM (128 units) is a strong, cheap baseline — supports our lightweight angle.
