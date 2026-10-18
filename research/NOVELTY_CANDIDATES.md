# Novelty candidates — Tanglish → Tamil, char-level Seq2Seq on Dakshina

Ranked by (value to a publishable paper) × (feasibility in one semester on one student GPU) × (confidence it is genuinely new). "Unexplored?" reflects what I could and could not find in the 32 papers read plus targeted web searches on 2026-10-18; absence of evidence is not proof. All citations refer to notes in `notes/`.

**Compute reality check.** Dakshina Tamil training lexicon = 25,000 native words, 68,218 (native, romanized) pairs (measured by the dataset teammate, see `DATASET.md`). Word-level BiLSTM / small Transformer models of 2–6M parameters train in tens of minutes to ~1.5 h on a single RTX 2080 Ti for 279k pairs (Moran & Lignos 2020), so 5–10 seeds × several configurations is affordable. The native-script Tamil Wikipedia (1.14M sentences) is available for LMs and synthetic data. Nothing below needs a model larger than ~10M parameters, except the optional ByT5-Small comparison.

**Recommended paper:** C1 (benchmark/protocol) + C2 (variation-aware augmentation) + C3 (controlled architecture comparison) as the core, C4 as an extra section. This gives a coherent story: *"Clean Dakshina accuracy overstates real-world Tanglish performance; here is how much, why, which architecture degrades least, and how to fix it cheaply."*

---

## C1 (rank 1). A paired robustness benchmark for informal Tamil romanization: Tamil-specific noise taxonomy + a small human-typed "WhatsApp-style" test set

**Gap.** No controlled Tamil robustness evaluation exists. Azam 2025 hand-noised only 100 words per language, unpaired with the clean set, and included trivially removable case noise; IndoNLP-2025 has a clean vs ad-hoc split but no Tamil and does not specify how the ad-hoc data were produced (Sumanathilaka 2025); the only Dravidian measurement is Malayalam (CER 7.4 → 22.7; Baiju 2024); TAMZHI (Herath 2024) characterises Tamil shorthand from a 215-user survey but evaluates no neural model on 700 mixed items. Human romanizations differ systematically from machine ones (LID accuracy 80.4% human vs 96.0% synthetic; Madhani 2023 LID), so synthetic noise alone is not enough.

**What to build.**
1. *Noise taxonomy (parameterised, severity p ∈ {0.1, 0.2, 0.3, 0.5})*, each operator grounded in a cited observation:
   - V-DROP: delete non-initial vowels ("kanakkil" → "kankl"; TAMZHI Table I; Benton 2025 "implicit vowel realization").
   - V-LEN: long/short vowel collapse (aa→a, ee/ii→i, oo→o, uu→u) (Wolf-Sonkin 2019 "long vowels … sometimes represented by doubling … but often not").
   - GEM: geminate collapse (kk→k, tt→t, pp→p, ll→l) (Wolf-Sonkin 2019; Benton 2025 "gemination").
   - DIGRAPH: th↔t, dh↔d, ch↔c/s, sh↔s, zh↔l/z, optional 'h' (Wolf-Sonkin 2019 aspiration; TAMZHI Table II ழ→zha/la, த→tha/ta).
   - KEY: adjacent-key QWERTY substitution / Gaussian tap noise (Wolf-Sonkin 2019 §4.2; Belinkov & Bisk 2018 "Key").
   - REPEAT: elongation ("semmaaa") (Xue 2022 "Repetitions"; Mandal 2018 elongation trimming).
   - MIX: random combination (Karpukhin 2019 "balanced diet").
   Apply to the Dakshina Tamil **test** romanizations so every noisy item is paired with its clean version and gold Tamil reference.
2. *Human-typed set (the novel data contribution)*: show 1,000–1,500 Dakshina test words in Tamil script to the three team members (and ideally 5–15 classmates, ~100 words each) and ask them to type them "as you would on WhatsApp, quickly, without correcting" — the collection protocol Hellsten et al. 2017 used for their proprietary Tamil keyboard test set. Gives naturally noisy, paired inputs with gold references. Optionally add 300–500 tokens sampled from TamilMixSentiment (Chakravarthi 2020) annotated with native-script targets to probe colloquial forms (see risk).
3. *Metrics*: top-1, top-5, CER (Roark/Kirov definitions), ΔCER and relative accuracy (noisy/clean) per operator and severity; degradation curves; and **validation of the synthetic noise model** = rank correlation between systems' synthetic-noise degradation and their human-set degradation (does synthetic noise predict real robustness?).

**Experiment that proves it.** Evaluate pair-n-gram WFST, BiLSTM-attention, small Transformer (and optionally IndicXlit as an external reference, since it is public) on clean / each-noise / human sets. Expected finding (hypothesis): large drops for V-DROP and GEM, small for KEY; human-set degradation between the two.

**Risks.** Few human typists → idiosyncratic set (report per-typist variance, call it a probe set); typing from Tamil-script prompts may still be more careful than real chat; colloquial-vs-literary target ambiguity for TamilMixSentiment tokens (needs an annotation guideline; keep it a separate small set). Ethics: typists' consent; no personal data.

**Unexplored?** I found no paired, taxonomy-based robustness benchmark for Tamil romanized→native, and no public human-typed Tanglish set with native references. Hellsten 2017 built one but it is proprietary and evaluated only FST keyboards. Confidence: fairly high that it is new for Tamil; the general idea (synthetic+natural noise evaluation) is established in MT (Belinkov & Bisk 2018).

---

## C2 (rank 2). Variation-aware training: sampled back-transliteration vs Tamil-phonological noise vs random character noise

**Gap.** Models trained on Dakshina/Aksharantar see few informal variants (Aksharantar 1.011 romanizations per word; Benton 2025). Baiju 2024 names "fine-tuning … with adhoc typing patterns" as future work without doing it. Benton 2025 shows sampling romanizations from a k-best romanizer massively improves *romanized LID*, beating bigger models; Kirov 2024 used sampled simulation only for *sentence-level* fine-tuning; Karpukhin 2019 found random char noise helps typos but not social-media style variation; Belinkov & Bisk 2018 found natural noise is phonological and that noise types do not transfer. Nobody has compared these augmentation families for word-level transliteration robustness.

**Experiment.** Train the same model (both BiLSTM and Transformer from C3) under:
- A0: Dakshina lexicon only (baseline).
- A1: + random char noise diet on the Latin side (60% clean / 10% each del-ins-sub-swap, resampled each epoch; Karpukhin 2019).
- A2: + Tamil-phonological noise (C1 operators V-DROP, V-LEN, GEM, DIGRAPH), resampled each epoch.
- A3: + sampled back-transliteration: train a native→Latin model on the Dakshina lexicon, romanize native words from the Tamil Wikipedia training text by sampling from its 8-best (temperature 1, as Benton 2025/Kirov 2024), add as synthetic pairs (Sennrich 2016 back-translation analogue).
- A4: A2 + A3.
- Control: same number of extra *clean* pairs (to separate "more data" from "more variation").
Evaluate on clean test, every C1 noise type, **held-out noise types not used in training** (e.g. train A2 without GEM, test on GEM), and the human set.

**Proof.** A2/A3 reduce human-set CER relative to A0 and A1 with ≤0.5 CER loss on clean (target set by Karpukhin's <1 BLEU clean cost); generalisation to the held-out operator and to the human set shows it is not just matching the generator.

**Risks.** Train/test leakage of the noise generator (mitigated by held-out operators and the human set); A3 synthetic romanizations may be too regular (the 1-best failure in Benton 2025 — hence sampling); vowel-dropped inputs are genuinely ambiguous ("knkl" could map to several words), so the ceiling is unknown — report oracle top-k.

**Unexplored?** Not found for Tamil transliteration. Sampled back-transliteration is known (Kirov 2024 sentence-level; Benton 2025 LID), so the novelty is the controlled comparison and robustness evaluation, not the mechanism. Confidence: moderate-high.

---

## C3 (rank 3). Char BiLSTM-attention vs small Transformer, matched for parameters and tuning budget, on clean **and** noisy Tamil input

**Gap / conflict.** Roark 2020 (5 seeds): LSTM best Tamil CER (8.4 vs 9.4, Transformer std 0.52). Kirov 2024 (25 seeds, same setup): Transformer 8.2 vs LSTM 8.6, and equal after ensembling. Moran & Lignos 2020: Transformer significantly better but with 2.7× more parameters. Wu et al. 2021: Transformer only wins at batch ≥128 — neither Dakshina paper tuned this. Kirov's EMD analysis suggests LSTM k-best lists better match human variant distributions. No one has compared robustness to noisy input.

**Experiment.** Three parameter budgets (~1M, ~3M, ~8M); for each, BiLSTM + Bahdanau/Luong attention vs pre-LN Transformer; equal tuning budget (e.g. 20 random-search trials each over lr, dropout, batch ∈ {64…512}, warmup, label smoothing); then 5–10 seeds of the best config; report mean ± sd, Kruskal–Wallis/Dunn or paired bootstrap (Moran 2020 methodology). Measure clean CER/acc, degradation slopes on C1 noise, human-set CER, plus training time and CPU latency. Optional: ByT5-Small fine-tune as a pretrained reference (Xue 2022), with Kirov's outlier pruning.

**Proof.** A statistically supported statement of the form "at ≤X M parameters, architecture A is better on clean but B degrades less under V-DROP" (or "no significant difference", which would itself resolve the Roark/Kirov conflict as seed noise).

**Risk.** Null result; mitigate by framing as a careful replication + robustness study. Hyperparameter search cost (still cheap at word level).

**Unexplored?** Clean comparison: done several times with conflicting results (so not novel alone). Matched-budget **plus noise robustness** for Tamil: not found. Confidence: moderate.

---

## C4 (rank 4). Does LM/lexicon-constrained decoding rescue noisy Tanglish?

**Gap.** LM help is large on clean input — unigram rerank +10.4 on Tamil (Madhani 2023: 68.10 → 78.53), word-level LM 27.2 → 17.6 sentence WER (Kirov 2024), nearest-lexicon snapping 51% → 90% for noisy Bengali (Mandal 2018) — but no one reports whether it recovers *noisy-input* errors for Tamil. Tamil's agglutination makes hard closed-vocabulary constraints risky (Roark 2020: noisy channel loses on ta/ml).

**Experiment.** On the C3 models: (a) beam k = 10 + unigram rerank F = αT + (1−α)P (Aksharantar), word unigram from Tamil Wikipedia training text; (b) shallow fusion with a char-level Tamil LM, log p = log p_xlit + β log p_LM (Gulcehre 2015); (c) soft trie constraint: bonus for prefixes in a Wikipedia vocabulary trie with an OOV escape (cf. Wolf-Sonkin 2019 pruned-trie OOV model). Tune α/β on dev; evaluate gains separately on clean / each noise / human set and on in- vs out-of-vocabulary references.

**Proof.** Larger absolute gains on V-DROP/GEM inputs than on clean would show the LM supplies exactly the information the noise removes; OOV breakdown shows the cost of constraints for agglutinative forms.

**Risk.** Domain/register mismatch (Wikipedia LM vs colloquial Tanglish; Kirov 2024 found mC4 LMs *hurt* Tamil); gains may simply mirror clean gains.

**Unexplored?** Reranking itself is known; noise-conditional analysis for Tamil not found. Trie-constrained neural beam search for Indic transliteration: no paper found (web search returned only dictionary reranking in AI4Bharat tooling). Confidence: moderate.

---

## C5 (rank 5). Accuracy–size–latency Pareto for an on-device Tamil transliterator (distillation + quantisation)

**Gap.** Deployed systems are FST-based under ~10 MB / ≤20 ms constraints (Hellsten 2017; Wolf-Sonkin 2019); neural Indic transliterators report accuracy but not size/latency (IndicXlit 11M params). Kim & Rush 2016 show Seq-KD students are much faster with greedy ≈ beam.

**Experiment.** Teacher = best C2/C3/C4 system; students = tiny BiLSTM (≤0.5M) and tiny Transformer; Seq-KD on Dakshina + Wikipedia words; int8 post-training quantisation; measure CPU (and Android, if available) latency per word, model MB, clean/noisy/human CER. Does robustness survive distillation?

**Risk.** Mostly engineering; novelty is moderate (application of known techniques). Phone benchmarking may be fiddly.

**Unexplored?** Not found for Tamil transliteration; generic technique well known. Confidence: moderate on "new for Tamil", low on methodological novelty.

---

## C6 (rank 6). Non-autoregressive CTC transliteration with input upsampling

**Gap.** Rosca & Breuel 2016 found CTC with epsilon insertion competitive with attention (EN→JA CER 18.1 vs 20.2). CTC is monotone (fits transliteration) and fast. Untested on Dakshina.

**Experiment.** BiLSTM/Transformer encoder + CTC, input upsampled ×2–3 (needed because vowel-dropped inputs like "knkl" are shorter than their Tamil code-point sequences — CTC requires output ≤ input length; *inference*), vs attention seq2seq: clean/noisy CER, latency.

**Risk.** Shorthand input stresses the length constraint; may underperform; conditional-independence of CTC may hurt vowel decisions.

**Unexplored?** Not found on Dakshina/Tamil. Confidence: moderate; value moderate.

---

## C7 (rank 7). Label-noise audit of the Dakshina Tamil lexicon and its effect on small models

**Gap.** Kirov 2024 (App. B) found mislabelled pairs (e.g. "tikket" ↔ wrong constituent) and that pruning the worst 10% fixes ByT5 on Tamil (12.7 → 7.9 CER) but does not change small models. Effect on robustness and on evaluation (noisy *test* references) not studied.

**Experiment.** Score pairs with a cross-validated native→Latin model or a colloquial romanizer (Aksharamukha, as Kirov did); manually check a sample of the top-scored pairs in train **and test**; report test-set error rate; re-evaluate models on a cleaned test subset; check whether pruning helps under noise.

**Risk.** Small effect; mostly a dataset-quality contribution. **Unexplored?** Partially explored (Kirov 2024). Use as a section, not the headline.

---

## C8 (rank 8, high risk). Colloquial-Tamil targets for real Tanglish

**Gap.** Real Tanglish (TamilMixSentiment) is often *spoken* Tamil ("parthavanga", "podunga"), while Dakshina targets are literary Wikipedia Tamil. No benchmark defines the right native-script target for colloquial input.

**Experiment.** Annotate 300–500 real Tanglish tokens with both a colloquial-faithful and a normalised-literary Tamil reference; measure which one models trained on Dakshina produce and how CER changes.

**Risk.** Annotation guideline disputes; small n; licensing of scraped comments (not verified). **Unexplored?** Not found. Good discussion material; risky as a main claim.

---

## What I could not verify
- Whether the IndoNLP-2025 shared task or later work released a Tamil ad-hoc set (the overview lists only si/bn/gu/hi/ml).
- Whether TAMZHI's 215-user typing-pattern data or its test set are public.
- Publication venues of several arXiv-only papers (Benton 2025, Azam 2025, Gharami 2025).
- Any 2026 work on this exact problem: searches up to 2026-10-18 found only an undated GitHub project (Dakshina-trained char Seq2Seq for Thanglish, no robustness evaluation) and a 2026 English–Tamil MT paper mentioning Tanglish noise; neither does C1–C3.
