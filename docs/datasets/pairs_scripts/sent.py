import json, sys, collections as C, unicodedata as U
src, out, dak = sys.argv[1:4]
d = json.load(open(src, encoding="utf-8"))
print("top keys", list(d.keys()), "total", len(d["data"]))
print("langs", C.Counter(x["unique_identifier"].rsplit("_", 1)[0] for x in d["data"]))
print("fields", list(d["data"][0].keys()))
ta = [x for x in d["data"] if x["unique_identifier"].startswith("ta_")]
with open(out, "w", encoding="utf-8") as f:
    f.write("id\tnative\troman\n")
    for x in ta:
        f.write(f'{x["unique_identifier"]}\t{x["native sentence"].replace(chr(9)," ").strip()}\t{x["romanized sentence"].replace(chr(9)," ").strip()}\n')
print("tamil", len(ta))
nat = [U.normalize("NFC", x["native sentence"].strip()) for x in ta]
dk = {s: {U.normalize("NFC", l.strip()) for l in open(f"{dak}/s{s}.native.txt", encoding="utf-8")} for s in ("dev", "test")}
print("in dakshina sent dev", sum(n in dk["dev"] for n in nat), "test", sum(n in dk["test"] for n in nat), "unique", len(set(nat)))
toks = [len(n.split()) for n in nat]; print("tokens/sent mean %.1f" % (sum(toks)/len(toks)))
lex = {l.split("\t")[0] for l in open(f"{dak}/test.tsv", encoding="utf-8")}
words = {w.strip(".,;:!?()\"'") for n in nat for w in n.split()}
print("sentence vocab", len(words), "∩ dakshina test words", len(words & lex))
for x in ta[:3] + ta[-2:]: print(" ", x["native sentence"][:120], "|||", x["romanized sentence"][:120])
