# Paper releases

| File | What it is |
|---|---|
| `paper-v2.pdf` | Previous final. Everything in v1 plus Section VII "Deployment Model" (the fully fine-tuned model, its table and figure, the preliminary real-chat check), the privacy statement, consistency fixes, a cleaned reference list. Source: git tag `paper-v2`. |
| `paper-v3.pdf` | **Latest layout.** Same content as v2; the abstract and keywords sit alone in the left column of page 1 and the Introduction starts at the top of the right column (`\newpage` before `\input{sections/introduction}` in `main.tex`). Git tag `paper-v3`. |
| `paper-v1.pdf` | First complete draft: related work, data and benchmark, method, setup, results (RQ1, RQ3, RQ4), discussion, limitations, conclusion; without the deployment-model section and v2 result. Source: git tag `paper-v1` (commit `fef4072`, with the corrected affiliation and the empty placeholder section removed). |

Authors in both: Lebi Raja, KRM Lohith, Allen John Isac and KP Shohil, Division of Data Science and Cybersecurity, Karunya Institute of Technology and Sciences, India (IEEE-style block: each name with the division and college under it, two authors per row; `\IEEEauthorblockN` for the name, `\IEEEauthorblockA` for the affiliation, `\and` between authors, `\linebreakand` for the second row). Tags `paper-v1.1` and `paper-v2.1` are the versions with the co-authors (the first tags `paper-v1`, `paper-v2` list only the first author).
