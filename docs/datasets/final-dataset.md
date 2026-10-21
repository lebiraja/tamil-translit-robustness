# Final dataset (v1, generated 2026-10-21)

Everything below is derived deterministically from the sources in `docs/datasets/README.md` by `scripts/prepare_data.py`, `scripts/synthesize_a3.py` and `scripts/build_wa_set.py`. `data/` is gitignored; regenerate with those scripts. Checksums for the Dakshina inputs: `data/dakshina-ta/SHA256SUMS`.

## Training sources
| ID | What | Size | How made |
|---|---|---|---|
| Dakshina train | real human romanizations, 25,000 words | 68,218 pairs | official lexicon (byte-range fetch) |
| A1 | random character noise on the romanization | online, re-drawn every epoch | `augment.Policy("random")` |
| A2 | Tamil-phonological noise (V-DROP, V-LEN, GEM, DIGRAPH mix) | online | `augment.Policy("phon")`; held-out variants A2-noGEM, A2-noVDROP |
| A3 | back-transliteration: 60,000 pool words romanized by a Dakshina-trained Tamil-to-Latin BiLSTM (3 temperature-1 samples per word, quality-filtered) | 123,488 pairs (17,828 degenerate samples dropped) | `data/synth/a3_sampled.tsv` |
| CTRL | same 60,000 words, one greedy romanization each | 60,000 pairs | `data/synth/a3_greedy.tsv` |
| A4 | A2 + A3 | | |
Pool rule: IndicXlit top Tamil words, pure Tamil script, length 2 to 20, not in any Dakshina split, not in the independent Aksharantar test, and no 5-code-point stem prefix shared with any Dakshina dev/test or independent-test word (removed 30,150 + 46,652 of 137,748 candidates; 60,000 kept). A3 romanizations are machine-made: say so in the paper.

## Evaluation sets
| ID | Size | Notes |
|---|---|---|
| Dakshina dev | 6,827 pairs, 6,806 distinct inputs | early stopping and tuning only |
| Dakshina test | 6,864 pairs, 6,833 distinct inputs | clean test |
| Noisy test (C1) | 28 sets, each 6,833 inputs | ops V-DROP, V-LEN, GEM, DIGRAPH, KEY, REPEAT, MIX x severity 0.1/0.2/0.3/0.5; seed 20261018; realised edit rates in `data/synth/noisy_test/manifest.json` |
| Independent | AK-Freq 2,607; AK-NEI 991; AK-NEF 706 inputs (+ AK-all) | Aksharantar test rows that are not Dakshina test rows and whose word is in no Dakshina split |
| WA (private) | WA-TA 370 words, WA-TAq 43 ambiguous | real chat words from Lebi's private WhatsApp exports; Tamil spellings model-labelled (Sonnet); becomes human-verified after Lebi checks `data/private/wa_verify.tsv`; never committed |
| Human-typed | about 1,500 words | pending (who types); sheets from `scripts/make_human_prompts.py` |
| Haiku pilot | 300 dev words x 3 | NOT used for training: 34.4% exact match to attested human spellings, 77.2% within one edit |

## Rules in force
Never train on IndicXlit sentence pairs, gowtham58, Mendeley, sanujen (D12). Test sets are never cleaned silently. WA data stays on Lebi's machines (D16/D17); only aggregate numbers are published.
