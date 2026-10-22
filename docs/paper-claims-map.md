# Paper claim -> evidence map

Every quantitative statement in `paper/` and where it comes from. All numbers are produced by `scripts/aggregate.py` into `results/summary/` (and the tables/figures by `scripts/make_tables.py`, `scripts/make_figures.py`).

| Claim (paper section) | Number | Evidence file | Where |
|---|---|---|---|
| Reproduces published dev CER (Setup) | BiLSTM dev 8.39 / 8.41 / 8.43 vs Roark 8.4; Transformer 3M 8.49 vs 9.4 / 8.2 | `results/summary/c3_clean.csv`, `research/KNOWLEDGE_BASE.md` 3.1 | Table `tab_c3` |
| Gate (untuned, 1 seed, greedy) | 8.95, 9.38 | `results/gate/*.json` | Setup text |
| 3M tie on clean | test CER 9.00 vs 9.01, diff -0.01 CI [-0.15,+0.12] | `results/summary/stats.json` (bootstrap) | Results 5.1, `tab_stats` |
| Vowel drop and keyboard slips are the damaging operators | V-DROP +15.0/+12.6 (1M), KEY +12.4..+13.1, MIX 24-25 at p=0.3 | `c1_degradation.csv` | Fig noise curves, 5.2 |
| V-LEN, GEM, REPEAT, DIGRAPH mild | +1.0..+1.1, +1.7..+2.0, +3.2..+3.3 | `c1_degradation.csv` | 5.2 |
| Realised noise strength | words changed %, char-edit % | `data/synth/noisy_test/manifest.json` | `tab_ops`, Data |
| Transformer better under MIX | BiLSTM minus Transformer +0.42/+1.30/+0.28 | `stats.json` | `tab_stats`, 5.3 |
| A1/A2 cost clean accuracy | +0.9/+0.8 (BiLSTM), +0.8/+0.8 (Transformer) | `c2.csv` | `tab_c2`, 5.4 |
| A2 beats A1 on V-DROP, loses on KEY | 17.7 vs 21.7; 23.4 vs 18.6 | `c2.csv` | 5.4 |
| A3 gain = extra words (CTRL equal) | clean 8.67 vs 8.64; A3 vs CTRL +0.03 CI [-0.08,+0.13] | `c2.csv`, `stats.json` | 5.4 |
| A4 best on MIX | 21.82 / 21.79 | `c2.csv` | `tab_c2` |
| No transfer to held-out V-DROP | 24.97 vs 17.70 (A2), 24.03 (A0); Transformer 22.35 / 17.43 / 21.65 | `c2.csv` | Fig held-out |
| Kruskal-Wallis / Dunn | eta^2 0.88-0.93 | `stats.json` | 5.4 |
| Data pool filtering | 137,748 candidates, 46,652 stem overlap, 60,000 kept; 141,316 samples, 17,828 dropped, 123,488 kept | `data/synth/native_pool.stats.json`, `logs_archive/` | Data |
| Incident disclosure | 33 of 72 runs overlapped; 1 of 110 mismatched (8.43 vs 8.49) | `FIXES.md` F3, `logs_archive/eval_mismatch.txt` | Limitations |
| Final model v2 (Deployment model) | dev 8.56, test 8.93, top-1 65.27, AK-all 10.76, MIX0.3 17.77, KEY0.3 15.40 vs parent 8.47 / 9.02 / 63.88 / 10.95 / 21.80 / 23.04 | `results/final/v2-ft-s0.json`, `results/c2/c2-transformer-A4-s1.json` | Table `tab_v2`, Fig. `fig_v2` |
| Preliminary real chat (370 words, model labels, unverified) | CER 25.4 (v1) vs 24.9 (v2); top-1 40.5 vs 39.7; top-5 68.6 vs 71.1 | computed on the laptop from `data/private/wa_test/WA-TA.tsv` (private, not in repo) | Deployment model, Limitations |

Rules: no number is written into the paper by hand; a number not in this table must be added here with its source before it is added to the paper. Literature numbers (Roark 8.4/9.4, Kirov 8.2, Baiju 7.4->22.7, Azam ~20% top-1, Aksharantar 56.0->67.7) come from `research/KNOWLEDGE_BASE.md`, which quotes the PDFs in `research/papers/`.
