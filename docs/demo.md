# Tanglish to Tamil typing demo (final model v1)

Run on any machine with the venv: `.venv/bin/python app/server.py [--port 8000] [--ckpt models/v1-a4-transformer-3m.pt]`, then open http://localhost:8000.
Type Tanglish; each Latin word is converted on its own (non-Latin characters and punctuation are kept). Click a word to pick one of the top-5 candidates; "Copy Tamil" copies the choice.

- **Model (v1):** the best seed of the A4 condition of the Transformer 3M (`c2-transformer-A4-s1`, dev CER 8.47, test CER 9.02, mixed-noise CER about 21.6). A4 = Tamil-phonological noise plus sampled back-transliteration pairs; chosen from the experiments in `docs/results.md`. It is not a single "best" model of the study: the study compares many small models, this is the one picked for use.
- **Checkpoint:** `models/v1-a4-transformer-3m.pt` (12.6 MB, gitignored). Copy from Leica `runs/c2-transformer-A4-s1/best.pt` or from the private Hugging Face repo (`models/c2/c2-transformer-A4-s1.pt`).
- **Code:** `src/translit/infer.py` (loader, beam search n-best, sentence splitter, cache), `app/server.py` (FastAPI, POST `/api/transliterate`), `app/static/index.html` (the page). CPU is enough (a word takes a few ms).
- **Known limits:** English words in a sentence are also transliterated ("office" becomes ஆபிக்); no context between words; some typed forms are ambiguous (check the alternatives); trained on formal-text romanizations plus synthetic noise, not yet validated on real chat (see the WhatsApp set in `docs/datasets/final-dataset.md`).
- **Planned v2:** fine-tune this model on much more real data (Aksharantar train, filtered) mixed with the old data and noise, then compare on the real-chat and independent sets.
