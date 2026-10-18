import csv, gzip, sys, collections as C
sp, ak, dak = sys.argv[1:4]
sg = {}
for l in list(gzip.open(sp, "rt", encoding="utf-8"))[1:]:
    n, r, c = l.rstrip("\n").split("\t"); sg[n] = r
akm = C.defaultdict(set)
for p, gz in ((f"{ak}/tam_train.tsv.gz", 1), (f"{ak}/tam_valid.tsv", 0), (f"{ak}/tam_test.tsv", 0)):
    f = gzip.open(p, "rt", encoding="utf-8") if gz else open(p, encoding="utf-8")
    r = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"); next(r)
    for row in r: akm[(p.split("/")[-1].split(".")[0], row[0])].add(row[1].lower())
for split in ("tam_train", "tam_valid", "tam_test"):
    keys = [n for n in sg if (split, n) in akm]
    same = sum(sg[n] in akm[(split, n)] for n in keys)
    print(f"sangraha words also in Aksharantar {split}: {len(keys)}; romanization identical to an Aksharantar {split} romanization: {same} ({100*same/max(1,len(keys)):.1f}%)")
dt = C.defaultdict(set)
for l in open(f"{dak}/test.tsv", encoding="utf-8"):
    n, r, _ = l.split("\t"); dt[n].add(r)
inter = [n for n in sg if n in dt]
print("dakshina-test natives in sangraha sample", len(inter), "identical to a dakshina-test romanization", sum(sg[n] in dt[n] for n in inter))
