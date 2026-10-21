"""Statistics helpers for the analysis stage: corpus CER, paired bootstrap, Kruskal-Wallis, Dunn post-hoc, Holm.

Plain numpy/scipy. Per-item arrays come from scripts/evaluate_ckpt.py (edits to the closest reference, reference length).
"""

from __future__ import annotations

from collections.abc import Sequence
from itertools import combinations

import numpy as np
from scipy import stats as st


def corpus_cer(edits: np.ndarray, lens: np.ndarray) -> float:
    """CER in percent: total edits / total reference length (same definition as metrics.score)."""
    return 100.0 * float(np.sum(edits)) / float(np.sum(lens))


def paired_bootstrap(edits_a: np.ndarray, edits_b: np.ndarray, lens: np.ndarray, n: int = 10_000, seed: int = 0) -> dict:
    """Paired bootstrap over test items of CER(a) - CER(b). Inputs are aligned per item; edits may be seed means.

    Returns the observed difference, a 95% percentile CI and a two-sided p-value (share of resamples whose sign
    disagrees with zero, doubled, capped at 1).
    """
    ea, eb, ln = (np.asarray(x, dtype=float) for x in (edits_a, edits_b, lens))
    if not (ea.shape == eb.shape == ln.shape):
        raise ValueError("arrays must be aligned per item")
    obs = corpus_cer(ea, ln) - corpus_cer(eb, ln)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(ln), size=(n, len(ln)))
    d = 100.0 * ((ea[idx].sum(1) - eb[idx].sum(1)) / ln[idx].sum(1))
    lo, hi = np.percentile(d, [2.5, 97.5])
    if np.allclose(d, 0):
        p = 1.0
    else:
        p = float(min(1.0, 2 * min(np.mean(d <= 0), np.mean(d >= 0))))
    return {"diff_cer": obs, "ci95": [float(lo), float(hi)], "p": p, "n_items": int(len(ln)), "n_boot": n}


def holm(p: Sequence[float]) -> list[float]:
    """Holm-Bonferroni adjusted p-values (step-down, monotone, capped at 1)."""
    p = np.asarray(p, dtype=float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    run = 0.0
    for rank, i in enumerate(order):
        run = max(run, (m - rank) * p[i])
        adj[i] = min(1.0, run)
    return adj.tolist()


def kruskal(groups: dict[str, Sequence[float]]) -> dict:
    """Kruskal-Wallis H over named groups with eta-squared effect size (H - k + 1) / (N - k)."""
    vals = [np.asarray(v, dtype=float) for v in groups.values()]
    h, p = st.kruskal(*vals)
    k, n = len(vals), sum(len(v) for v in vals)
    return {"H": float(h), "p": float(p), "k": k, "N": n, "eta2": float((h - k + 1) / (n - k))}


def dunn(groups: dict[str, Sequence[float]]) -> list[dict]:
    """Dunn's pairwise test on pooled ranks with tie correction; Holm-adjusted two-sided p-values."""
    names = list(groups)
    vals = [np.asarray(groups[g], dtype=float) for g in names]
    allv = np.concatenate(vals)
    ranks = st.rankdata(allv)
    n = len(allv)
    _, counts = np.unique(allv, return_counts=True)
    tie = np.sum(counts**3 - counts) / (12 * (n - 1))
    mean_rank, start = {}, 0
    for g, v in zip(names, vals, strict=True):
        mean_rank[g] = ranks[start : start + len(v)].mean()
        start += len(v)
    out = []
    for a, b in combinations(names, 2):
        se = np.sqrt((n * (n + 1) / 12 - tie) * (1 / len(groups[a]) + 1 / len(groups[b])))
        z = (mean_rank[a] - mean_rank[b]) / se
        out.append({"a": a, "b": b, "z": float(z), "p": float(2 * st.norm.sf(abs(z)))})
    for r, pa in zip(out, holm([r["p"] for r in out]), strict=True):
        r["p_holm"] = pa
    return out


def cohens_d(a: Sequence[float], b: Sequence[float]) -> float:
    """Cohen's d with pooled SD (per-seed means; small n, report with caution)."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    sp = np.sqrt(((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1)) / (len(a) + len(b) - 2))
    return float((a.mean() - b.mean()) / sp) if sp > 0 else 0.0
