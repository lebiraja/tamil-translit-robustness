"""Romanize Dakshina test natives with rule-based tools; agreement with human romanizations."""
import collections as C, sys, re, unicodedata as U, warnings
warnings.filterwarnings("ignore")
from aksharamukha import transliterate as AK
from indic_transliteration import sanscript as SS
dak = sys.argv[1]
d = C.defaultdict(dict)
for l in open(f"{dak}/test.tsv", encoding="utf-8"):
    n, r, c = l.rstrip("\n").split("\t"); d[n][r] = int(c)
def norm(s):  # strip diacritics, lowercase, keep a-z
    s = U.normalize("NFD", s.lower()); return re.sub(r"[^a-z]", "", s)
words = sorted(d)
tools = {
  "aksharamukha:ISO": lambda w: AK.process("Tamil", "ISO", w),
  "aksharamukha:IAST": lambda w: AK.process("Tamil", "IAST", w),
  "aksharamukha:HK": lambda w: AK.process("Tamil", "HK", w),
  "indic_transliteration:ITRANS": lambda w: SS.transliterate(w, SS.TAMIL, SS.ITRANS),
  "indic_transliteration:OPTITRANS": lambda w: SS.transliterate(w, SS.TAMIL, SS.OPTITRANS),
}
for name, f in tools.items():
    try:
        out = {w: f(w) for w in words}
    except Exception as e:
        print(name, "ERR", e); continue
    any_m = sum(norm(out[w]) in d[w] for w in words)
    top_m = sum(norm(out[w]) == max(d[w], key=d[w].get) for w in words)
    print(f"{name}: matches some human variant {100*any_m/len(words):.1f}%, top variant {100*top_m/len(words):.1f}%  e.g. " + "; ".join(f"{w}->{out[w]}" for w in words[100:104]))
