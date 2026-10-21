"""Turn the private WhatsApp exports into an anonymous word list for noise calibration and annotation.

PRIVATE DATA: input is data/private/whatsapp/*.txt (gitignored, never committed, never sent to any
service or agent). Output keeps only lowercase word types with counts, no sender names, no messages,
no timestamps: data/private/wa_types.tsv (word, count, english_guess). Lebi must review the list
for personal names before any word-level artifact leaves this machine.
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINE = re.compile(r"^\[?\d{1,2}/\d{1,2}/\d{2,4},? [^-\]]*[-\]]? ?[^:]+: (.*)$")
FORCE_TAMIL = set("da di pa ma la na nu ku dei ji ra po va vaa naa nee ne un en oru illa illai enna inga anga avan ava "
                  "anna akka thala vera sema semma padam ponga vanga romba nalla mattum thaan dhan kitta mela pola mari "
                  "machan macha".split())


def main() -> None:
    c: Counter[str] = Counter()
    for f in sorted((ROOT / "data/private/whatsapp").glob("*.txt")):
        for line in f.read_text(encoding="utf-8", errors="ignore").splitlines():
            g = LINE.match(line.strip())
            if not g or "omitted" in g.group(1) or "http" in g.group(1):
                continue
            c.update(t for t in re.findall(r"[a-z]+", g.group(1).lower()) if len(t) >= 2)
    try:
        from wordfreq import zipf_frequency
        eng = lambda w: w not in FORCE_TAMIL and zipf_frequency(w, "en") >= 3.5  # noqa: E731
    except ImportError:
        print("wordfreq not installed: english_guess left as '?'", file=sys.stderr)
        eng = lambda w: None  # noqa: E731
    out = ROOT / "data/private/wa_types.tsv"
    with out.open("w", encoding="utf-8") as f:
        f.write("word\tcount\tenglish_guess\n")
        for w, n in c.most_common():
            e = eng(w)
            f.write(f"{w}\t{n}\t{'?' if e is None else int(e)}\n")
    print(f"{len(c)} types, {sum(c.values())} tokens -> {out}")


if __name__ == "__main__":
    main()
