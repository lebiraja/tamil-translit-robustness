"""kaikki Tamil Wiktionary: headwords + forms + romanizations -> lexicon and (native, ISO-roman) pairs."""
import collections as C, json, re, sys, unicodedata as U
src, outdir, dak = sys.argv[1:4]
TA = re.compile(r"^[஀-௿]+$")
heads, forms, roms = set(), set(), {}
pos = C.Counter(); n = 0
for line in open(src, encoding="utf-8"):
    e = json.loads(line); n += 1
    w = U.normalize("NFC", e.get("word", "")); pos[e.get("pos")] += 1
    if TA.match(w): heads.add(w)
    for f in e.get("forms", []) or []:
        fw = U.normalize("NFC", f.get("form", ""))
        tags = f.get("tags", []) or []
        if "romanization" in tags and TA.match(w): roms.setdefault(w, fw)
        elif TA.match(fw): forms.add(fw)
lex = heads | forms
print("entries", n, "pos", pos.most_common(6))
print("Tamil headwords", len(heads), "inflected/other forms", len(forms), "union", len(lex), "headwords with romanization", len(roms))
open(f"{outdir}/tamil_wiktionary_wordlist.txt", "w", encoding="utf-8").write("\n".join(sorted(lex)) + "\n")
with open(f"{outdir}/headword_romanization.tsv", "w", encoding="utf-8") as f:
    f.write("native\tromanization_iso\n")
    for w in sorted(roms): f.write(f"{w}\t{roms[w]}\n")
for s in ("train", "dev", "test"):
    dn = {l.split("\t")[0] for l in open(f"{dak}/{s}.tsv", encoding="utf-8")}
    print(f"  coverage of dakshina-{s}: {100*len(dn & lex)/len(dn):.1f}% (headwords only {100*len(dn & heads)/len(dn):.1f}%)")
for w in list(sorted(roms))[200:205]: print("  ", w, roms[w])
