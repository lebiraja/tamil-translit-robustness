"""Overlap of a (native, roman, count) TSV.gz with Dakshina splits; agreement with human romanizations."""
import collections as C, gzip, random, sys
p, dak = sys.argv[1:3]
rows = [l.rstrip("\n").split("\t") for l in gzip.open(p, "rt", encoding="utf-8")][1:]
nat = C.defaultdict(set)
for r in rows: nat[r[0]].add(r[1])
print("rows", len(rows), "native types", len(nat), "tokens", sum(int(r[2]) for r in rows))
for s in ("train", "dev", "test"):
    d = C.defaultdict(dict)
    for l in open(f"{dak}/{s}.tsv", encoding="utf-8"):
        n, r, c = l.rstrip("\n").split("\t"); d[n][r] = int(c)
    inter = set(nat) & set(d)
    any_m = sum(bool(nat[n] & set(d[n])) for n in inter)
    top_m = sum(max(d[n], key=d[n].get) in nat[n] for n in inter)
    print(f"dakshina-{s}: native overlap {len(inter)}/{len(d)} ({100*len(inter)/len(d):.1f}%); romanization equals some human variant {any_m} ({100*any_m/max(1,len(inter)):.1f}%), equals top human variant {top_m} ({100*top_m/max(1,len(inter)):.1f}%)")
random.seed(0)
for r in rows[:3] + random.sample(rows, 5): print("  ", r)
