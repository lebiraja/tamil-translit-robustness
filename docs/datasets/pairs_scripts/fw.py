import sys, pyarrow.parquet as pq, collections as C
f = pq.ParquetFile(sys.argv[1]); print(f.schema_arrow.names, "rows", f.metadata.num_rows)
t = f.read(columns=["text"]).column("text").to_pylist()
ch = sum(len(x) for x in t); print("chars %.1fM, mean doc %d chars" % (ch / 1e6, ch / len(t)))
ta = sum(1 for x in t for c in x if 0x0B80 <= ord(c) <= 0x0BFF); print("Tamil-block char share %.1f%%" % (100 * ta / ch))
print("words %.1fM" % (sum(len(x.split()) for x in t) / 1e6))
for x in t[:3]: print("  ", x[:200].replace("\n", " "))
