# Hellsten et al. 2017 — Transliterated mobile keyboard input via WFSTs

**Citation.** Lars Hellsten, Brian Roark, Prasoon Goyal, Cyril Allauzen, Françoise Beaufays, Tom Ouyang, Michael Riley, David Rybach. 2017. "Transliterated Mobile Keyboard Input via Weighted Finite-State Transducers." *Proc. 13th FSMNLP*, pp. 10–19, Umeå. doi:10.18653/v1/W17-4002. Read in full.

## Problem
On-device QWERTY→native-script (Hindi, Tamil, …) keyboard decoding under strict constraints: ≤20 ms latency, ~10 MB total model size, bounded memory.

## Method
Pair n-gram (joint multigram) transliteration model trained with EM alignments (multi-symbol merges like "sha:श" to cut epsilons), compiled as WFST T = I∘P∘O; determinization with auxiliary symbols for weight pushing; optimized L∘G as character trie with LOUDS encoding and 8-bit quantized weights; conditional normalisation of the joint transliteration model; on-the-fly composition of static C∘T (~1.7 MB) with static L∘G (~6.7 MB). Reduced beam, stricter edit and spatial models — authors note that "doubling or interchanging vowels is one common source of transliteration ambiguity" that overlaps with the typo-correction model.

## Data
Vocab 150k, pruned trigram 750k n-grams. Transliteration training: per native word, transliterations from ~5 speakers. **Blind test sets: real tapped and gestured sentences in Hindi and Tamil (>3,000 words each), typed by participants "using their preferred transliteration", at natural pace, mistakes not fixed** — i.e. naturally noisy romanized input. Not public.

## Results
Table 2 (WER %, latency per char ms): Hindi baseline HMM 19.5 / 3.0 → WFST 16.4 / 0.5; **Tamil baseline 26.2 / 2.1 → WFST 22.6 / 0.2**. Tamil L∘G size: standard 126.5 MB, generic compact 37.1 MB, LOUDS 9.80 MB (Table 1). Launched for 22 languages in Gboard (H1 2017).

## Limitations
Proprietary data; no neural comparison; results include tap noise and LM so not directly comparable to Dakshina word accuracy.

## Relevance to us
- Only paper found that evaluates Tamil transliteration on **naturally typed, uncorrected** romanized input; Tamil WER (22.6) is higher than Hindi (16.4) — citable evidence that Tamil is the harder case under realistic noise.
- Establishes the deployment constraints (10 MB, 20 ms) that a "lightweight model" claim should be measured against.
- Pair n-gram WFST is a strong non-neural baseline (also used by Dakshina).
