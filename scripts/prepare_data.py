"""Build every derived dataset the experiments need (deterministic, seeded, no torch needed).

  python scripts/prepare_data.py all        # everything below
  python scripts/prepare_data.py noisy      # C1 paired noisy test sets  -> data/synth/noisy_test/
  python scripts/prepare_data.py independent# Aksharantar non-Dakshina   -> data/synth/independent/
  python scripts/prepare_data.py pool       # A3 native word pool        -> data/synth/native_pool.tsv
"""

from __future__ import annotations

import gzip
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from translit import data as D  # noqa: E402
from translit import noise  # noqa: E402
from translit.metrics import edit_distance  # noqa: E402

OUT = D.ROOT / "data" / "synth"
NOISE_SEED = 20261018
OPS = list(noise.OPS) + ["MIX"]
TAMIL = set(chr(c) for c in range(0x0B80, 0x0BFF))


def write_suite(path: Path, rows: list[tuple[str, str, list[str]]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        f.write("clean_roman\tnoisy_roman\trefs\n")
        for c, n, r in rows:
            f.write(f"{c}\t{n}\t{'|'.join(r)}\n")


def noisy() -> None:
    table = D.reference_table(D.load_lexicon("test"))
    manifest = {"seed": NOISE_SEED, "n_inputs": len(table), "suites": {}}
    for op in OPS:
        for p in noise.SEVERITIES:
            rows = [(r, noise.noisy_variant(r, op, p, NOISE_SEED), refs) for r, refs in sorted(table.items())]
            write_suite(OUT / "noisy_test" / f"test.{op}.{p}.tsv", rows)
            changed = sum(c != n for c, n, _ in rows)
            ed = sum(edit_distance(c, n) for c, n, _ in rows)
            ln = sum(len(c) for c, _, _ in rows)
            manifest["suites"][f"{op}.{p}"] = {"changed_pct": 100 * changed / len(rows), "char_edit_rate_pct": 100 * ed / ln}
    (OUT / "noisy_test" / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print("noisy sets:", len(manifest["suites"]), "inputs each:", len(table))
    for k, v in manifest["suites"].items():
        print(f"  {k:12s} changed {v['changed_pct']:5.1f}%  realised char-edit {v['char_edit_rate_pct']:5.2f}%")


def independent() -> None:
    src = D.ROOT / "data" / "aksharantar-tamil" / "tam_test.no_dakshina.tsv"
    by: dict[str, dict[str, set[str]]] = {}
    for line in src.read_text(encoding="utf-8").splitlines()[1:]:
        native, roman, source = line.split("\t")[:3]
        by.setdefault(source, {}).setdefault(D.norm_roman(roman), set()).add(D.nfc(native))
    pooled: dict[str, set[str]] = {}
    for source, t in by.items():
        write_suite(OUT / "independent" / f"AK-{source.removeprefix('AK-')}.tsv", [(r, r, sorted(v)) for r, v in sorted(t.items())])
        print("independent", source, len(t))
        for r, v in t.items():
            pooled.setdefault(r, set()).update(v)
    write_suite(OUT / "independent" / "AK-all.tsv", [(r, r, sorted(v)) for r, v in sorted(pooled.items())])


def pool(prefix_len: int = 5, top: int = 60000) -> None:
    """Native Tamil words for A3 synthesis, never overlapping Dakshina dev/test or the independent test."""
    rows = {s: D.load_lexicon(s) for s in D.SPLITS}
    known = {n for s in D.SPLITS for n, _, _ in rows[s]}
    held = {n for s in ("dev", "test") for n, _, _ in rows[s]}
    ak = {D.nfc(l.split("\t")[0]) for l in (D.ROOT / "data/aksharantar-tamil/tam_test.no_dakshina.tsv").read_text(encoding="utf-8").splitlines()[1:]}
    held_prefix = {w[:prefix_len] for w in held | ak if len(w) >= prefix_len}
    stats = Counter()
    keep: list[tuple[str, float]] = []
    with gzip.open(D.ROOT / "data/indicxlit-wordprob-tamil/ta_word_prob.tsv.gz", "rt", encoding="utf-8") as f:
        for line in f:
            w, p = line.rstrip("\n").split("\t")
            w = D.nfc(w)
            stats["seen"] += 1
            if not (2 <= len(w) <= 20) or any(c not in TAMIL for c in w):
                stats["not_pure_tamil_or_length"] += 1
            elif w in known or w in ak:
                stats["in_dakshina_or_ak_test"] += 1
            elif len(w) >= prefix_len and w[:prefix_len] in held_prefix:
                stats["stem_prefix_overlap"] += 1
            else:
                keep.append((w, float(p)))
                if len(keep) >= top:
                    break
            if stats["seen"] > 3_000_000:
                break
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "native_pool.tsv").open("w", encoding="utf-8") as f:
        for w, p in keep:
            f.write(f"{w}\t{p}\n")
    (OUT / "native_pool.stats.json").write_text(json.dumps({"prefix_len": prefix_len, "kept": len(keep), **stats}, indent=1))
    print("pool kept", len(keep), dict(stats))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("noisy", "all"):
        noisy()
    if cmd in ("independent", "all"):
        independent()
    if cmd in ("pool", "all"):
        pool()
