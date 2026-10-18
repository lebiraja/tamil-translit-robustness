# Azam et al. 2025 — Beyond Specialization: Benchmarking LLMs for Transliteration of Indian Languages

**Citation.** Gulfarogh Azam, Mohd Sadique, Saif Ali, Mohammad Nadeem, Erik Cambria, Shahab Saquib Sohail, Mohammad Sultan Alam. 2025. "Beyond Specialization: Benchmarking LLMs for Transliteration of Indian Languages." arXiv:2505.19851 (preprint formatted as an IEEE Transactions manuscript; no confirmed venue). Read in full.

## Setup
Word-level romanized→native on 10 languages; Dakshina test + Aksharantar AK-Freq/AK-NEF/AK-NEI (AK-Uni dropped as "missing or incomplete"). Systems: GPT-4o, GPT-4.5, GPT-4.1, Gemma-3-27B-it, Mistral-Large 2402 (few-shot JSON prompts), IndicXlit, and GPT-4o fine-tuned via OpenAI API (Dakshina+Aksharantar; Tamil 92,321 train / 8,824 val). Metrics: top-1 accuracy and mean per-word CER. Tamil test: Dakshina 6,847, AK-Freq 2,608, AK-NEF 829, AK-NEI 1,216.

## Tamil results (Table 3; top-1 % / CER)
| | GPT-4o | GPT-4.5 | GPT-4.1 | Gemma-3 | Mistral-L | IndicXlit | GPT-4o-FT |
|---|---|---|---|---|---|---|---|
| Dakshina | 70.44/.108 | **76.61/.096** | 67.91/.116 | 46.80/.173 | 49.28/.178 | 67.97/.117 | 72.84/.104 |
| AK-Freq | 74.07/.046 | **78.48/.041** | 72.54/.050 | 43.77/.114 | 51.46/.094 | 69.75/.052 | 75.22/.041 |
| AK-NEF | 44.74 | 43.52 | 40.22 | 42.91 | 24.03 | 39.08 | 45.11 |
| AK-NEI | 48.94 | 49.36 | 48.60 | 45.12 | 27.71 | 43.58 | 48.60 |

## Robustness (Table 4) — Tamil
100 common words per language, **manually** noised in two ways: spelling changes preserving pronunciation ("nadiad"→"nadeead", "chaurasiya"→"chaurassia") and inserted upper-case letters ("lowell"→"loveLl"). Tamil top-1: GPT-4o 19, GPT-4.5 22, IndicXlit 20, GPT-4o-FT 37; CER 0.218 / 0.218 / 0.232 / 0.172. I.e. a collapse from ~68–77% clean to ~20% noisy for all models; fine-tuning helps most.

## Issues to flag
- Internal inconsistency: abstract says GPT models "generally outperform … IndicXlit for most instances"; introduction says "IndicXlit model outperforms most LLMs except GPT-4.5".
- Noisy test set is tiny (n = 100/language), hand-made, not released as far as I can tell, and the "case" noise is trivially removable by lower-casing (Dakshina/Kirov lowercase input). No significance testing. Proprietary, non-reproducible API models.
- Noisy and clean test words differ (noisy set is "100 common words"), so the drop is not a paired comparison.

## Relevance to us
- Gives Tamil reference points for very large models (GPT-4.5: 76.61% on Dakshina test) — a ceiling-ish comparison for our small models.
- The robustness section is the only multi-model noisy-input evaluation including Tamil I found; its weaknesses (small n, unpaired, unprincipled noise) define what a better robustness protocol must fix: **paired** clean/noisy versions of the same test words, a **parameterised noise taxonomy with severity levels**, thousands of items, and released code.
