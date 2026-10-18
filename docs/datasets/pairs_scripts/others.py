import collections as C, re, sys, unicodedata as U, pyarrow.parquet as pq
data, dak = sys.argv[1:3]
nfc = lambda s: U.normalize("NFC", (s or "").strip())
D = {}
for s in ("train", "dev", "test"):
    d = C.defaultdict(set)
    for l in open(f"{dak}/{s}.tsv", encoding="utf-8"):
        n, r, _ = l.rstrip("\n").split("\t"); d[n].add(r)
    D[s] = d
pairs_all = {s: {(n, r) for n, rs in D[s].items() for r in rs} for s in D}
sent = {s: {nfc(l) for l in open(f"{dak}/s{s}.native.txt", encoding="utf-8")} for s in ("dev", "test")}
print("== gowtham58 lexicon")
for sp in ("train", "test"):
    t = pq.read_table(f"{data}/gowtham58-ta-tng-en-lexicon/data/{sp}-00000-of-00001.parquet").to_pylist()
    nat = {nfc(r["ta"]) for r in t}; pr = {(nfc(r["ta"]), (r["tng"] or "").strip().lower()) for r in t}
    print(f" {sp}: rows {len(t)} native types {len(nat)} pairs {len(pr)}; romanizations/native {len(pr)/len(nat):.2f}")
    for s in D:
        print(f"   ∩dakshina-{s}: native {len(nat & set(D[s]))} ({100*len(nat & set(D[s]))/len(D[s]):.1f}% of dak {s}), exact pairs {len(pr & pairs_all[s])}")
print("== gowtham58 sentences")
for sp in ("train", "test"):
    t = pq.read_table(f"{data}/gowtham58-ta-tng-en/data/{sp}-00000-of-00001.parquet").to_pylist()
    nat = [nfc(r["ta"]) for r in t]
    print(f" {sp}: rows {len(t)}; in dakshina sent dev {sum(n in sent['dev'] for n in nat)} test {sum(n in sent['test'] for n in nat)}; single-token rows {sum(len(n.split())==1 for n in nat)}")
    single = {n for n in nat if len(n.split()) == 1}
    for s in D: print(f"   single-token natives ∩ dakshina-{s} lexicon: {len(single & set(D[s]))}")
print("== polyglots NER transliterated")
TA = re.compile(r"^[஀-௿]+$")
wp = C.Counter(); mis = 0; n = 0
for sp in ("train", "validation"):
    for r in pq.read_table(f"{data}/polyglots-tamil-ner-transliterated/data/{sp}-00000-of-00001.parquet").to_pylist():
        a, b = list(r["input"]), list(r["transliterated_input"]); n += 1
        if len(a) != len(b): mis += 1; continue
        for x, y in zip(a, b):
            if TA.match(nfc(x)) and y.isascii() and y.isalpha(): wp[(nfc(x), y.lower())] += 1
nat = {x for x, _ in wp}
print(f" sentences {n}, token-misaligned {mis}, word pairs {len(wp)}, native types {len(nat)}, roman/native {len(wp)/len(nat):.3f}")
for s in D: print(f"   ∩dakshina-{s}: native {len(nat & set(D[s]))}")
agree = [x for x in nat if x in D['train'] or x in D['test'] or x in D['dev']]
m = sum(any(y in (D['train'].get(x, set()) | D['dev'].get(x, set()) | D['test'].get(x, set())) for (xx, y) in wp if xx == x) for x in agree)
print(f"   of overlapping natives, romanization equals a Dakshina human variant: {m}/{len(agree)}")
