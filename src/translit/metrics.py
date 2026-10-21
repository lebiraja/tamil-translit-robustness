"""Metrics: CER (corpus level, closest reference), top-k accuracy, MRR.

Definition (logged in every results file): for each input the references are all
native forms attested for that exact romanization in the same split. CER = total
edit distance to the closest reference / total length of that reference, over
code points of NFC text, taking the top-1 hypothesis. Top-k = any of the k best
hypotheses equals any reference. MRR uses the rank of the first correct hypothesis.
"""

from __future__ import annotations

from collections.abc import Sequence


def edit_distance(a: str, b: str) -> int:
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def closest(hyp: str, refs: Sequence[str]) -> tuple[int, int]:
    """Return (edits, reference length) for the closest reference."""
    best = min(refs, key=lambda r: edit_distance(hyp, r))
    return edit_distance(hyp, best), len(best)


def score(nbest: Sequence[Sequence[str]], refs: Sequence[Sequence[str]], ks: Sequence[int] = (1, 5)) -> dict[str, float]:
    """``nbest[i]`` are ranked hypotheses for input i; ``refs[i]`` its attested references."""
    n = len(nbest)
    edits = length = 0
    rr = 0.0
    hits = {k: 0 for k in ks}
    for hyps, rs in zip(nbest, refs, strict=True):
        e, ln = closest(hyps[0] if hyps else "", rs)
        edits += e
        length += ln
        rset = set(rs)
        for k in ks:
            hits[k] += any(h in rset for h in hyps[:k])
        for rank, h in enumerate(hyps, 1):
            if h in rset:
                rr += 1.0 / rank
                break
    out = {"cer": 100.0 * edits / length, "mrr": rr / n, "n": float(n)}
    out.update({f"top{k}": 100.0 * hits[k] / n for k in ks})
    return out
