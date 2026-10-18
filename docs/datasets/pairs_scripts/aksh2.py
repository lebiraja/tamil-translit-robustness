"""Derive a Dakshina-disjoint Aksharantar test set; proxy stem-overlap of Aksharantar train with Dakshina test."""
import csv, gzip, sys, collections as C, random
out, dak = sys.argv[1:3]
def rd(p, gz=False):
    f = gzip.open(p, "rt", encoding="utf-8") if gz else open(p, encoding="utf-8")
    r = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE, escapechar="\\"); next(r); return list(r)
dk = {s: {l.split("\t")[0] for l in open(f"{dak}/{s}.tsv", encoding="utf-8")} for s in ("train", "dev", "test")}
dkr = {s: {l.split("\t")[1] for l in open(f"{dak}/{s}.tsv", encoding="utf-8")} for s in ("train", "dev", "test")}
test = rd(f"{out}/tam_test.tsv")
alld = dk["train"] | dk["dev"] | dk["test"]; allr = dkr["train"] | dkr["dev"] | dkr["test"]
keep = [r for r in test if r[2] != "Dakshina" and r[0] not in alld]
with open(f"{out}/tam_test.no_dakshina.tsv", "w", encoding="utf-8") as f:
    f.write("native\troman\tsource\n")
    for r in keep: f.write(f"{r[0]}\t{r[1]}\t{r[2]}\n")
c = C.Counter(r[2] for r in keep)
print("independent test rows", len(keep), "natives", len({r[0] for r in keep}), dict(c), "natives per src", {s: len({r[0] for r in keep if r[2]==s}) for s in c})
print("  of these, roman string also a Dakshina roman string:", sum(r[1] in allr for r in keep))
train = rd(f"{out}/tam_train.tsv.gz", gz=True)
tn = {r[0] for r in train}
# stem proxy: does some Aksharantar-train word share the first k code points with a Dakshina-test word (k = len-2, min 4)?
prefixes = set()
for w in tn:
    for k in range(4, min(len(w), 12) + 1): prefixes.add(w[:k])
hit = 0; ex = []
for w in sorted(dk["test"]):
    k = max(4, len(w) - 2)
    if w[:min(k, 12)] in prefixes: hit += 1; ex.append(w)
print("dak-test words whose (len-2, cap 12) code-point prefix starts some Aksharantar-train word: %d/2500 (%.1f%%)" % (hit, hit/25))
# same proxy for Dakshina train (should be lower due to lemma-disjoint design)
prefixes2 = set()
for w in dk["train"]:
    for k in range(4, min(len(w), 12) + 1): prefixes2.add(w[:k])
hit2 = sum(1 for w in dk["test"] if w[:min(max(4, len(w)-2), 12)] in prefixes2)
print("same proxy vs Dakshina train: %d/2500 (%.1f%%)" % (hit2, hit2/25))
random.seed(1)
for r in random.sample(keep, 6): print("  ", r)
