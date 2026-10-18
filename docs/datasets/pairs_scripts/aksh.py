"""Convert Aksharantar Tamil JSONL to TSV and measure stats + overlap with Dakshina."""
import collections as C, csv, gzip, json, sys, unicodedata as U, random

ext, dak, out = sys.argv[1:4]
def nfc(s): return U.normalize("NFC", s.strip())
def load_dak(split):
    rows = [l.rstrip("\n").split("\t") for l in open(f"{dak}/{split}.tsv", encoding="utf-8")]
    return {nfc(r[0]) for r in rows}, {(nfc(r[0]), r[1].strip().lower()) for r in rows}, {r[1].strip().lower() for r in rows}
dk = {s: load_dak(s) for s in ("train", "dev", "test")}
def tamil_only(w): return all(0x0B80 <= ord(c) <= 0x0BFF for c in w)

for split in ("test", "valid", "train"):
    rows = []
    bad = 0
    for line in open(f"{ext}/tam_{split}.json", encoding="utf-8"):
        d = json.loads(line)
        rows.append((nfc(d["native word"]), d["english word"].strip(), d.get("source"), d.get("score")))
    op = gzip.open(f"{out}/tam_{split}.tsv.gz", "wt", encoding="utf-8", newline="") if split == "train" else open(f"{out}/tam_{split}.tsv", "w", encoding="utf-8", newline="")
    w = csv.writer(op, delimiter="\t", lineterminator="\n", quoting=csv.QUOTE_NONE, escapechar="\\")
    w.writerow(["native", "roman", "source", "score"])
    for r in rows: w.writerow(r)
    op.close()
    nat = {r[0] for r in rows}; pairs = {(r[0], r[1].lower()) for r in rows}; roms = {r[1].lower() for r in rows}
    src = C.Counter(r[2] for r in rows)
    per = C.Counter(r[0] for r in rows)
    print(f"== {split}: rows {len(rows)} unique native {len(nat)} unique pairs {len(pairs)} unique roman {len(roms)}")
    print("   romanizations/native mean %.3f max %d" % (len(rows)/len(nat), max(per.values())))
    print("   sources", src.most_common())
    print("   non-Tamil-block native", sum(not tamil_only(n) for n in nat), "roman non a-z", sum(not r.isascii() or not r.isalpha() for r in roms), "roman has uppercase", sum(any(c.isupper() for c in r) for r in roms))
    if split != "train":
        print("   empty fields", sum(not r[0] or not r[1] for r in rows))
    for s in ("train", "dev", "test"):
        dn, dp, dr = dk[s]
        print(f"   overlap vs dakshina-{s}: native {len(nat & dn)} ({100*len(nat & dn)/len(nat):.2f}%), pairs {len(pairs & dp)}, roman strings {len(roms & dr)}")
    if split == "test":
        for sname in src:
            sn = {r[0] for r in rows if r[2] == sname}
            print(f"   [{sname}] native {len(sn)} rows {src[sname]} | ∩dak-train {len(sn & dk['train'][0])} ∩dak-dev {len(sn & dk['dev'][0])} ∩dak-test {len(sn & dk['test'][0])}")
    if split == "train":
        dsrc = {r[0] for r in rows if r[2] == "Dakshina"}
        print("   Dakshina-source natives", len(dsrc), "of which in dak-train", len(dsrc & dk['train'][0]), "dak-dev", len(dsrc & dk['dev'][0]), "dak-test", len(dsrc & dk['test'][0]))
        sc = [r[3] for r in rows if r[3] is not None]
        print("   scored rows", len(sc), "score min/median/max", min(sc), sorted(sc)[len(sc)//2], max(sc))
    random.seed(0)
    print("   examples:")
    for r in rows[:2] + random.sample(rows, 3): print("     ", r)
