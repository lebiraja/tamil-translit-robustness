"""Render docs/results.md from docs/results_text.md by replacing {{name}} placeholders with tables built from results/summary/.

  python scripts/make_results_md.py
Every number in the tables comes from results/summary/*.csv|json (written by scripts/aggregate.py); the text file holds only prose.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SUM = ROOT / "results/summary"
MODELS = [("lstm", s) for s in ("1m", "3m", "8m")] + [("transformer", s) for s in ("1m", "3m", "8m")]
OPS = ["V-DROP", "V-LEN", "GEM", "DIGRAPH", "KEY", "REPEAT", "MIX"]
NAMES = {"lstm": "BiLSTM", "transformer": "Transformer"}
CONDS = ["A0", "A1", "A2", "A3", "A4", "CTRL", "A2-noGEM", "A2-noVDROP"]


def md(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join("" if (isinstance(v, float) and np.isnan(v)) else str(v) for v in r) + " |")
    return "\n".join(out)


def pm(m: float, s: float, d: int = 2) -> str:
    return f"{m:.{d}f} ± {s:.{d}f}" if s == s else f"{m:.{d}f}"


def mname(a: str, s: str) -> str:
    return f"{NAMES[a]} {s.upper()}"


def t_c3() -> str:
    d = pd.read_csv(SUM / "c3_clean.csv")
    rows = []
    for a, s in MODELS:
        r = d[(d.arch == a) & (d["size"] == s)].iloc[0]
        rows.append({"model": mname(a, s), "params": f"{r.n_params_mean / 1e6:.2f}M", "seeds": int(r.n_seeds),
                     "dev CER": pm(r.dev_cer_mean, r.dev_cer_sd), "test CER": pm(r.test_cer_mean, r.test_cer_sd),
                     "top-1 %": pm(r.test_top1_mean, r.test_top1_sd), "top-5 %": pm(r.test_top5_mean, r.test_top5_sd),
                     "MRR": pm(r.test_mrr_mean, r.test_mrr_sd, 3), "train min": f"{r.wall_s_mean / 60:.0f}"})
    return md(pd.DataFrame(rows))


def t_c1_sev(sev: float = 0.3) -> str:
    d = pd.read_csv(SUM / "c1_degradation.csv")
    c3 = pd.read_csv(SUM / "c3_clean.csv")
    rows = []
    clean = {"noise": "clean"}
    for a, s in MODELS:
        r = c3[(c3.arch == a) & (c3["size"] == s)].iloc[0]
        clean[mname(a, s)] = pm(r.test_cer_mean, r.test_cer_sd)
    rows.append(clean)
    for op in OPS:
        row = {"noise": f"{op} {sev}"}
        for a, s in MODELS:
            r = d[(d.arch == a) & (d["size"] == s) & (d.op == op) & (np.isclose(d.severity, sev))].iloc[0]
            row[mname(a, s)] = pm(r.cer_mean, r.cer_sd)
        rows.append(row)
    return md(pd.DataFrame(rows))


def t_c1_rel(sev: float = 0.3) -> str:
    d = pd.read_csv(SUM / "c1_degradation.csv")
    rows = []
    for op in OPS:
        row = {"noise": f"{op} {sev}"}
        for a, s in MODELS:
            r = d[(d.arch == a) & (d["size"] == s) & (d.op == op) & (np.isclose(d.severity, sev))].iloc[0]
            row[mname(a, s)] = f"+{r.abs_deg_cer_mean:.1f} ({r.rel_deg_cer_pct:.0f}%)"
        rows.append(row)
    return md(pd.DataFrame(rows))


def t_c1_curve(op: str = "MIX") -> str:
    d = pd.read_csv(SUM / "c1_degradation.csv")
    rows = []
    for a, s in MODELS:
        row = {"model": mname(a, s)}
        for sev in (0.1, 0.2, 0.3, 0.5):
            r = d[(d.arch == a) & (d["size"] == s) & (d.op == op) & (np.isclose(d.severity, sev))].iloc[0]
            row[f"{op} {sev}"] = pm(r.cer_mean, r.cer_sd)
        rows.append(row)
    return md(pd.DataFrame(rows))


def t_c2(arch: str) -> str:
    d = pd.read_csv(SUM / "c2.csv")
    rows = []
    for c in CONDS:
        r = d[(d.arch == arch) & (d.condition == c)].iloc[0]
        row = {"condition": c, "clean": pm(r.clean_cer_mean, r.clean_cer_sd)}
        for key, lab in (("MIX.0.1", "MIX .1"), ("MIX.0.3", "MIX .3"), ("MIX.0.5", "MIX .5"), ("V-DROP.0.3", "V-DROP .3"),
                         ("GEM.0.3", "GEM .3"), ("KEY.0.3", "KEY .3"), ("AK-all", "AK-all"), ("AK-NEI", "AK-NEI")):
            row[lab] = pm(r[f"{key}_cer_mean"], r[f"{key}_cer_sd"])
        rows.append(row)
    return md(pd.DataFrame(rows))


def t_boot() -> str:
    st = json.loads((SUM / "stats.json").read_text())
    rows = [{"a": b["a"], "b": b["b"], "suite": b["suite"], "ΔCER (a−b)": f"{b['diff_cer']:+.2f}",
             "95% CI": f"[{b['ci95'][0]:+.2f}, {b['ci95'][1]:+.2f}]", "p": f"{b['p']:.4f}"} for b in st["bootstrap"]]
    return md(pd.DataFrame(rows))


def t_kw() -> str:
    st = json.loads((SUM / "stats.json").read_text())
    rows = [{"family": k.replace("|", " / "), "H": f"{v['H']:.2f}", "p": f"{v['p']:.2g}", "η²": f"{v['eta2']:.2f}", "k groups": v["k"], "N": v["N"]}
            for k, v in st["kruskal"].items()]
    return md(pd.DataFrame(rows))


def t_dunn() -> str:
    st = json.loads((SUM / "stats.json").read_text())
    rows = []
    for k, lst in st["dunn"].items():
        for r in lst:
            if r["p_holm"] < 0.05:
                rows.append({"family": k.replace("|", " / "), "pair": f"{r['a']} vs {r['b']}", "z": f"{r['z']:+.2f}", "p (Holm)": f"{r['p_holm']:.3g}"})
    return md(pd.DataFrame(rows)) if rows else "_no pair significant after Holm correction_"


def t_manifest() -> str:
    m = json.loads((SUM / "noise_manifest.json").read_text())["suites"]
    rows = []
    for op in OPS:
        row = {"operator": op}
        for sev in ("0.1", "0.2", "0.3", "0.5"):
            v = m[f"{op}.{sev}"]
            row[f"p={sev}"] = f"{v['changed_pct']:.0f}% words, {v['char_edit_rate_pct']:.1f}% chars"
        rows.append(row)
    return md(pd.DataFrame(rows))


def t_runs() -> str:
    s = json.loads((SUM / "summary.json").read_text())
    return f"{s['n_runs']['c3']} C3 runs and {s['n_runs']['c2']} C2 runs; diverged runs: {len(s['diverged_runs'])}"


TABLES = {"c3": t_c3, "c1_sev03": t_c1_sev, "c1_rel03": t_c1_rel, "c1_mix": lambda: t_c1_curve("MIX"), "c1_vdrop": lambda: t_c1_curve("V-DROP"),
          "c1_key": lambda: t_c1_curve("KEY"), "c2_lstm": lambda: t_c2("lstm"), "c2_transformer": lambda: t_c2("transformer"),
          "boot": t_boot, "kw": t_kw, "dunn": t_dunn, "manifest": t_manifest, "runs": t_runs}


def main() -> None:
    text = (ROOT / "docs/results_text.md").read_text()
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: TABLES[m.group(1)](), text)
    (ROOT / "docs/results.md").write_text(out)
    print(f"wrote docs/results.md ({len(out.splitlines())} lines)")


if __name__ == "__main__":
    main()
