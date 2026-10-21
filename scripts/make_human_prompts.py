"""Sample Dakshina TEST words for the human-typed set and write per-typist prompt sheets.

Proposal from docs/human-typing-protocol.md (to confirm with Lebi): 3 typists x 500 words,
100 words shared by all, stratified by word length, fixed seed. Output (gitignored):
  data/human-typed/prompts_T{1,2,3}.tsv   id <TAB> tamil word
  data/human-typed/type_sheet_T{1,2,3}.html  offline typing form that downloads typist_T?.tsv
  data/human-typed/manifest.json
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from translit import data as D  # noqa: E402

SEED, N_SHARED, N_PER, TYPISTS = 424242, 100, 500, 3
OUT = D.ROOT / "data" / "human-typed"

HTML = """<!doctype html><meta charset=utf-8><title>Typing sheet {tid}</title>
<style>body{{font:18px sans-serif;max-width:640px;margin:2em auto}}.w{{font-size:30px;margin:.6em 0 .2em}}
input{{font-size:20px;width:100%;padding:.3em}}button{{font-size:18px;padding:.5em 1em;margin-top:1em}}</style>
<h2>Typist {tid}: type each Tamil word the way you would in a chat, in English letters</h2>
<p>No autocorrect, no copy-paste, no looking things up. Do not fix typos. Skip nothing: if unsure, type what feels natural.
Enter moves to the next word. You can pause and use Download any time (progress is also kept in this browser).</p>
<div id=app></div><button onclick=dl()>Download answers (TSV)</button> <span id=n></span>
<script>
const W={words};const KEY='typesheet_{tid}';let A=JSON.parse(localStorage.getItem(KEY)||'{{}}');
const app=document.getElementById('app');
W.forEach(([id,w],i)=>{{const d=document.createElement('div');d.innerHTML='<div class=w>'+(i+1)+'/'+W.length+'  '+w+'</div>';
const inp=document.createElement('input');inp.autocomplete='off';inp.autocapitalize='off';inp.spellcheck=false;inp.value=A[id]||'';
inp.oninput=()=>{{A[id]=inp.value;localStorage.setItem(KEY,JSON.stringify(A));cnt()}};
inp.onpaste=e=>e.preventDefault();
inp.onkeydown=e=>{{if(e.key==='Enter'){{const nx=app.querySelectorAll('input')[i+1];if(nx)nx.focus()}}}};
d.appendChild(inp);app.appendChild(d)}});
function cnt(){{document.getElementById('n').textContent=Object.values(A).filter(x=>x.trim()).length+'/'+W.length+' done'}}cnt();
function dl(){{const t=W.map(([id,w])=>id+'\\t'+w+'\\t'+(A[id]||'').trim()).join('\\n');
const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([t],{{type:'text/tab-separated-values'}}));a.download='typist_{tid}.tsv';a.click()}}
</script>"""


def main() -> None:
    words = sorted({n for n, _, _ in D.load_lexicon("test")})
    rng = random.Random(SEED)
    by_len: dict[int, list[str]] = {}
    for w in words:
        by_len.setdefault(min(len(w) // 3, 5), []).append(w)
    need = N_SHARED + TYPISTS * (N_PER - N_SHARED)
    pick: list[str] = []
    for b in sorted(by_len):  # proportional stratified sample by length bucket
        k = round(need * len(by_len[b]) / len(words))
        pick += rng.sample(by_len[b], min(k, len(by_len[b])))
    rng.shuffle(pick)
    pick = pick[:need]
    shared, rest = pick[:N_SHARED], pick[N_SHARED:]
    OUT.mkdir(parents=True, exist_ok=True)
    per = N_PER - N_SHARED
    manifest = {"seed": SEED, "source": "Dakshina ta test lexicon natives", "shared": shared, "typists": {}}
    for t in range(TYPISTS):
        tid = f"T{t + 1}"
        mine = shared + rest[t * per : (t + 1) * per]
        random.Random(SEED + t).shuffle(mine)
        items = [(f"{tid}-{i:03d}", w) for i, w in enumerate(mine)]
        (OUT / f"prompts_{tid}.tsv").write_text("\n".join(f"{i}\t{w}" for i, w in items), encoding="utf-8")
        (OUT / f"type_sheet_{tid}.html").write_text(HTML.format(tid=tid, words=json.dumps(items, ensure_ascii=False)), encoding="utf-8")
        manifest["typists"][tid] = len(items)
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    print("sampled", len(pick), "words;", manifest["typists"])


if __name__ == "__main__":
    main()
