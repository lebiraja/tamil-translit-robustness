"""Token-level script/language shares and informal-pattern rates for Tanglish corpora.
Heuristic measurement tool, not a model. Usage: python -I tanglish_measure.py DATA_DIR DAK_DIR DAK_SENT OUT_JSON"""
from __future__ import annotations
import ast, gzip, json, math, random, re, sys, unicodedata
from collections import Counter, defaultdict
from pathlib import Path
import pandas as pd
from wordfreq import zipf_frequency, iter_wordlist

DATA, DAK, DAK_SENT, OUT = map(Path, sys.argv[1:5])
TA_BLOCK = re.compile(r"[஀-௿]")
TOKEN = re.compile(r"[஀-௿‌‍]+|[A-Za-z]+(?:'[A-Za-z]+)?|\d+[A-Za-z]*|[A-Za-z]+\d+[A-Za-z\d]*")
VOW = set("aeiou")
# Short Tamil function words that collide with frequent English/other strings; forced to TA.
TA_FORCE = set("""da di pa ma la na nu ku ah aa eh dei di ji ra ya po va vaa naa nee ne un en
oru illa illai enna ena inga anga avan ava ivan iva anna akka thala thalaiva thalaivar vera
sema semma padam ponga vanga ivlo evlo apo ipo appo ippo epdi eppadi romba nalla nala mattum
thaan dhan dhaan tha thaa kitta mela kela pola mari maari machan macha bro""".split()) - {"bro"}

def squeeze(t: str, n: int = 2) -> str:
    return re.sub(r"(.)\1{%d,}" % n, lambda m: m.group(1) * n, t)

def runs1(t: str) -> str:  # collapse every run to one char
    return re.sub(r"(.)\1+", r"\1", t)

def vlen_key(t: str) -> str:  # collapse vowel runs only
    return re.sub(r"([aeiou])\1+", r"\1", t)

def gem_key(t: str) -> str:  # collapse consonant runs only
    return re.sub(r"([b-df-hj-np-tv-z])\1+", r"\1", t)

def h_key(t: str) -> str:
    return re.sub(r"(?<=[^aeiouh])h", "", t)

def skel(t: str) -> str:
    return re.sub(r"[aeiou]+", "", t)

def is_subseq(a: str, b: str) -> bool:
    it = iter(b)
    return all(c in it for c in a)

# ---------------- lexicons
dak_roman: set[str] = set()
for f in ("train.tsv", "dev.tsv", "test.tsv"):
    for line in open(DAK / f, encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) >= 2:
            dak_roman.add(p[1].lower())
ak_roman: set[str] = set()
with gzip.open(DATA / "aksharantar-tamil/tam_train.tsv.gz", "rt", encoding="utf-8") as fh:
    next(fh)
    for line in fh:
        p = line.split("\t")
        if len(p) >= 3 and p[2] in ("Dakshina", "IndicCorp", "AK-Freq", "Existing"):
            ak_roman.add(p[1].lower())
ta_lex = dak_roman | ak_roman
print("lexicon sizes dak", len(dak_roman), "ak", len(ak_roman), file=sys.stderr)

# ---------------- char n-gram NB for OOV Latin tokens
def grams(w: str) -> list[str]:
    s = f"<{w}>"
    return [s[i:i + n] for n in (2, 3, 4) for i in range(len(s) - n + 1)]
en_words = [w for w in iter_wordlist("en") if w.isascii() and w.isalpha()][:40000]
rng = random.Random(0)
ta_train = [w for w in dak_roman if zipf_frequency(w, "en") < 3.0] + rng.sample(sorted(ak_roman), 60000)
nb: dict[str, Counter] = {"en": Counter(), "ta": Counter()}
for lab, ws in (("en", en_words), ("ta", ta_train)):
    for w in ws:
        nb[lab].update(grams(w))
tot = {k: sum(v.values()) for k, v in nb.items()}
V = len(set(nb["en"]) | set(nb["ta"]))
def nb_label(w: str) -> str:
    sc = {}
    for lab in ("en", "ta"):
        sc[lab] = sum(math.log((nb[lab][g] + 0.5) / (tot[lab] + 0.5 * V)) for g in grams(w))
    return "ta" if sc["ta"] > sc["en"] else "en"

def latin_lid(tok: str) -> str:
    t = squeeze(tok.lower())
    if t in TA_FORCE or runs1(t) in TA_FORCE:
        return "ta"
    z = zipf_frequency(t, "en")
    if z >= 4.0:
        return "en"
    if t in ta_lex:
        return "ta"
    if z >= 3.0:
        return "en"
    return nb_label(t)

# ---------------- validation on EnTaCs manual tags (single non-Tamil-proficient annotator)
def validate() -> dict:
    gold = []
    for f in ("train.conll", "val.conll"):
        for line in open(DATA / "entacs-langid" / f, encoding="utf-8"):
            p = line.split()
            if len(p) == 2 and p[1] in ("en", "ta") and re.fullmatch(r"[A-Za-z]+", p[0]):
                gold.append((p[0], p[1]))
    pred = [latin_lid(w) for w, _ in gold]
    acc = sum(p == g for p, (_, g) in zip(pred, gold)) / len(gold)
    conf = Counter((g, p) for p, (_, g) in zip(pred, gold))
    dis = [(w, g, p) for p, (w, g) in zip(pred, gold) if p != g]
    return {"n": len(gold), "acc": acc, "confusion_gold_pred": {f"{g}->{p}": c for (g, p), c in conf.items()},
            "disagreements_sample": random.Random(1).sample(dis, min(40, len(dis)))}

# ---------------- loaders
def l_dcm():
    out = []
    for line in open(DATA / "dravidiancodemix-zenodo/DravidianCodeMix/tamil_sentiment_full.csv", encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if len(p) == 2:
            out.append(p[1])
    return out
def l_tms():
    return pd.concat([pd.read_parquet(f) for f in sorted((DATA / "hf-tamilmixsentiment/data").glob("*.parquet"))]).text.tolist()
def l_hope():
    out = []
    for f in sorted((DATA / "hopeedi-tamil").glob("*.csv")):
        for line in open(f, encoding="utf-8"):
            out.append(line.split("\t")[0])
    return out
def l_tamhatex():
    return pd.read_csv(DATA / "tamhatex-mendeley/TamHateX_V4_final.csv", encoding="utf-8-sig").Input_Text.astype(str).tolist()
def l_vishnu():
    d = pd.read_json(DATA / "vishnu-tanglish-corpus-185k/tanglish_corpus.jsonl", lines=True)
    return d[d.source != "dravidiancodemix"].text.tolist()
def l_krishan():
    return pd.concat([pd.read_csv(DATA / f"krishan-tamil-hate-speech/{s}.csv") for s in ("train", "test")]).text.astype(str).tolist()
def l_sts():
    d = pd.read_json(DATA / "vishnu-tanglish-sts/tanglish_sts.jsonl", lines=True)
    return d.s1.tolist() + d.s2.tolist()
def l_karky():
    d = pd.read_csv(DATA / "karky-lyrics-tanglish-tamil/tamengl.csv")
    out = []
    for x in d.Tanglishlyrics:
        try:
            out += ast.literal_eval(x)
        except Exception:
            pass
    return out
def l_dak():
    return [l.rstrip("\n").split("\t")[1] for l in open(DAK_SENT, encoding="utf-8") if "\t" in l]

SETS = {"DravidianCodeMix-Tamil (Zenodo)": l_dcm, "TamilMixSentiment (HF)": l_tms, "HopeEDI-Tamil": l_hope,
        "TamHateX v4": l_tamhatex, "Tanglish-Corpus-185k (non-DCM rows)": l_vishnu, "Tamil_Hate_Speech (krishan-CSE)": l_krishan,
        "TanglishSTS": l_sts, "karky lyrics (Tanglish side)": l_karky, "Dakshina romanized sentences (formal baseline)": l_dak}

# ---------------- per-dataset measurement
def measure(texts: list[str]) -> dict:
    tok_c = Counter(); line_c = Counter(); ta_toks: list[str] = []
    for s in texts:
        s = unicodedata.normalize("NFC", str(s))
        toks = TOKEN.findall(s)
        has_ta = has_lat = False
        for t in toks:
            if TA_BLOCK.search(t):
                tok_c["tamil_script"] += 1; has_ta = True
            elif re.fullmatch(r"[A-Za-z]+(?:'[A-Za-z]+)?", t):
                has_lat = True
                lab = latin_lid(t.replace("'", ""))
                tok_c["latin_" + lab] += 1
                if lab == "ta":
                    ta_toks.append(t.replace("'", ""))
            elif re.search(r"[A-Za-z]", t):
                tok_c["latin_alnum_mix"] += 1; has_lat = True
            else:
                tok_c["number"] += 1
        line_c["tamil_script_only" if has_ta and not has_lat else "latin_only" if has_lat and not has_ta
               else "mixed_script" if has_ta else "no_words"] += 1
    words = sum(v for k, v in tok_c.items() if k != "number")
    shares = {k: round(100 * v / words, 2) for k, v in tok_c.items() if k != "number"} if words else {}
    # informal patterns on Latin-Tamil tokens; variant matching against Dakshina roman lexicon only
    # (human romanizations), directional: the observed token must be SHORTER than the lexicon form.
    pat = Counter(); examples = defaultdict(list)
    low = [t.lower() for t in ta_toks]
    oov = {squeeze(x) for x in low} - dak_roman
    keyfns = {"vowel_length_collapse": vlen_key, "geminate_collapse": gem_key,
              "length+geminate_collapse": runs1, "h_drop": h_key}
    want = {k: {f(t) for t in oov} for k, f in keyfns.items()}
    want["vowel_drop"] = {skel(runs1(t)) for t in oov}
    idx = {k: defaultdict(list) for k in want}
    for w in dak_roman:
        for k, f in keyfns.items():
            kk = f(w)
            if kk in want[k]: idx[k][kk].append(w)
        kk = skel(runs1(w))
        if kk in want["vowel_drop"]: idx["vowel_drop"][kk].append(w)
    nv = lambda x: len(re.findall(r"[aeiou]+", x))
    cls = {}
    for t in oov:
        hit = None
        for k, f in keyfns.items():
            m = [w for w in idx[k].get(f(t), []) if len(w) > len(t)]
            if m: hit = (k, min(m, key=len)); break
        if not hit:
            m = [w for w in idx["vowel_drop"].get(skel(runs1(t)), []) if nv(runs1(w)) > nv(runs1(t)) and is_subseq(runs1(t), runs1(w))]
            if m: hit = ("vowel_drop", min(m, key=len))
        cls[t] = hit or (("in_aksharantar_only" if t in ta_lex else "oov_other"), "")
    n = len(low)
    for raw, t0 in zip(ta_toks, low):
        t = squeeze(t0)
        if re.search(r"(.)\1\1", t0): pat["elongation_3plus"] += 1; examples["elongation_3plus"].append((raw, ""))
        if raw.isupper() and len(raw) > 1: pat["all_caps"] += 1
        if t in dak_roman: pat["in_dakshina_lexicon"] += 1
        else:
            c, w = cls[t]; pat[c] += 1; examples[c].append((raw, w))
        if not (set(t) & VOW): pat["no_vowel"] += 1; examples["no_vowel"].append((raw, ""))
    rates = {k: round(100 * v / n, 2) for k, v in pat.items()} if n else {}
    rng = random.Random(0); sample = []
    for c in ("vowel_drop", "geminate_collapse", "vowel_length_collapse", "length+geminate_collapse", "h_drop", "elongation_3plus", "no_vowel", "oov_other"):
        ex = sorted(set(examples[c]))
        sample += [(c, a, b) for a, b in rng.sample(ex, min(4 if c != "oov_other" else 3, len(ex)))]
    top = Counter(low).most_common(30)
    return {"n_texts": len(texts), "n_word_tokens": words, "token_shares_pct": shares, "text_script_pct":
            {k: round(100 * v / len(texts), 2) for k, v in line_c.items()}, "n_latin_ta_tokens": n,
            "latin_ta_pattern_pct": rates, "pattern_samples": sample, "top_latin_ta_tokens": top}

res = {"validation_vs_entacs_manual": validate()}
print(json.dumps(res["validation_vs_entacs_manual"], ensure_ascii=False)[:600], file=sys.stderr)
for name, fn in SETS.items():
    texts = fn()
    res[name] = measure(texts)
    print(name, res[name]["n_texts"], res[name]["token_shares_pct"], file=sys.stderr)
OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1))
