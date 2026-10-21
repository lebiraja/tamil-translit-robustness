"""A3 data: romanize the filtered native pool with the Dakshina-trained native->roman model.

  python scripts/synthesize_a3.py --ckpt runs/reverse-lstm-s0/best.pt --k 3
Writes data/synth/a3_sampled.tsv (k temperature-1 samples per word, de-duplicated; roman<TAB>native)
and data/synth/a3_greedy.tsv (1 greedy romanization per word; the clean control with the same words).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from translit import data as D  # noqa: E402
from translit.decode import greedy, sample  # noqa: E402
from translit.metrics import edit_distance  # noqa: E402

MAX_REL_EDIT, MIN_REL_LEN = 0.35, 0.6  # quality filter vs the greedy romanization
from translit.models import build  # noqa: E402


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default="runs/reverse-lstm-s0/best.pt")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--temp", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    torch.manual_seed(a.seed)
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    ck = torch.load(D.ROOT / a.ckpt, map_location=dev)
    v = D.Vocab(**ck["vocab"])
    m = build(ck["arch"], len(v.src), len(v.tgt), **ck["kw"]).to(dev)
    m.load_state_dict(ck["model"])
    words = [l.split("\t")[0] for l in (D.ROOT / "data/synth/native_pool.tsv").read_text(encoding="utf-8").splitlines()]
    samp: set[tuple[str, str]] = set()
    gre: list[tuple[str, str]] = []
    dropped = 0
    for s in range(0, len(words), 512):
        chunk = words[s : s + 512]
        src, _ = D.collate([(v.enc_src(w), [1, 2]) for w in chunk])
        src = src.to(dev)
        g = {}
        for w, ids in zip(chunk, greedy(m, src), strict=True):
            r = v.dec_tgt(ids)
            if r:
                gre.append((r, w))
                g[w] = r
        for _ in range(a.k):
            for w, ids in zip(chunk, sample(m, src, a.temp), strict=True):
                r = v.dec_tgt(ids)
                if r and w in g and len(r) >= MIN_REL_LEN * len(g[w]) and edit_distance(r, g[w]) <= MAX_REL_EDIT * len(g[w]):
                    samp.add((r, w))
                else:
                    dropped += 1
    out = D.ROOT / "data/synth"
    (out / "a3_sampled.tsv").write_text("".join(f"{r}\t{n}\n" for r, n in sorted(samp)), encoding="utf-8")
    (out / "a3_greedy.tsv").write_text("".join(f"{r}\t{n}\n" for r, n in gre), encoding="utf-8")
    print(f"words {len(words)}  sampled pairs {len(samp)} (dropped by filter {dropped})  greedy pairs {len(gre)}")


if __name__ == "__main__":
    main()
