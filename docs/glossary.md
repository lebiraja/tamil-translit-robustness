# Glossary (plain-language, for reading the docs and the paper)

| Term | Meaning |
|---|---|
| Transliteration | Writing the sounds of a word in another script (here Latin letters to Tamil letters), not translating the meaning |
| Romanization / Tanglish | Typing Tamil with English letters, for example "vanakkam" for வணக்கம்; "Tanglish" is the informal, inconsistent version people use on phones |
| Dakshina | Google's dataset of romanized South Asian languages; our Tamil part is formal Wikipedia text romanized by native speakers on request |
| Aksharantar | AI4Bharat's very large transliteration dataset (26M pairs across 21 languages), mostly mined from the web |
| IndicXlit | AI4Bharat's pretrained transliteration model (about 11M parameters) trained on Aksharantar |
| Lexicon | A word list; here pairs of (romanized spelling, Tamil word) |
| Seq2Seq | A model that reads one sequence (the romanized letters) and writes another (the Tamil letters) |
| Attention | The mechanism that lets the decoder look back at the relevant input letters while writing each output letter |
| BiLSTM | Bidirectional LSTM, a recurrent network that reads the input left-to-right and right-to-left |
| Transformer | Attention-only encoder-decoder (Vaswani 2017); no recurrence |
| Character-level | Model works on single letters, not words or subwords |
| Beam search | Decoding that keeps the best k partial outputs to produce a ranked list of candidates (top-1, top-5, ...) |
| CER | Character error rate: letter-level edit distance divided by reference length; lower is better |
| WER | Word error rate: share of wrong words |
| Top-1 / top-k accuracy | Share of inputs whose correct output is the first (or among the first k) candidates |
| MRR | Mean reciprocal rank of the correct candidate |
| Noise operator | A rule that corrupts the romanized input the way people type (drop vowels, collapse doubled letters, etc.) |
| V-DROP, V-LEN, GEM, DIGRAPH, KEY, REPEAT, MIX | Our noise operators: vowel drop, long-to-short vowel collapse, geminate (double consonant) collapse, th/t-style swaps, adjacent-key typos, letter elongation, random combination |
| Paired benchmark | Every noisy test item has its clean version and gold answer, so degradation is measured exactly |
| Augmentation | Adding corrupted or synthetic training examples to make the model robust |
| Back-transliteration | Using a Tamil-to-Latin model to generate new Latin spellings for Tamil words (synthetic training pairs) |
| Held-out noise type | A noise type left out of training and used only at test time, to check the model generalizes |
| Seed | The random-number starting point; we run several seeds and report mean and spread |
| Leakage | Test data (or near copies) sneaking into training, making results look better than they are |
| Lemma / stem disjoint | Dakshina's splits share no root words; Aksharantar training breaks this, so we treat it separately |
| Reproduction gate | Our check that we match published baseline numbers before running new experiments |
| Leica | Lebi's lab server with the RTX 5070 (12 GB) used for long training runs |
| IA3 | The internal assessment this project is for |
| D1 to D10 | Decision numbers in `DECISIONS.md` |
| C1 to C8 | Novelty candidates in `research/NOVELTY_CANDIDATES.md` (we do C1, C2, C3; C4 optional) |
