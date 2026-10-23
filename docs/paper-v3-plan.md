# Paper v3 plan (restructure after the staff conversation)

Status: PLAN ONLY. No LaTeX has been changed. v1 and v2 stay untouched in `paper/releases/`. Written 2026-10-23.

Sources: the two voice notes in `ignore-it/` (transcribed with agy, 2026-10-23), `paper/` (v2 sources), `docs/paper-claims-map.md`, `docs/results.md`, `research/KNOWLEDGE_BASE.md`, `research/notes/`.

## 1. What the staff asked for (from the audio)

| # | Instruction | How v3 satisfies it |
|---|---|---|
| S1 | Section order: Abstract, Intro, (Related Work), Proposed Methodology, Results and Discussion, Conclusion | Exactly six sections, no others (limitations become a paragraph inside Results and Discussion) |
| S2 | Abstract about 150 words: why this project, who it reaches, which models, the performance numbers | Draft in section 4 (145 words) |
| S3 | Intro as a short story line (who needs it, how it helps), then cite papers with their issues and say which we fix | Tanglish-typist story, then gap paragraph, then contributions |
| S4 | Related Work grouped by model type (ML, DL, AI), at most about 1.5 lines per paper, pros and cons, focus on the cons we fix, polite tone | Table plus short paragraphs, section 5 |
| S5 | Fix only one or two gaps, not everything | Primary gaps G1 and G2 below; everything else is supporting |
| S6 | Comparison tables and charts go at the end of Results and Discussion | Final subsection "Summary comparison" holds the all-conditions table and the figure |

Note on S4: the staff suggested praising while criticising. We do that, but every stated con must be something we read in the paper or in our own measurement. No claim about a paper that we did not verify.

## 2. The two gaps we claim (decision needed from Lebi: confirm)

- **G1 (benchmark gap).** No public, paired, severity-graded robustness benchmark for Latin-to-Tamil word transliteration (KNOWLEDGE_BASE section 5, gaps 1 and 3). Closest work: Azam 2025 (100 hand-noised words, unpaired), TAMZHI (rules, 700 items, no neural model), IndoNLP 2025 and Baiju 2024 (Malayalam, vowel-omitted only).
- **G2 (remedy gap).** Which training remedy helps, and does it transfer to unseen error types? Sampled back-transliteration plus Tamil-phonological noise is untested at word level for Tamil (gap 4). Includes the "words versus spelling variety" control.

Supporting (reported, not claimed as the contribution): architecture comparison under noise (the Roark-vs-Kirov conflict) and the 12.6 MB deployment model.

## 3. Section skeleton and word budgets (target 9 IEEE pages, about 3,800 body words plus tables and figures)

| Section | Words | Content | Replaces in v2 |
|---|---|---|---|
| Abstract | 145 to 150 | section 4 | abstract |
| I. Introduction | 400 | story, gap, contributions, findings in one line | introduction |
| II. Related Work | 450 plus Table I | section 5 | related |
| III. Proposed Methodology | 1,000 | A. data and benchmark, B. noise operators (Table II), C. models and training, D. augmentation conditions, E. metrics and statistics, F. reproduction check | data, method, experiments |
| IV. Results and Discussion | 1,700 | A. baseline and clean, B. RQ1 damage, C. RQ3 remedies, D. held-out transfer, E. RQ4 architecture, F. deployment model, G. threats to validity (the old limitations, shortened), H. summary table and figure | results, final_model, discussion, limitations |
| V. Conclusion | 200 | findings, future work, reproducibility | conclusion |

Figures to keep (6 exist): noise curves, architectures, augmentation, held-out, tuning (move to methodology or drop), v2. Tables: ops, c3, c2, stats, v2. Staff rule S6: put the c2/c3 comparison table and one summary figure last. Re-check that nothing exceeds the page limit (unknown, see section 8).

## 4. Abstract draft (145 words; every number is in the claims map)

> People type Tamil in Latin letters, yet transliteration models are trained and tested on carefully romanized text, so their accuracy under fast, informal typing is unknown. We release a paired, seeded benchmark of seven Tamil-specific noise operators at four severities, built from the Dakshina test lexicon, and evaluate 110 character-level models (BiLSTM with attention and Transformer, 1M to 8M parameters, five seeds). Our implementation reproduces the published development CER of 8.4. Vowel dropping and keyboard slips raise character error rate (CER) from about 9 to 22-24 at severity 0.3; other operators cost 1 to 3 points. Tamil-phonological noise training cuts BiLSTM vowel-drop CER from 24.0 to 17.7 but does not transfer to a held-out operator; adding sampled back-transliterations gives the lowest mixed-noise CER (21.8 against 25.5). Fine-tuning that Transformer on 2.4M pairs gives a 12.6 MB model with mixed-noise CER 17.8 at unchanged clean accuracy.

Checks done: 22-24 = V-DROP 0.3 (21.7 to 24.0) and KEY 0.3 (21.4 to 22.1); "1 to 3" = V-LEN/GEM/REPEAT/DIGRAPH +1.0 to +3.3 (rounds to 3); 25.5 = BiLSTM A0 MIX 0.3, 21.8 = A4 (both archs 21.82/21.79); 17.8 = v2 17.77. To state in the body, not the abstract: v2's noise numbers are not held-out.

## 5. Related Work plan (grouped as the staff asked)

All entries are from `research/KNOWLEDGE_BASE.md`, which quotes the PDFs; the last column is the gap sentence we may write. Group names: "Rule-based and statistical (ML)", "Neural (DL)", "Pretrained and large language models (AI)", then one short block on noise and augmentation.

| Group | Paper | Pro (as read) | Con that matters to us |
|---|---|---|---|
| ML | Brahmi-Net 2015 | Rule+SMT system for many Indic pairs | Tamil collapses voiced/aspirated plosives; no noisy-input test |
| ML | Hellsten 2017 | On-device WFST, real phone-typed Tamil test, WER 26.2 to 22.6 | Test set is proprietary, so nobody can reproduce it |
| ML | Wolf-Sonkin 2019 | Typology of romanization variation | No neural model, no Tamil benchmark |
| ML | Herath 2024 (TAMZHI) | 215-user survey of Tamil shorthand, rule-based, 93% char / 70% word on 700 items | No neural comparison, small mixed test set |
| DL | Roark 2020 | Dakshina data, strong BiLSTM/Transformer baselines, CER 8.4/9.4 | Clean, formal, elicited text only; 5 seeds |
| DL | Kirov 2024 | 25 seeds, context, ensembles; Transformer 8.2 vs LSTM 8.6 | Clean input only; reverses Roark's ranking |
| DL | Madhani 2023 (Aksharantar) | 26M pairs, large accuracy gain from mined data | About one romanization per word; clean; Dakshina overlap (we filter it) |
| DL | Kunchukuttan 2021 | Multilingual Indic model | Tamil script under-specified; clean input |
| DL | Baiju 2024 / Sumanathilaka 2025 | Show the ad-hoc drop (Malayalam CER 7.4 to 22.7) | Malayalam, not Tamil; no severity levels |
| DL | Moran 2020, Wu 2021 | LSTM vs Transformer studies | Not Tamil, not noisy; parameter and batch-size confounds |
| AI | Azam 2025 | LLM benchmark; GPT-4.5 76.61% top-1 on clean Tamil | Only 100 hand-noised words, unpaired |
| AI | Xue 2022 (ByT5) | Byte models robust to some noise | Not tested on Tamil informal romanization (Dakshina clean only) |
| Noise | Belinkov 2018, Karpukhin 2019, Benton 2025 | Noise training transfers poorly; sampled variants help LID | Not transliteration, not Tamil |

Table I (end of Related Work) = this table compressed to: system group, dataset/noise, what is missing. The paragraph after it states G1 and G2 in two sentences.

Correction to carry into v3: v2's intro says "every system, including large language models, falls to about 20% top-1 on 100 hand-noised Tamil words". The knowledge base shows GPT-4o fine-tuned reached 37. Write "most systems fall to about 20% (a fine-tuned GPT-4o reaches 37)".

## 6. Claims inventory (what v3 may state, and where the number comes from)

Everything is in `docs/paper-claims-map.md` already. Before writing, re-run `scripts/make_tables.py` and `scripts/make_figures.py` so no number is typed by hand. Headline claims:

1. Reproduction: dev CER 8.39/8.41/8.43 (BiLSTM) vs 8.4; Transformer 3M 8.49 vs 9.4/8.2.
2. Damage at p=0.3: V-DROP +12.4 to +15.0, KEY +12.4 to +13.1, MIX +14.9 to +16.5, DIGRAPH +3.2 to +3.3, REPEAT +1.7 to +2.0, V-LEN/GEM +1.0 to +1.1.
3. A2 vs A0: BiLSTM V-DROP 17.70 vs 24.03; costs +0.83 clean. No transfer: noVDROP 24.97.
4. A3 gain equals CTRL gain on clean (+0.03, CI [-0.08, +0.13]); A3 vs CTRL on MIX -0.58 (BiLSTM), -0.81 (Transformer).
5. A4 best on MIX: 21.82 / 21.79; clean cost +0.35 / -0.03.
6. Architectures: tie at 3M clean (-0.01, CI [-0.15, +0.12]); Transformer lower on MIX at every size (+0.42, +1.30, +0.28 BiLSTM minus Transformer).
7. v2: test 8.93, MIX 17.77, KEY 15.40, AK-all 10.76; not held-out.

## 7. Problems found in v2 that v3 must fix (precision)

1. **Split mismatch in the reproduction paragraph.** v2 says our top-1 (63.3%) is below the published 65.3%. Our 63.3 is a test top-1; Roark's 65.3 is a dev top-1. `results/summary/c3_clean.csv` has no dev top-1 column. Fix: compute dev top-1 from `results/c3/*.json` if stored; otherwise delete the comparison and say we compare CER only.
2. The Azam 2025 sentence above.
3. Abstract is 290 words; the staff want about 150.
4. The paper says "informal romanized Tamil" in places and "Tanglish" in others; keep "informal romanized Tamil" in the title/abstract (D5) and define Tanglish once in the intro story.
5. Limitation text mentions a "supervisor bug" incident in detail (about 120 words). Keep the facts (33 of 72 runs overlapped, 1 of 110 mismatched, retrained) but shrink to 2 sentences.
6. `refs.bib` entries that are arXiv-only still need venue details (HANDOVER item 3); verify before the final compile.
7. Real chat is still "preliminary" because `data/private/wa_verify.tsv` is unverified. See decision 3 in section 8.

## 8. Decisions needed from Lebi before writing

1. **Confirm G1 + G2 as the two gaps** (section 2).
2. **Venue and page limit.** Unknown. Which conference or journal, and what is the limit? v3 targets 9 pages until told otherwise.
3. **RQ2 (real chat).** Option A: write v3 now with real chat as a clearly marked preliminary check (honest, ready now). Option B: first verify `wa_verify.tsv` (413 words) and run the evaluation, then add a real-typing result. B is a stronger paper; A does not block on it.
4. **Title.** Keep v2's title, or use a shorter one such as "Robustness of Character-Level Transliteration to Informal Typing in Romanized Tamil".
5. **Plagiarism check.** Run the new PDF through whichever checker the staff uses; v3 reuses no sentences from v1/v2, but numbers and method names are necessarily the same.

## 9. Execution order once decisions 1 to 4 are answered

1. Regenerate tables and figures from `results/`; resolve issue 1 above.
2. Write Methodology, then Results and Discussion (the content), then Related Work, then Introduction, then Conclusion, then Abstract last.
3. Compile with `xelatex main && biber main && xelatex main && xelatex main`; need exit 0, no undefined citations or references, no overfull boxes, page count within the limit.
4. Cross-check every number in the PDF against `docs/paper-claims-map.md`; update the map for any new number.
5. Save as `paper/releases/paper-v3.pdf`, commit as `docs:`, prepend `STATUS.md`, bump `HANDOVER.md` (move Current to Previous first).
