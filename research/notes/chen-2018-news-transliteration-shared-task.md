# Chen et al. 2018 — Report of NEWS 2018 Named Entity Transliteration Shared Task

**Citation.** Nancy Chen, Rafael E. Banchs, Min Zhang, Xiangyu Duan, Haizhou Li. 2018. "Report of NEWS 2018 Named Entity Transliteration Shared Task." *Proc. Seventh Named Entities Workshop (NEWS 2018) at ACL*, pp. 55–73, Melbourne. Read in full (appendix tables scanned for English–Tamil).

## Content
19 named-entity transliteration tasks (13 languages), 6 teams, 424 runs; standard runs only (no external data). Includes **M-EnTa (English→Tamil, mixed-origin names)**.

## Metrics (§3) — canonical definitions we can cite
- **ACC** (word accuracy in top-1): 1 if top candidate matches *any* reference.
- **Mean F-score** ("fuzziness in top-1"): LCS-based precision/recall vs the closest reference (by edit distance), LCS(c,r) = ½(|c|+|r|−ED(c,r)).
- **MRR** over up to 10 candidates; **MAP_ref** precision over references in the n-best list.
Systems submit ranked lists of up to 10 candidates.

## Systems
SINGA: non-neural baselines (Sequitur, Moses) — "generally comparable to neural systems"; UALB: system combination of DirecTL+, Sequitur, OpenNMT, seq2seq, RL-NMT (up to +8% abs. from combination); EDI: deep attention RNN encoder–decoder with dropout, ensembling and right-to-left rescoring — best in most tasks; UJUS: RNN and CNN NMT with BPE and char segmentation.

## English→Tamil results (Table A4, NEWS18 test)
Best top-1 ACC **0.3343** (SINGA, non-neural); EDI 0.3333 ACC with the best F-score **0.8515** and MRR 0.4455; UALB best 0.3243. I.e. top-1 ≈ 33% but F ≈ 0.85: most errors are near-misses of a few characters.

## Limitations
Named entities in standard English spelling (not informal romanization); licensing-restricted datasets; Persian test-set script mismatch.

## Relevance to us
- Source for metric definitions (ACC, F-score, MRR, MAP) — we should report top-1 ACC, top-k ACC, MRR and CER; the large ACC/F gap for Tamil supports reporting a character-level metric alongside exact match.
- Evidence that non-neural (Sequitur/Moses) systems remain competitive on Tamil — include the pair n-gram WFST baseline.
