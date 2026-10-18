# Data decisions to confirm with the team / user

Each question lists what it depends on and a default recommendation. The evidence for each is in `DATASET.md`, with the section number given.

1. **Task granularity.** Is the core deliverable *word-level* transliteration (Dakshina lexicon), *sentence-level* transliteration, or both?
   Default: word-level char seq2seq on the lexicon. For sentences, add an optional token-by-token evaluation on the 5k test sentences. No human sentence-level training data exists (§4.2).

2. **How do we phrase the "Tanglish" claim?** Dakshina is elicited romanization of Wikipedia Tamil. It is not chat text, has no colloquial forms, and contains little shorthand or code-mixing (§6). Options:
   - (a) Rename the claim to "romanized Tamil → Tamil script".
   - (b) Keep "Tanglish" and add a real-Tanglish test set.
   - (c) Keep "Tanglish" and add a synthetic-noise robustness study.
   Default: (a) for the main result, plus (c), with (b) if time allows.

3. **Do we build a small real-Tanglish test set ourselves?** For example, 300–1,000 tokens or sentences, either from TamilMixSentiment/DravidianCodeMix comments (licence unverified) or typed by the team or volunteers with consent. The Tamil-script targets would be annotated by the 3 team members.
   This needs agreement on an annotation guideline. The main question is whether colloquial forms (`podunga`) are written as spoken in Tamil script or normalised to literary Tamil (Dakshina references are literary). The time cost must be agreed too.

4. **Extra training data: Dakshina only, or Dakshina + Aksharantar?** Aksharantar adds about 3.2M Tamil pairs (about 80% accurate for the mined part, 97 MB). It would make results incomparable with Roark's Dakshina-only baselines, and it changes the compute budget.
   Default: Dakshina-only as the main setting. Aksharantar would be at most an ablation, and its *test* set would be used only for robustness.

5. **Use of attestation counts.** Options:
   - (a) Each unique pair once.
   - (b) Repeat each pair by its count, as Roark does.
   - (c) Keep only the most-attested romanization.
   Default: (b) to match the baseline, with (a) as an ablation. Avoid (c), because it throws away exactly the spelling variation we want to be robust to.

6. **Cleaning.** Do we drop suspected noisy lexicon pairs (≈0.35% heuristic flags, e.g. `நதி → moolam`) and the misaligned sentence pairs?
   Default: clean **train only**, using a documented rule. Leave dev/test untouched for comparability, but report the size of the affected subset.

7. **Evaluation metrics and reporting.** Confirm: top-1 accuracy (primary), CER computed on NFC Unicode code points, top-3/top-5 from beam search, and any-reference matching for the 29 ambiguous test inputs. Report mean ± std over N seeds; what is N, given our GPU budget? Report test numbers only once.

8. **Which published number do we compare against?** Roark 2020 LSTM numbers are *dev* (CER 8.4, top-1 65.3). Aksharantar's Dakshina-only Transformer numbers are *test* (56.0 monolingual). IndicXlit (68.1) and GPT-4.5 (76.6) use far more data. Default: compare on dev with Roark and on test with Aksharantar's Dakshina-only rows, and quote IndicXlit/LLMs only as an upper reference.

9. **Compute and storage.** We can fetch only the Tamil files (~23 MB via byte ranges) or the full 1.87 GiB tar once. Is the native Tamil Wikipedia text (58 MB gz, 1.14M sentences) in scope, e.g. for a character LM, reranking, or synthetic back-transliteration?

10. **Licence obligations.** Dakshina is CC BY-SA 4.0. If we publish cleaned splits or a derived test set, they must be CC BY-SA with attribution. Are we publishing data, or code only? Is the course report public?

11. **Verification tasks before final numbers** (no decision needed, but someone must own each):
    - Aksharantar overlap: done (DATASET.md §8). Filtered robustness file: `data/aksharantar-tamil/tam_test.no_dakshina.tsv` (4,335 rows; rule: source ≠ Dakshina and NFC native word not in any Dakshina split). Verified.
    - Confirm the Bhasha-Abhijnaanam Tamil count.
    - Decide how to handle the 15 sentences duplicated across dev and test.
