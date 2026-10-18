import collections as C, re, sys, unicodedata as U
mode, p, dak = sys.argv[1:4]
W = re.compile(r"[஀-௿]+")
cnt = C.Counter(); lines = 0; chars = 0
if mode == "parquet":
    import pyarrow.parquet as pq
    it = pq.read_table(p, columns=["text"]).column("text").to_pylist()
else:
    it = open(p, encoding="utf-8", errors="replace")
bad = 0
for t in it:
    if mode == "txt" and "�" in t: bad += 1
    lines += 1; chars += len(t); cnt.update(W.findall(U.normalize("NFC", t)))
print(f"{mode}: docs/lines {lines}, chars {chars/1e6:.1f}M, Tamil tokens {sum(cnt.values())/1e6:.2f}M, types {len(cnt)}, lines with U+FFFD {bad}")
for s in ("train", "test"):
    dn = {l.split("\t")[0] for l in open(f"{dak}/{s}.tsv", encoding="utf-8")}
    print(f"  dakshina-{s} words present: {100*sum(w in cnt for w in dn)/len(dn):.1f}%")
