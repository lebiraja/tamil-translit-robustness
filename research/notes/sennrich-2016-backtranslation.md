# Sennrich, Haddow, Birch 2016 — Improving NMT Models with Monolingual Data (back-translation)

**Citation.** Rico Sennrich, Barry Haddow, Alexandra Birch. 2016. "Improving Neural Machine Translation Models with Monolingual Data." *Proc. ACL 2016* (venue per standard citation; arXiv:1511.06709v4 PDF used). Read in full.

## Content
Use target-side monolingual data without changing the architecture: (a) **dummy** empty source, or (b) **synthetic source via back-translation** with a reverse model, mixed with real parallel data. WMT'15 En↔De +2.8–3.7 BLEU; IWSLT'14 Tr→En +2.1–3.4; in-domain fine-tuning on back-translated TED data +1.2 BLEU. Back-translating the target side of the existing parallel data also helps (regularisation effect even without new text); quality of the back-translation system matters but even weaker reverse models help.

## Relevance to us
Formal precedent for the **"back-transliteration" augmentation** used by Dakshina/Kirov: romanize native Tamil Wikipedia words with a native→Latin model and train Latin→Tamil on the synthetic pairs. Kirov 2024 (fn. 14) explicitly draws this analogy. Combined with Benton 2025 (sampling ≫ 1-best for variation) this suggests our augmentation experiment: back-transliteration with *sampled* (variable) romanizations, optionally pushed toward Tanglish-style noise.
