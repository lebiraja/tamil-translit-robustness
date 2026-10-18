# Human-typed informal Tamil test set: protocol (draft, to be confirmed)

Status: **draft**. Locked so far (D4): about 1,500 Dakshina test words, typed by team members WhatsApp-style from Tamil-script prompts. Everything else below is a proposal for Lebi to confirm. Nothing has been collected yet. Lebi will say when to start.

## Why this set exists
No public dataset pairs real informal romanized Tamil with Tamil-script gold (checked 2026-10-18; `docs/datasets/informal-tanglish-datasets.md` section 5). Dakshina is elicited from formal Wikipedia text; Aksharantar is mostly mined at about one romanization per word; real comment corpora (DravidianCodeMix, HopeEDI, Tanglish-Corpus-185k) carry only sentiment/offence labels. A set where people see a Tamil word and type it the way they would on WhatsApp gives naturally noisy input **with a gold reference and a clean counterpart**. It answers RQ2 (does synthetic noise predict real degradation?) and gives the only real-typing numbers in the paper. Prior art for the protocol: Hellsten et al. 2017 (proprietary Tamil keyboard test set).

## What is collected
- **Items:** about 1,500 words sampled from the Dakshina Tamil **test** lexicon (so each has a gold Tamil word and a Dakshina romanization to compare with). Sample with a recorded seed, stratified by word length, excluding obvious proper-noun-only items if Lebi wants a cleaner set (decision needed).
- **Prompt:** the Tamil-script word, shown on a sheet or form. No transliteration hints.
- **Instruction to typists:** "Type this word the way you would type it in a WhatsApp message to a friend, quickly, in English letters. Do not correct yourself, do not look up a spelling, do not use a transliteration tool, no autocorrect."
- **Recorded per item:** typist id (pseudonym such as T1, T2, T3), the typed romanization, item id, the gold Tamil word, timestamp, device type (phone or laptop keyboard), and whether autocorrect was on.
- **Optional second pass:** typists also type 20 to 30 short phrases in their own words (not used for scoring), only to calibrate pattern rates against the real comment corpora.

## Proposed design (confirm with Lebi)
| Item | Proposal | Reason |
|---|---|---|
| Typists | the three team members, about 500 words each | locked in D4; but see the open question below |
| Overlap | 100 words typed by all three, 400 unique words each (1,300 unique words, 1,500 typed items) | measures inter-typist variability; supports the per-typist analysis |
| Order | randomized per typist, fixed seed | avoids fatigue patterns aligned with word order |
| Tool | simple local web form or a spreadsheet; no autocorrect, one word per row | easy and auditable |
| Time | about 1 hour per typist | from the 500-word load |
| Storage | `data/human-typed/typist_<id>.tsv` plus `manifest.json` (seed, sampling rule) | gitignored until consent and de-identification are settled |
| Release | only pseudonymous typed strings and gold words, with consent | Ethics below |

## Open question: who types?
Lebi said "we can complete it by ourselves" and gave no teammate details. A single typist would make the set idiosyncratic and weaken RQ2. Options: (a) three people as locked (preferred); (b) Lebi plus two friends or classmates, about 500 words each; (c) Lebi alone as a smaller 300-word probe, clearly labelled single-typist. Recommend (a) or (b). Decision needed before collection.

## Quality checks after collection
- Remove duplicate submissions and empty rows; keep a log (not silent deletion).
- Spot-check 5 percent for pasted or auto-corrected entries.
- Compute per-typist pattern rates (vowel drop, vowel-length collapse, geminate collapse, digraph swaps, elongation) and compare with the real-comment rates in `docs/datasets/informal-tanglish-measurements.json` (inform the noise model; do not tune the noise model on the **same words** used for the final test, to avoid leakage: calibrate on pattern rates only).
- Report inter-typist agreement on the shared 100 words and the fraction of typed forms equal to the Dakshina romanization.

## Ethics and licensing
- Typists give informed consent (verbal or written) to release pseudonymized typed strings.
- No personal data: words only, no names or messages from private chats. Do not paste real chat messages.
- If the set is released, use a clear license (for example CC BY 4.0), cite Dakshina (CC BY-SA 4.0) for the gold word list and note that Dakshina's license is share-alike (the released set may need CC BY-SA 4.0 for the derived words; check before release).

## Deliverables
`data/human-typed/*.tsv`, a short datasheet in `docs/datasets/human-typed-set.md` (counts, protocol, per-typist stats, limitations), and the paper's dataset section.
