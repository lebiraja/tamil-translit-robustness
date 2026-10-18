# Wolf-Sonkin, Schogol, Roark, Riley 2019 — Latin-script keyboards for South Asian languages with finite-state normalization

**Citation.** Lawrence Wolf-Sonkin, Vlad Schogol, Brian Roark, Michael Riley. 2019. "Latin script keyboards for South Asian languages with finite-state normalization." *Proc. 14th FSMNLP*, pp. 108–117, Dresden. Read in full.

## Problem
Users who keep text in Latin script (romanized Hindi/Tamil…) still need auto-correction and prediction, but there is no standard spelling, so a word-based LM with one "canonical" romanization per word mismatches users' variants.

## Evidence of variation (useful quote material)
A 2011 India Today blog comment thread: भ्रष्टाचार romanized 16× "bhrastachar", 7× "bhrashtachar", 1× each "barashtachaar", "bharastachar", "bharstachar", "bhastachar", "bhrstachar" (§2.1). Variation sources named: optional 'h' for aspiration, optional doubling for long vowels and geminates — "These variants are not random in the way that a character loop model would score them" (§3.3). This is a citable typology of *systematic* romanization variation distinct from typos.

## Method
FST keyboard decoder (spatial model ∘ transducer ∘ LM). Compared: fixed vocabulary with canonical romanization; + compact supplemental unigram of attested alternatives (KL-minimised compact automaton); pair n-gram transducer variant→canonical; transducer to native-script LM, reading the output from the **input tape** so the user's own spelling is preserved; + pruned-trie OOV model.

## Data / evaluation
Proprietary Hindi lexicon: ~110k native words, 3.1 romanizations/word; pair 3-gram pruned to 110k n-grams; LM 150k words, 750k n-grams; target total model ~10MB for cheap phones. Dev: 4,000 manually romanized Hindi Wikipedia sentences (36,027 tokens). **Noise simulation**: touch points sampled from 2-D Gaussians centred on each key; "literal" baseline (raw keys hit) WER = 45.0%.

## Results (Table 1, WER %)
At ~1.0 ms/tap: fixed vocab 22.6, + supplemental unigram 12.4, + transducer to canonical 12.9, transducer to native 13.1, transducer to native + OOV model **10.5** (54% relative reduction; 11.2 MB vs 4.9 MB). At ~0.55 ms/tap: supplemental unigram best, 12.1 (46% relative reduction). Doubling LM n-grams in the fixed-vocab system does not help → variation is not fixed by more capacity.

## Limitations
Hindi only; proprietary data; output is Latin script (not transliteration); simulated rather than real typing noise.

## Relevance to us
- Gives a principled, cited **noise model** (Gaussian key-tap noise on a QWERTY layout) we can reuse to synthesize "fat-finger" Tanglish typos, separately from *systematic* romanization variation (h-dropping, vowel/consonant doubling).
- Shows that size/latency constraints matter for real deployment (10 MB, <20 ms/tap) — supports a lightweight-model angle.
