"""Upload the final checkpoints to a PRIVATE Hugging Face model repo. The token is read from the HF_TOKEN environment variable only.

  HF_TOKEN=... python scripts/push_to_hf.py --repo <user>/tamil-translit-robustness-models [--dry]
Uploads runs/<name>-s<seed>/best.pt for every C3/C2 result (renamed <name>-s<seed>.pt), the two reproduction-gate models and the
reverse (Tamil->Latin) model used to synthesise A3, plus README.md (model card) and MANIFEST.json (sha256, results, commit).
Each .pt is a torch checkpoint {model, kw, arch, vocab}; rebuild with translit.models.build(arch, len(vocab.src), len(vocab.tgt), **kw).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

import pandas as pd
from huggingface_hub import CommitOperationAdd, HfApi

ROOT = Path(__file__).resolve().parents[1]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def collect() -> list[tuple[str, Path, dict]]:
    out = []
    for blk in ("c3", "c2"):
        for j in sorted((ROOT / "results" / blk).glob("*.json")):
            d = json.loads(j.read_text())
            run = j.stem
            ck = ROOT / "runs" / run / "best.pt"
            if ck.exists():
                out.append((f"models/{blk}/{run}.pt", ck, {"block": blk, "arch": d["config"]["arch"], "seed": d["config"]["seed"],
                                                           "n_params": d["n_params"], "dev_cer": d["dev"]["cer"], "test_cer": d["test"]["cer"],
                                                           "test_top1": d["test"]["top1"], "code_commit": d.get("commit")}))
    for run, role in (("gate-lstm-3m-s0", "reproduction gate"), ("gate-transformer-3m-s0", "reproduction gate"),
                      ("reverse-lstm-s0", "Tamil->Latin model used to synthesise A3 data")):
        ck = ROOT / "runs" / run / "best.pt"
        if ck.exists():
            out.append((f"models/other/{run}.pt", ck, {"block": "other", "role": role}))
    return out


def card(items: list, commit: str) -> str:
    c3 = pd.read_csv(ROOT / "results/summary/c3_clean.csv")
    rows = "\n".join(f"| {r.arch} | {r['size']} | {r.n_params_mean / 1e6:.2f}M | {r.test_cer_mean:.2f} ± {r.test_cer_sd:.2f} | {r.test_top1_mean:.1f} |"
                     for _, r in c3.iterrows())
    return f"""---
library_name: pytorch
tags: [transliteration, tamil, romanized-tamil, robustness, research]
---
# Tamil transliteration robustness: trained checkpoints (private)

Character-level Latin (romanized/"Tanglish") to Tamil-script word transliteration models from an IA3 deep-learning project
(topic 34). {len(items)} checkpoints: 30 C3 models (BiLSTM+attention and pre-LN Transformer at about 1M/3M/8M parameters, 5 seeds),
80 C2 augmentation models (3M parameters, conditions A0-A4, CTRL, A2-noGEM, A2-noVDROP, 5 seeds), 2 reproduction-gate models and the
reverse model used to synthesise the A3 training data. All trained from scratch on Dakshina Tamil (plus, for A3/A4/CTRL, synthetic
romanizations of a word list that excludes every Dakshina and independent-test word). Code, configs, results and the paper draft live in
the private GitHub repo `lebiraja/tamil-translit-robustness` (code commit `{commit}`).

## Use
Each `.pt` is `torch.save({{"model": state_dict, "kw": model kwargs, "arch": "lstm"|"transformer", "vocab": {{"src": [...], "tgt": [...]}}}})`.
Rebuild with `translit.models.build(arch, len(vocab["src"]), len(vocab["tgt"]), **kw)` and decode with `translit.decode.beam_search`
(beam 10 was used for every reported number). See `scripts/evaluate_ckpt.py` in the GitHub repo.

## Results (clean Dakshina test, mean ± sd over 5 seeds, beam 10)
| arch | size | params | test CER | top-1 % |
|---|---|---|---|---|
{rows}

Full tables, noisy-test results, statistics and limitations: `docs/results.md` in the GitHub repo. `MANIFEST.json` lists every file with
its sha256, parameter count and logged dev/test scores.

## Caveats
- Dakshina is formal Wikipedia-derived romanization, not chat text; robustness numbers are on synthetic noise (human-typed and WhatsApp sets are not evaluated).
- Provenance incident: 33 C2 runs shared checkpoint folders with duplicate training processes; one run that failed the checkpoint-vs-log check was retrained and replaced. All stored checkpoints were re-scored against their logs (see `docs/results.md` section 5 and `FIXES.md` F3).
- Private research artifact; no license granted. Check the dataset licences listed in `docs/datasets/` before any redistribution.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--batch", type=int, default=12)
    a = ap.parse_args()
    items = collect()
    commit = subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], text=True).strip()
    manifest = {"code_commit": commit, "files": {p: {"sha256": sha256(f), "bytes": f.stat().st_size, **meta} for p, f, meta in items}}
    print(f"{len(items)} checkpoints, {sum(m['bytes'] for m in manifest['files'].values()) / 1e9:.2f} GB")
    if a.dry:
        return
    api = HfApi(token=os.environ["HF_TOKEN"])
    api.create_repo(a.repo, repo_type="model", private=True, exist_ok=True)
    api.create_commit(a.repo, operations=[
        CommitOperationAdd("README.md", card(items, commit).encode()),
        CommitOperationAdd("MANIFEST.json", json.dumps(manifest, indent=1).encode())], commit_message="model card and manifest")
    for i in range(0, len(items), a.batch):
        ops = [CommitOperationAdd(p, str(f)) for p, f, _ in items[i : i + a.batch]]
        api.create_commit(a.repo, operations=ops, commit_message=f"checkpoints {i + 1}-{i + len(ops)}")
        print(f"uploaded {i + len(ops)}/{len(items)}", flush=True)
    info = api.model_info(a.repo)
    print("repo private:", info.private, "files:", len(info.siblings))


if __name__ == "__main__":
    main()
