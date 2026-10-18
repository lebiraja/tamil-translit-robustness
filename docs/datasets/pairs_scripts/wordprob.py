"""Stream IndicXlit ta_word_prob_dict.json out of the remote zip into word\tprob TSV.gz."""
import gzip, io, json, sys
sys.path.insert(0, sys.argv[1])
import rzip  # noqa: E402

url, member, out = sys.argv[2:5]
z = rzip.open_remote(url)
n = 0
with z.open(member) as raw, gzip.open(out, "wt", encoding="utf-8") as g:
    for line in io.TextIOWrapper(raw, encoding="utf-8"):
        line = line.strip().rstrip(",")
        if not line or line in "{}":
            continue
        k, v = line.rsplit(":", 1)
        g.write(f"{json.loads(k)}\t{v.strip()}\n")
        n += 1
print("rows", n)
