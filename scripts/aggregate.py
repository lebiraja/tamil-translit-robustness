"""Aggregate C3/C2 results into results/summary/ (CSV + JSON). numpy/scipy/pandas only.

  python scripts/aggregate.py [--boot 10000]
Inputs: results/c3/*.json, results/c2/*.json (run summaries), results/items/*.npz (per-item, scripts/evaluate_ckpt.py).
Outputs: c3_clean.csv, c1_degradation.csv, c2.csv, stats.json, summary.json, noise_manifest.json.
Bootstrap comparisons pool seeds by averaging per-item edits over the seeds of each system (items stay paired).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from translit.stats import cohens_d, dunn, kruskal, paired_bootstrap  # noqa: E402

ROOT = Path(os.environ.get("AGG_ROOT", Path(__file__).resolve().parents[1]))  # AGG_ROOT: smoke tests only
OUT = ROOT / "results/summary"
SIZES = ("1m", "3m", "8m")
C2_MAIN = ("A0", "A1", "A2", "A3", "A4", "CTRL")


def load_runs(block: str) -> pd.DataFrame:
    rows = []
    for f in sorted((ROOT / "results" / block).glob("*.json")):
        j = json.loads(f.read_text())
        c = j["config"]
        name = c["name"]  # c3-<arch>-<size> | c2-<arch>-<cond>
        _, arch, tag = name.split("-", 2)
        r = {"file": f.name, "commit": j.get("commit"), "name": name, "arch": arch, "tag": tag, "seed": c["seed"],
             "n_params": j["n_params"], "wall_s": j.get("wall_s"), "epochs_run": len(j.get("history", [])),
             "diverged": any(not np.isfinite(h["train_loss"]) for h in j.get("history", []))}
        for split in ("dev", "test"):
            for m in ("cer", "top1", "top5", "mrr"):
                r[f"{split}_{m}"] = j.get(split, {}).get(m, np.nan)
        for suite, d in {**j.get("noisy", {}), **j.get("independent", {})}.items():
            r[f"{suite}|cer"], r[f"{suite}|top1"] = d["cer"], d["top1"]
        rows.append(r)
    return pd.DataFrame(rows)


def msd(g: pd.DataFrame, cols: list[str]) -> pd.Series:
    out = {"n_seeds": len(g)}
    for c in cols:
        out[f"{c}_mean"], out[f"{c}_sd"] = g[c].mean(), g[c].std(ddof=1) if len(g) > 1 else np.nan
    return pd.Series(out)


def c3_clean(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["dev_cer", "test_cer", "test_top1", "test_top5", "test_mrr", "n_params", "wall_s"]
    return df.groupby(["arch", "tag"]).apply(msd, cols, include_groups=False).reset_index().rename(columns={"tag": "size"})


def c1_degradation(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    suites = sorted({c.split("|")[0] for c in df.columns if "|" in c and not c.startswith("AK-")})
    for (arch, size), g in df.groupby(["arch", "tag"]):
        for s in suites:
            op, sev = s.rsplit(".", 2)[0], float(s.split(".", 1)[1])
            cer, top1 = g[f"{s}|cer"], g[f"{s}|top1"]
            d_cer, d_top1 = cer - g["test_cer"], g["test_top1"] - top1
            rows.append({"arch": arch, "size": size, "op": op, "severity": sev, "n_seeds": len(g),
                         "cer_mean": cer.mean(), "cer_sd": cer.std(ddof=1), "top1_mean": top1.mean(), "top1_sd": top1.std(ddof=1),
                         "clean_cer_mean": g["test_cer"].mean(), "clean_top1_mean": g["test_top1"].mean(),
                         "abs_deg_cer_mean": d_cer.mean(), "abs_deg_cer_sd": d_cer.std(ddof=1),
                         "rel_deg_cer_pct": 100 * d_cer.mean() / g["test_cer"].mean(),
                         "abs_deg_top1_mean": d_top1.mean(), "rel_deg_top1_pct": 100 * d_top1.mean() / g["test_top1"].mean()})
    return pd.DataFrame(rows).sort_values(["arch", "size", "op", "severity"])


def c2_table(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    suites = [c.split("|")[0] for c in df.columns if c.endswith("|cer")]
    keep = [s for s in suites if s.endswith(".0.3") or s.startswith("MIX.") and s[-3:] in ("0.1", "0.3", "0.5") or s.startswith("AK-")]
    rows = []
    for (arch, cond), g in df.groupby(["arch", "tag"]):
        r = {"arch": arch, "condition": cond, "n_seeds": len(g), "clean_cer_mean": g["test_cer"].mean(),
             "clean_cer_sd": g["test_cer"].std(ddof=1), "clean_top1_mean": g["test_top1"].mean()}
        for s in sorted(set(keep)):
            r[f"{s}_cer_mean"], r[f"{s}_cer_sd"] = g[f"{s}|cer"].mean(), g[f"{s}|cer"].std(ddof=1)
            r[f"{s}_top1_mean"] = g[f"{s}|top1"].mean()
        rows.append(r)
    return pd.DataFrame(rows)


def items(run_prefix: str) -> list[dict]:
    return [dict(np.load(f)) for f in sorted((ROOT / "results/items").glob(f"{run_prefix}-s*.npz"))]


def boot(a: str, b: str, suite: str, n: int) -> dict | None:
    ia, ib = items(a), items(b)
    if not ia or not ib:
        return None
    ea = np.mean([x[f"{suite}__edits"] for x in ia], 0)
    eb = np.mean([x[f"{suite}__edits"] for x in ib], 0)
    r = paired_bootstrap(ea, eb, ia[0][f"{suite}__reflen"], n=n)
    return {"a": a, "b": b, "suite": suite, "seeds_a": len(ia), "seeds_b": len(ib), **r}


def per_seed_cer(df: pd.DataFrame, name: str, col: str) -> list[float]:
    return df.loc[df["name"] == name, col].dropna().tolist()


def stats(c3: pd.DataFrame, c2: pd.DataFrame, n: int) -> dict:
    out: dict = {"note": "Paired bootstrap over test items (seed-mean per-item edits). diff_cer = CER(a) - CER(b), negative favours a. "
                         "Seed-level tests use 5 (or fewer) per-seed CERs per system: statistical power is low.",
                 "bootstrap": [], "seed_level": [], "kruskal": {}, "dunn": {}}
    pairs = [(f"c3-lstm-{s}", f"c3-transformer-{s}", su) for s in SIZES for su in ("clean", "MIX.0.3")]
    for arch in ("lstm", "transformer"):
        p = f"c2-{arch}"
        pairs += [(f"{p}-A2", f"{p}-A1", su) for su in ("clean", "MIX.0.3")]
        pairs += [(f"{p}-A3", f"{p}-CTRL", su) for su in ("clean", "MIX.0.3")]
        pairs += [(f"{p}-A4", f"{p}-A2", su) for su in ("clean", "MIX.0.3")]
        pairs += [(f"{p}-A2-noGEM", f"{p}-A2", "GEM.0.3"), (f"{p}-A2-noVDROP", f"{p}-A2", "V-DROP.0.3")]
    for a, b, su in pairs:
        r = boot(a, b, su, n)
        if r:
            out["bootstrap"].append(r)
        df = c3 if a.startswith("c3") else c2
        col = "test_cer" if su == "clean" else f"{su}|cer"
        if not df.empty and col in df:
            xa, xb = per_seed_cer(df, a, col), per_seed_cer(df, b, col)
            if len(xa) > 1 and len(xb) > 1:
                out["seed_level"].append({"a": a, "b": b, "suite": su, "mean_a": float(np.mean(xa)), "mean_b": float(np.mean(xb)),
                                          "cohens_d": cohens_d(xa, xb), "n_a": len(xa), "n_b": len(xb)})
    if not c2.empty:
        for arch in ("lstm", "transformer"):
            for su, col in (("clean", "test_cer"), ("MIX.0.3", "MIX.0.3|cer")):
                g = {c: per_seed_cer(c2, f"c2-{arch}-{c}", col) for c in C2_MAIN}
                if all(len(v) >= 2 for v in g.values()):
                    out["kruskal"][f"{arch}|{su}"] = kruskal(g)
                    out["dunn"][f"{arch}|{su}"] = dunn(g)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=10_000)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    c3, c2 = load_runs("c3"), load_runs("c2")
    if not c3.empty:
        c3_clean(c3).to_csv(OUT / "c3_clean.csv", index=False, float_format="%.4f")
        c1_degradation(c3).to_csv(OUT / "c1_degradation.csv", index=False, float_format="%.4f")
    if not c2.empty:
        c2_table(c2).to_csv(OUT / "c2.csv", index=False, float_format="%.4f")
    st = stats(c3, c2, a.boot)
    (OUT / "stats.json").write_text(json.dumps(st, indent=1))
    man = ROOT / "data/synth/noisy_test/manifest.json"
    if man.exists():
        shutil.copy(man, OUT / "noise_manifest.json")
    allruns = pd.concat([c3, c2], ignore_index=True)
    digest = {
        "n_runs": {"c3": len(c3), "c2": len(c2)}, "n_item_dumps": len(list((ROOT / "results/items").glob("*.npz"))),
        "diverged_runs": allruns.loc[allruns["diverged"], "file"].tolist() if not allruns.empty else [],
        "c3_test_cer": {f"{r.arch}-{r.tag}": round(r.test_cer_mean, 3) for r in
                        c3.groupby(["arch", "tag"])["test_cer"].mean().reset_index(name="test_cer_mean").itertuples()} if not c3.empty else {},
        "c2_test_cer": {f"{r.arch}-{r.tag}": round(r.test_cer_mean, 3) for r in
                        c2.groupby(["arch", "tag"])["test_cer"].mean().reset_index(name="test_cer_mean").itertuples()} if not c2.empty else {},
        "inputs": [{"file": r.file, "commit": r.commit} for r in allruns.itertuples()] if not allruns.empty else [],
    }
    (OUT / "summary.json").write_text(json.dumps(digest, indent=1))
    print(f"wrote {OUT} (c3 {len(c3)} runs, c2 {len(c2)} runs, {len(st['bootstrap'])} bootstrap comparisons)")


if __name__ == "__main__":
    main()
