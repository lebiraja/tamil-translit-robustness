"""Wikidata person labels (ta, en) -> token-aligned word pairs; overlap with Dakshina."""
import collections as C, gzip, re, sys, unicodedata as U
src, out, dak = sys.argv[1:4]
TA = re.compile(r"^[஀-௿]+$"); LA = re.compile(r"^[a-z]+$")
rows = [l.rstrip("\n").split("\t") for l in open(src, encoding="utf-8")][1:]
lab = lambda s: s.rsplit("@", 1)[0].strip('"')
items = {(r[0].rsplit("/", 1)[-1], lab(r[1]), lab(r[2])) for r in rows if len(r) >= 3}
pairs = C.Counter(); aligned = 0
for q, ta, en in items:
    a, b = U.normalize("NFC", ta).replace("-", " ").split(), en.replace("-", " ").replace(".", " ").lower().split()
    if len(a) != len(b): continue
    aligned += 1
    for x, y in zip(a, b):
        if TA.match(x) and LA.match(y) and len(y) > 1: pairs[(x, y)] += 1
print("labels", len(items), "token-count aligned", aligned, "word pairs", len(pairs), "native types", len({x for x, _ in pairs}))
with open(out, "w", encoding="utf-8") as f:
    f.write("native\troman\tcount\n")
    for (x, y), c in pairs.most_common(): f.write(f"{x}\t{y}\t{c}\n")
for s in ("train", "dev", "test"):
    dn = {l.split("\t")[0] for l in open(f"{dak}/{s}.tsv", encoding="utf-8")}
    print(f"  native ∩ dakshina-{s}: {len({x for x, _ in pairs} & dn)}")
for p in list(pairs.most_common())[:5] + list(pairs.most_common())[5000:5004]: print("  ", p)
