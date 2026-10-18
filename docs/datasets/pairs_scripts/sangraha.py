"""Sample Sangraha synthetic tam_Taml + tam_Latn (doc-aligned), save JSONL.gz, extract word pairs."""
import collections as C, gzip, json, re, sys
import pyarrow.parquet as pq
from huggingface_hub import HfFileSystem
out, ngroups = sys.argv[1], int(sys.argv[2])
fs = HfFileSystem()
base = "datasets/ai4bharat/sangraha/synthetic"
T = pq.ParquetFile(fs.open(f"{base}/tam_Taml/wiki_tam_Taml_0000_of_0063.parquet", block_size=8 << 20))
L = pq.ParquetFile(fs.open(f"{base}/tam_Latn/wiki_tam_Latn_0000_of_0063.parquet", block_size=8 << 20))
docs = []
for g in range(ngroups):
    t, l = T.read_row_group(g).to_pylist(), L.read_row_group(g).to_pylist()
    assert len(t) == len(l)
    for a, b in zip(t, l):
        assert a["doc_id"] == b["doc_id"], (g, a["doc_id"], b["doc_id"])
        docs.append({"doc_id": a["doc_id"], "native": a["text"], "roman": b["text"]})
with gzip.open(f"{out}/sangraha_synth_tam_shard0_rg0-{ngroups-1}.jsonl.gz", "wt", encoding="utf-8") as f:
    for d in docs: f.write(json.dumps(d, ensure_ascii=False) + "\n")
print("docs", len(docs))
TA = re.compile(r"^[஀-௿]+$"); LA = re.compile(r"^[a-z]+$")
strip = lambda w: w.strip(".,;:!?()[]{}\"'“”‘’-–—/")
pairs = C.Counter(); lines_tot = lines_ok = 0; tok_n = tok_r = 0
for d in docs:
    nl, rl = d["native"].split("\n"), d["roman"].split("\n")
    if len(nl) != len(rl): continue
    for a, b in zip(nl, rl):
        at, bt = a.split(), b.split()
        if not at: continue
        lines_tot += 1
        if len(at) != len(bt): continue
        lines_ok += 1
        for x, y in zip(at, bt):
            x, y = strip(x), strip(y).lower()
            if TA.match(x) and LA.match(y): pairs[(x, y)] += 1
            tok_n += 1
print("lines", lines_tot, "token-count-aligned", lines_ok, "%.1f%%" % (100 * lines_ok / lines_tot), "tokens", tok_n)
with gzip.open(f"{out}/word_pairs.tsv.gz", "wt", encoding="utf-8") as f:
    f.write("native\troman\tcount\n")
    for (x, y), c in pairs.most_common(): f.write(f"{x}\t{y}\t{c}\n")
nat = C.Counter(); [nat.update({x: 1}) for (x, _) in pairs]
print("word pairs", len(pairs), "native types", len(nat), "roman per native mean %.3f" % (len(pairs) / len(nat)))
