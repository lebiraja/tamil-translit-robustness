"""Build the private WhatsApp test suites from model labels (data/private/wa_labels.tsv).

Output (gitignored, suite format clean<TAB>noisy<TAB>refs):
  data/private/wa_test/WA-TA.tsv    labelled TA   (confident)
  data/private/wa_test/WA-TAq.tsv   labelled TA?  (ambiguous; report separately)
Labels are model-made; the paper must call this "model-labelled, human-verified" only after Lebi checks a sample
(data/private/wa_check_sample.tsv is written for that).
"""

from __future__ import annotations

import random
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    rows = [l.split("\t") for l in (ROOT / "data/private/wa_labels.tsv").read_text(encoding="utf-8").splitlines()[1:]]
    out = ROOT / "data/private/wa_test"
    out.mkdir(parents=True, exist_ok=True)
    kept: dict[str, list[tuple[str, str]]] = {"TA": [], "TA?": []}
    for r in rows:
        if len(r) >= 3 and r[1] in kept and r[2].strip():
            kept[r[1]].append((r[0], unicodedata.normalize("NFC", r[2].strip())))
    for lab, name in (("TA", "WA-TA"), ("TA?", "WA-TAq")):
        with (out / f"{name}.tsv").open("w", encoding="utf-8") as f:
            f.write("clean_roman\tnoisy_roman\trefs\n")
            for w, t in kept[lab]:
                f.write(f"{w}\t{w}\t{t}\n")
        print(name, len(kept[lab]))
    sample = random.Random(11).sample(kept["TA"], min(150, len(kept["TA"])))
    (ROOT / "data/private/wa_check_sample.tsv").write_text(
        "word\tmodel_tamil\tcorrect_y_or_fix\n" + "".join(f"{w}\t{t}\t\n" for w, t in sample), encoding="utf-8")
    print("check sample:", len(sample))


if __name__ == "__main__":
    sys.exit(main())
