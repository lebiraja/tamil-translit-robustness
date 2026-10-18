# DECISIONS

Locked decisions. Change one only by adding a new row, never by silent edit.

| # | Date | Decision | Why |
|---|---|---|---|
| D1 | 2026-10-18 | Topic: #34 Tanglish-to-Tamil transliteration, char-level Seq2Seq, Google Dakshina (Tamil) | Lebi's Tamil strength; new area (seq2seq); published baselines to beat |
| D2 | 2026-10-18 | Novelty scope: **C1 + C2 + C3** (see `research/NOVELTY_CANDIDATES.md`). C4 (LM reranking) only if time is left | 2-week deadline; coherent story |
| D3 | 2026-10-18 | Models: char BiLSTM+attention vs small Transformer, matched ~3M params, equal tuning budget, 5 seeds each | Resolves Roark 2020 vs Kirov 2024 conflict; fits RTX 5070 |
| D4 | 2026-10-18 | Human-typed test set: 3 team members, ~500 Dakshina-test words each (~1,500 total), typed WhatsApp-style from Tamil-script prompts | Real informal input with gold references; Dakshina is not chat text |
| D5 | 2026-10-18 | Framing: "informal romanized Tamil" in title, not bare "Tanglish" | Dakshina is formal Wikipedia Tamil romanized on request (DATASET.md); honesty |
| D6 | 2026-10-18 | Paper: IEEE conference format (IEEEtran), LaTeX, refs from `research/refs.bib` | Lebi's choice |
| D7 | 2026-10-18 | Compute (corrected after reading `/home/lebi/workspace/networks/dscs-lab`): laptop `rog` = RTX 4050 6 GB (dev, small tests); lab server **Leica** (`ssh airoot`) = RTX 5070 12 GB Blackwell, i7-14700, 15 GB RAM, 237 GB free, Ubuntu 24.04, Docker empty, no nvcc. Long runs on Leica; PyTorch there needs a CUDA 12.8+ build for sm_120 | Lebi's hardware; earlier note wrongly said the laptop had the 5070 |
| D8 | 2026-10-18 | Deadline: Lebi says ignore it; the staff's real date is unknown. Keep a soft internal target of ~2026-11-01 so the work stays scoped | Lebi (later message) |
| D10 | 2026-10-18 | Long training runs go on the lab system; laptop RTX 5070 for development. Lebi and Claude do the work; no teammate split needed in docs | Lebi |
| D9 | 2026-10-18 | Staff only asks for the deliverable; we follow our own research method (full experiments, statistics, citations) | Lebi |

## Still open (need Lebi)
- Leica kernel pin is not permanent (see below); ask Lebi before applying it or rebooting.
- Who types the 1,500-word human set (D4 assumes the 3 team members).
- ~~Aksharantar overlap~~ resolved: use `data/aksharantar-tamil/tam_test.no_dakshina.tsv` (4,335 rows); see `docs/datasets/`.
