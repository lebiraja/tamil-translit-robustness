# Kunchukuttan, Puduppully, Bhattacharyya 2015 — Brahmi-Net

**Citation.** Anoop Kunchukuttan, Ratish Puduppully, Pushpak Bhattacharyya. 2015. "Brahmi-Net: A transliteration and script conversion system for languages of the Indian subcontinent." *Proc. NAACL-HLT 2015: Demonstrations*, pp. 81–85. Read in full (demo paper).

## Problem / method
Online system for transliteration among 18 languages (306 pairs) + rule-based script conversion among 10 Brahmi-derived scripts and extended ITRANS romanization.
- Script conversion exploits Unicode's coordinated layout: "the first 85 characters in each Unicode block are in the same order and position", so conversion is code-point offset mapping.
- **Tamil note (§2.1):** Tamil "uses the characters for unvoiced, unaspirated plosives for representing voiced and/or aspirated plosives"; conversion into Tamil collapses voiced/aspirated plosives to the unvoiced unaspirated one.
- Statistical transliteration: phrase-based SMT (Moses) on character sequences, trained on 1,694,576 pairs mined (Sajjad et al. 2012) from the ILCI parallel corpus across 110 language pairs (~15k per pair). Tamil–English mined pairs: 3,500 (eng→tam column) / 3,549 (Table 1).

## Results
Table 2 (1,000 IndoWordNet pairs per language pair), e.g. mal→tam: rule-based 27.9, statistical top-1 30.9, top-5 66.0 (%). Large top-1→top-5 gap; LM reranking of top-k transliterations improved SMT BLEU (Table 3).

## Limitations
Formal ITRANS romanization, not informal user romanization; no English-romanized-Tamil evaluation; tiny eval; pre-neural.

## Relevance to us
Historical baseline for Indic transliteration; a citable source for (a) the Tamil-script voicing under-specification and (b) the large top-1 vs top-k gap that motivates reporting top-k and LM reranking. Also, a deterministic ITRANS-style rule system is a sensible *non-learned baseline* row for our paper (inference; Brahmi-Net itself does not evaluate this on Dakshina).
