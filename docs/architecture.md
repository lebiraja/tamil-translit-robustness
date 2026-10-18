# Architecture (planned; no code exists yet)

This describes the intended code layout and data flow so any session can start implementing without re-deriving it. Update it when the code appears (per the project rule: keep `docs/` in sync).

## Goals
Reproducible experiments: every number in the paper regenerable from configs, seeds and data checksums. Small, testable modules. No web service, no API; this is a research codebase run as CLI scripts.

## Planned layout
```
src/translit/
  data/        loaders for Dakshina lexicon, Aksharantar test, human-typed set; NFC normalization; vocab builder; cleaning rules with logged counts
  noise/       operators (vdrop, vlen, gem, digraph, key, repeat, mix), severity, seeded paired generation
  models/      bilstm_attn.py, transformer.py, param-count helper for size budgets
  train/       training loop, early stopping on dev, mixed-precision option, checkpointing, seed control
  decode/      beam search (top-k, MRR), greedy; later: rerank, shallow fusion
  eval/        CER, top-k accuracy with multiple references, per-noise degradation, bootstrap, Kruskal-Wallis/Dunn, Spearman
  augment/     A1 random noise, A2 phonological noise, A3 sampled back-transliteration
configs/       one YAML per experiment (model, size, data, augmentation, seed list)
scripts/      fetch_dakshina.py (byte ranges), make_noisy_sets.py, run_experiment.py, aggregate.py, make_figures.py
results/      <block>/<run-id>.json (metrics + provenance), figures/, tables/ (small, committed)
tests/        pytest: noise operators, metrics (known edit distances), loaders, tokenizer round-trip, beam search on a toy model
paper/        IEEEtran LaTeX, figures generated from results/
data/         gitignored: dakshina-ta/, aksharantar-tamil/, human-typed/, LM and lexicon samples
```

## Data flow
```
Dakshina train/dev/test (TSV)  -->  loaders (NFC, lowercase roman)  -->  vocab (train only)
                                                         |
                          clean batches  <---------------+-----------> noise ops (seeded)  --> paired noisy test sets
                                |                                             |
                                v                                             v
                    train (A0..A4, control) --> checkpoints (laptop/Leica)    evaluation (clean, noisy, held-out ops, Aksharantar, human set)
                                |                                             |
                                +------------------> results/*.json <---------+
                                                               |
                                              aggregate.py --> tables/figures --> paper/
```

## Key design decisions
- Character-level vocabularies built from training data only; Latin side lowercase a to z; Tamil side NFC code points. Unknown characters mapped explicitly and counted.
- Noise operators are pure functions of (word, severity, rng), so noisy test sets are paired and reproducible; operators for training augmentation use separate seeds from the test set.
- Evaluation handles multiple attested references per romanized input exactly as defined in Roark 2020/Kirov 2024 (decision recorded in code docstrings and tested). The baseline reproduction gate (`docs/experiment-plan.md` section 6) validates this.
- Parameter budgets are set by a helper that tunes hidden size to hit about 1M, 3M and 8M parameters for both architectures.
- Every run writes a self-describing JSON: config, seed, git commit, data checksums, library versions, GPU, wall time, metrics.
- Python rules from the user's global conventions: type hints, Pydantic models for configs, async only where useful (probably nowhere); dependencies pinned in `requirements.txt`; venv or Docker only.

## Testing strategy
pytest for noise operators (determinism, pairing, never empty), metrics (hand-computed edit distances and multi-reference cases), data loaders (counts equal 25,000 / 2,500 / 2,500 words and 68,218 / 6,827 / 6,864 pairs), beam search toy cases. A small end-to-end smoke test (tiny model, 100 pairs, 2 epochs) runs on CPU in CI-like fashion before any GPU job.

## Out of scope (now)
Web demo, REST API, sentence-level transliteration, mobile deployment (C5 is optional future work).
