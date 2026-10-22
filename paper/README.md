# Paper (IEEE conference, IEEEtran)

`main.tex` includes `sections/*.tex`; figures are in `figures/` (vector PDF) and tables in `tables/` (booktabs). Both are generated from `results/` by `scripts/make_figures.py` and `scripts/make_tables.py`; do not edit them by hand.

Build (XeLaTeX is needed because the text prints Tamil script with Noto Sans Tamil; biber for the bibliography):
```
cd paper && export PATH=/usr/local/bin:$PATH
xelatex main && biber main && xelatex main && xelatex main
```
Done means: exit code 0, `main.pdf` exists, no `Citation ... undefined` / `Reference ... undefined` in `main.log`, no overfull boxes. Current length: 9 pages (check `pdfinfo main.pdf`); venue limit to confirm with the staff.

`refs.bib` is a copy of `research/refs.bib`; only papers that were downloaded and read are in it. Claim-to-evidence map: `docs/paper-claims-map.md`.

Open items before submission: evaluate the real-chat and team-typed sets (RQ2) and add them to Results; page-limit check; proofread.
