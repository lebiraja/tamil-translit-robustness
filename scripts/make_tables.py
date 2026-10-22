"""LaTeX tables for the paper from results/summary and the noise manifest. Writes paper/tables/*.tex (booktabs).

  .venv/bin/python scripts/make_tables.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "tables"
S = ROOT / "results" / "summary"
OUT.mkdir(parents=True, exist_ok=True)
ARCH = {"lstm": "BiLSTM", "transformer": "Transformer"}


def pm(m: float, s: float, d: int = 2) -> str:
    return f"{m:.{d}f}\\,{{\\scriptsize$\\pm${s:.{d}f}}}"


def write(name: str, body: str) -> None:
    (OUT / f"{name}.tex").write_text(body)
    print("wrote", name)


def tab_c3() -> None:
    c = pd.read_csv(S / "c3_clean.csv")
    lines = ["\\begin{tabular}{llrcccc}", "\\toprule", "Model & Size & Params & Dev CER & Test CER & Top-1 (\\%) & Top-5 (\\%) \\\\", "\\midrule"]
    for arch in ("lstm", "transformer"):
        for _, r in c[c.arch == arch].iterrows():
            best = r.test_cer_mean == c.test_cer_mean.min()
            t = pm(r.test_cer_mean, r.test_cer_sd)
            lines.append(f"{ARCH[arch]} & {r['size'].upper()} & {r.n_params_mean / 1e6:.2f}M & {pm(r.dev_cer_mean, r.dev_cer_sd)} & {'\\textbf{' + t + '}' if best else t} & "
                         f"{pm(r.test_top1_mean, r.test_top1_sd, 1)} & {pm(r.test_top5_mean, r.test_top5_sd, 1)} \\\\")
        if arch == "lstm":
            lines.append("\\midrule")
    lines += ["\\bottomrule", "\\end{tabular}"]
    write("tab_c3", "\n".join(lines))


def tab_c2() -> None:
    c = pd.read_csv(S / "c2.csv")
    cols = [("clean_cer", "clean"), ("MIX.0.3_cer", "MIX"), ("V-DROP.0.3_cer", "V-DR."), ("KEY.0.3_cer", "KEY"), ("AK-all_cer", "AK")]
    conds = ["A0", "A1", "A2", "A3", "A4", "CTRL"]
    lines = ["\\begin{tabular}{l" + "c" * len(cols) + "c" * len(cols) + "}", "\\toprule",
             "& \\multicolumn{5}{c}{BiLSTM 3M} & \\multicolumn{5}{c}{Transformer 3M} \\\\", "\\cmidrule(lr){2-6}\\cmidrule(lr){7-11}",
             "Condition & " + " & ".join(n for _, n in cols) + " & " + " & ".join(n for _, n in cols) + " \\\\", "\\midrule"]
    for cond in conds:
        cells = []
        for arch in ("lstm", "transformer"):
            r = c[(c.arch == arch) & (c.condition == cond)].iloc[0]
            for k, _ in cols:
                col = c[(c.arch == arch) & (c.condition.isin(conds))][f"{k}_mean"]
                v = f"{r[f'{k}_mean']:.2f}"
                cells.append(f"\\textbf{{{v}}}" if r[f"{k}_mean"] == col.min() else v)
        lines.append(f"{cond} & " + " & ".join(cells) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    write("tab_c2", "\n".join(lines))
    sd = max(c[c.condition.isin(conds)][[f"{k}_sd" for k, _ in cols]].max())
    (OUT / "c2_max_sd.txt").write_text(f"{sd:.2f}")


def tab_ops() -> None:
    m = json.loads((ROOT / "data/synth/noisy_test/manifest.json").read_text())["suites"]
    desc = {"V-DROP": "delete non-initial vowels", "V-LEN": "collapse doubled vowels", "GEM": "collapse doubled consonants",
            "DIGRAPH": "th/t, dh/d, sh/s, ch/c/s swaps; zh$\\to$l,z", "KEY": "adjacent QWERTY key substitution", "REPEAT": "stretch one vowel by 1--3 letters",
            "MIX": "random combination of the six"}
    lines = ["\\begin{tabular}{llccc}", "\\toprule", "Operator & Effect & \\multicolumn{3}{c}{Words changed (\\%) at $p=$} \\\\", "\\cmidrule(lr){3-5}",
             " & & 0.1 & 0.3 & 0.5 \\\\", "\\midrule"]
    for op in ("V-DROP", "V-LEN", "GEM", "DIGRAPH", "KEY", "REPEAT", "MIX"):
        lines.append(f"{op} & {desc[op]} & " + " & ".join(f"{m[f'{op}.{p}']['changed_pct']:.0f}" for p in ("0.1", "0.3", "0.5")) + " \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    write("tab_ops", "\n".join(lines))
    rates = {op: m[f"{op}.0.3"]["char_edit_rate_pct"] for op in ("V-DROP", "KEY", "MIX", "DIGRAPH", "REPEAT", "V-LEN", "GEM")}
    (OUT / "edit_rates.json").write_text(json.dumps(rates))


def tab_stats() -> None:
    st = json.loads((S / "stats.json").read_text())["bootstrap"]
    pick = [("c3-lstm-3m", "c3-transformer-3m", "clean"), ("c3-lstm-3m", "c3-transformer-3m", "MIX.0.3"), ("c3-lstm-8m", "c3-transformer-8m", "MIX.0.3"),
            ("c2-lstm-A2", "c2-lstm-A1", "MIX.0.3"), ("c2-transformer-A2", "c2-transformer-A1", "MIX.0.3"), ("c2-lstm-A3", "c2-lstm-CTRL", "clean"),
            ("c2-lstm-A3", "c2-lstm-CTRL", "MIX.0.3"), ("c2-transformer-A3", "c2-transformer-CTRL", "MIX.0.3"), ("c2-lstm-A4", "c2-lstm-A2", "clean"),
            ("c2-transformer-A4", "c2-transformer-A2", "clean")]
    nice = lambda n: n.replace("c3-", "").replace("c2-", "").replace("lstm-", "BiLSTM ").replace("transformer-", "Trans. ").replace("3m", "3M").replace("8m", "8M").replace("1m", "1M")  # noqa: E731
    lines = ["\\begin{tabular}{llcc}", "\\toprule", "System $a$ vs.\\ $b$ & Suite & $\\Delta$CER ($a-b$) & 95\\% CI \\\\", "\\midrule"]
    for a, b, su in pick:
        r = next(x for x in st if x["a"] == a and x["b"] == b and x["suite"] == su)
        lo, hi = r["ci95"]
        lines.append(f"{nice(a)} vs.\\ {nice(b)} & {su.replace('.0.', ' $p{=}0.')}{'$' if 'MIX' in su else ''} & {r['diff_cer']:+.2f} & [{lo:+.2f}, {hi:+.2f}] \\\\")
    lines += ["\\bottomrule", "\\end{tabular}"]
    write("tab_stats", "\n".join(lines).replace("suite", "suite"))


if __name__ == "__main__":
    tab_c3()
    tab_c2()
    tab_ops()
    tab_stats()
