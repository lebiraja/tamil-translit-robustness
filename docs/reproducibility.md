# Reproducibility guide

Everything in the paper regenerates from this repository. Seeds, configs, code commits and data checksums are stored inside each result JSON.

## 0. Environment
- Python 3.12, PyTorch 2.11 with CUDA 12.8 (Blackwell RTX 5070 on the lab server Leica; the RTX 4050 laptop also works). `scripts/setup_env.sh` builds `.venv`; `requirements.txt` lists the rest (torch is installed from the cu128 index; for CPU-only use the cpu index).
- Hardware used for all reported runs: one RTX 5070 12 GB, i7-14700, 15 GB RAM, Ubuntu 24.04, kernel 6.17.0-22-generic. Up to three jobs shared the GPU.

## 1. Data (all local, `data/` is gitignored)
1. Dakshina Tamil files by HTTP byte range from the official tar (offsets in `research/DATASET.md` section 2) into `data/dakshina-ta/`; check `data/dakshina-ta/SHA256SUMS` (train `fd98cc4e...`, dev `c5bb92e0...`, test `062fdc82...`; counts 68,218 / 6,827 / 6,864 pairs, tested by `tests/test_data.py`).
2. Aksharantar Tamil (HF `ai4bharat/Aksharantar`, Tamil split) into `data/aksharantar-tamil/`; the independent test file `tam_test.no_dakshina.tsv` (4,335 rows) is built by the filter in `docs/datasets/README.md`.
3. IndicXlit word list `data/indicxlit-wordprob-tamil/ta_word_prob.tsv.gz`.
4. `python scripts/prepare_data.py all` builds the 28 noisy test suites (seed 20261018), the independent suites and the 60,000-word pool (deterministic).
5. `python scripts/train.py configs/reverse_lstm.yaml` then `python scripts/synthesize_a3.py --k 3` builds the A3 and CTRL pairs (123,488 and 60,000 pairs).

## 2. Experiments
| Step | Command | Output |
|---|---|---|
| tests | `python -m pytest tests -q` (30 pass; `tests/test_resume.py` runs about 1 min) | |
| reproduction gate | `python scripts/run_matrix.py gate` | `results/gate/` |
| tuning (6 combos x 20 trials) | `python scripts/tune.py <lstm\|transformer> <1m\|3m\|8m>` | `results/tune/`, `configs/best_*.yaml` |
| C3 | `python scripts/run_matrix.py c3` (30 runs) | `results/c3/` |
| C2 | `python scripts/run_matrix.py c2` (80 runs) | `results/c2/` |
| per-item scoring | `python scripts/evaluate_ckpt.py` | `results/items/*.npz` (not committed) |
| statistics | `python scripts/aggregate.py` | `results/summary/` |
| report | `python scripts/make_results_md.py` | `docs/results.md` |
| final model | `python scripts/finetune.py name=v2-ft epochs=5` | `results/final/`, checkpoint in `runs/` |
`scripts/supervisor.py` plus user cron ran the queues unattended on Leica; per-run locks (`logs/locks/`) prevent duplicate training (see FIXES F3).

## 3. Paper
`python scripts/make_figures.py` and `python scripts/make_tables.py` write `paper/figures/*.pdf` and `paper/tables/*.tex` from `results/`; then in `paper/`: `xelatex main && biber main && xelatex main && xelatex main` (XeLaTeX because the paper prints Tamil script with Noto Sans Tamil). Clean build and page count are checked before every commit.

## 4. What is not reproducible from the repository alone
- The private real-chat word set and any team-typed set (privacy; documented in `docs/datasets/final-dataset.md`).
- Checkpoints (1.8 GB) are not in git: they are in a private Hugging Face model repo with a MANIFEST of sha256 and logged scores (`scripts/push_to_hf.py`).
- GPU runs are not bit-for-bit deterministic across machines; seeds fix data order and initialisation, and the five-seed mean and sd are what we report. One affected Transformer rerun differed by 0.17 test CER (FIXES F3).
