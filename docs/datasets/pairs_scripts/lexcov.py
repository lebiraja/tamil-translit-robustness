"""Lexicon stats: size, Tamil-block validity, malformed starts, coverage of Dakshina words (top-N cutoffs)."""
import gzip, re, sys, unicodedata as U
dak = sys.argv[1]
DEP = set(range(0x0BBE, 0x0BCE)) | {0x0BCD, 0x0BD7, 0x0B82}  # dependent signs, virama, anusvara
TA = re.compile(r"^[஀-௿]+$")
dk = {s: {U.normalize("NFC", l.split("\t")[0]) for l in open(f"{dak}/{s}.tsv", encoding="utf-8")} for s in ("train", "dev", "test")}
def report(name, words):  # words: list ordered by frequency desc (or arbitrary)
    seen, ordered = set(), []
    for w in words:
        w = U.normalize("NFC", w.strip())
        if w and w not in seen: seen.add(w); ordered.append(w)
    ta = [w for w in ordered if TA.match(w)]
    bad = sum(ord(w[0]) in DEP for w in ta)
    print(f"== {name}: types {len(ordered)}, pure-Tamil-block {len(ta)}, start with dependent sign/virama (malformed) {bad}")
    for cut in (50_000, 200_000, 1_000_000, None):
        sub = set(ta[:cut]) if cut else set(ta)
        if cut and cut > len(ta): continue
        print("   top-%s: cover dak-test %.1f%%  dak-dev %.1f%%  dak-train %.1f%%" % (cut or "all", *(100 * len(dk[s] & sub) / len(dk[s]) for s in ("test", "dev", "train"))))
mode = sys.argv[2]
if mode == "wordprob":
    report("IndicXlit ta_word_prob", (l.split("\t", 1)[0] for l in gzip.open(sys.argv[3], "rt", encoding="utf-8")))
elif mode == "csvfreq":
    for p in sys.argv[3:]:
        report(p.rsplit("/", 1)[-1], [l.rsplit(",", 1)[0] for l in open(p, encoding="utf-8")])
elif mode == "plain":
    for p in sys.argv[3:]:
        report(p.rsplit("/", 1)[-1], [l.rstrip("\n") for l in open(p, encoding="utf-8")])
