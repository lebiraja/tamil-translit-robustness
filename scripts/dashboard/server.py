"""Live training dashboard for Leica. Plain python3 (no dependencies), read-only.

  python3 scripts/dashboard/server.py [--port 8383]
Serves static/index.html and a JSON API built from logs/*.log and results/**/*.json on every poll (cached by mtime).
GET /api/state       everything the page draws          GET /api/tail?file=NAME.log&n=200   last lines of a log
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parents[2]
LOGS, RESULTS = ROOT / "logs", ROOT / "results"
LINE = re.compile(r"\[(?P<run>[^\]]+)\] ep(?P<ep>\d+) loss (?P<loss>[\d.]+) devCER\(greedy\) (?P<cer>[\d.]+|nan)")
STATIC = Path(__file__).resolve().parent / "static"
_cache: dict[str, tuple[float, object]] = {}


def sh(cmd: list[str], t: int = 5) -> str:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=t).stdout
    except Exception:
        return ""


def parse_log(p: Path) -> dict:
    """Return {run: {ep:[], loss:[], cer:[]}} and the last run name, cached by mtime."""
    key = str(p)
    m = p.stat().st_mtime
    if key in _cache and _cache[key][0] == m:
        return _cache[key][1]  # type: ignore[return-value]
    runs: dict[str, dict[str, list]] = {}
    last = None
    for line in p.read_text(errors="ignore").splitlines():
        g = LINE.search(line)
        if g:
            r = runs.setdefault(g["run"], {"ep": [], "loss": [], "cer": []})
            r["ep"].append(int(g["ep"]))
            r["loss"].append(float(g["loss"]))
            r["cer"].append(None if g["cer"] == "nan" else float(g["cer"]))
            last = g["run"]
    out = {"runs": runs, "last": last}
    _cache[key] = (m, out)
    return out


def gpu() -> dict:
    o = sh(["nvidia-smi", "--query-gpu=name,temperature.gpu,power.draw,power.limit,utilization.gpu,memory.used,memory.total,fan.speed",
            "--format=csv,noheader,nounits"]).strip().split(", ")
    try:
        return dict(name=o[0], temp=float(o[1]), power=float(o[2]), power_limit=float(o[3]), util=float(o[4]),
                    mem_used=float(o[5]), mem_total=float(o[6]), fan=o[7])
    except Exception:
        return {}


def system() -> dict:
    load = open("/proc/loadavg").read().split()[:3]
    mem = {l.split(":")[0]: int(l.split()[1]) for l in open("/proc/meminfo") if ":" in l}
    st = subprocess.os.statvfs("/")
    return dict(load=[float(x) for x in load], mem_used_gb=(mem["MemTotal"] - mem["MemAvailable"]) / 1048576,
                mem_total_gb=mem["MemTotal"] / 1048576, disk_free_gb=st.f_bavail * st.f_frsize / 1e9,
                kernel=sh(["uname", "-r"]).strip(), uptime_s=float(open("/proc/uptime").read().split()[0]))


def results() -> list[dict]:
    out = []
    for f in sorted(RESULTS.glob("*/*.json")):
        if f.parent.name in ("summary", "items"):
            continue
        key = str(f)
        m = f.stat().st_mtime
        if key not in _cache or _cache[key][0] != m:
            try:
                d = json.loads(f.read_text())
                c = d["config"]
                row = dict(file=f.name[:-5], block=f.parent.name, name=c["name"], seed=c["seed"], arch=c["arch"], params=d["n_params"],
                           dev=d.get("dev"), test=d.get("test"), wall_s=d.get("wall_s"), mtime=m,
                           hp={k: c[k] for k in ("lr", "batch_size", "dropout", "label_smoothing", "warmup") if k in c},
                           noisy={k: v["cer"] for k, v in d.get("noisy", {}).items()},
                           independent={k: v["cer"] for k, v in d.get("independent", {}).items()},
                           history=d.get("history", []))
            except Exception as e:  # half-written file
                row = dict(file=f.name[:-5], block=f.parent.name, error=str(e))
            _cache[key] = (m, row)
        out.append(_cache[key][1])
    return out


# ---------- Plan tab: checklist and time estimate (everything derived from files on disk) ----------
ARCHS = (("lstm", "BiLSTM"), ("transformer", "Transformer"))
SIZES = ("1m", "3m", "8m")
C2_CONDS = ("A0", "A1", "A2", "A3", "A4", "CTRL", "A2-noGEM", "A2-noVDROP")
C2_COST = {"A3": 2.8, "A4": 2.8, "CTRL": 1.9}  # extra training pairs make an epoch longer
FALLBACK_MIN = {("lstm", "1m"): 7, ("lstm", "3m"): 9, ("lstm", "8m"): 14, ("transformer", "1m"): 20, ("transformer", "3m"): 25,
                ("transformer", "8m"): 45}  # per final run, only used until a real run of that kind has finished
TUNE_FALLBACK_MIN = {"lstm": 4, "transformer": 11}
EVAL_MIN, AGG_MIN, DOCS_MIN, PARALLEL = 4.3, 5, 45, 2


def plan(rows: list[dict], st: dict) -> dict:
    now = time.time()
    ok = [r for r in rows if "error" not in r]

    def n_of(prefix: str) -> int:
        return sum(1 for r in ok if r["block"] == prefix[0] and r["name"] == prefix[1])

    def walls(block: str, name: str) -> list[float]:
        return [r["wall_s"] / 60 for r in ok if r["block"] == block and r["name"] == name and r.get("wall_s")]

    tune_t = [r["mtime"] - r["wall_s"] for r in ok if r["block"] == "tune" and r.get("wall_s")]
    start = min(tune_t) if tune_t else now
    done_f = LOGS / "AUTOPILOT_DONE"
    finished = done_f.exists()
    end = done_f.stat().st_mtime if finished else None

    def avg(xs: list[float], fb: float) -> float:
        return sum(xs) / len(xs) if xs else fb

    groups, est = [], {}
    # --- tuning
    items, rem_tune = [], 0.0
    for a, label in ARCHS:
        for sz in SIZES:
            name = f"{a}-{sz}"
            n = min(20, sum(1 for r in ok if r["block"] == "tune" and r["name"].startswith(name + "-t")))
            fb = TUNE_FALLBACK_MIN[a] * (1.5 if sz == "8m" and a == "transformer" else 1)
            per = avg([r["wall_s"] / 60 for r in ok if r["block"] == "tune" and r["name"].startswith(name + "-t") and r.get("wall_s")], fb)
            rem_tune = max(rem_tune, (20 - n) * per)
            items.append(dict(label=f"{label} {sz.upper()} tuned", progress=[n, 20], done=(ROOT / f"configs/best_{a}_{sz}.yaml").exists()))
    groups.append(dict(title="Hyperparameter tuning (20 trials each, dev CER only)", items=items))
    # --- C3
    items, rem3, rem3_big = [], 0.0, 0.0
    for a, label in ARCHS:
        for sz in SIZES:
            name = f"c3-{a}-{sz}"
            n = min(5, n_of(("c3", name)))
            per = avg(walls("c3", name), FALLBACK_MIN[(a, sz)])
            if a == "transformer" and sz == "8m":
                rem3_big += (5 - n) * per
            else:
                rem3 += (5 - n) * per
            items.append(dict(label=f"{label} {sz.upper()} trained, 5 seeds", progress=[n, 5], done=n >= 5))
    groups.append(dict(title="C3: architecture comparison (clean training)", items=items))
    # --- C2
    items, rem2 = [], 0.0
    for a, label in ARCHS:
        base = avg([w for sz in ("3m",) for w in walls("c3", f"c3-{a}-{sz}")], FALLBACK_MIN[(a, "3m")])
        for cond in C2_CONDS:
            n = min(5, n_of(("c2", f"c2-{a}-{cond}")))
            rem2 += (5 - n) * base * C2_COST.get(cond, 1.0)
            items.append(dict(label=f"{label} {cond}", progress=[n, 5], done=n >= 5))
    groups.append(dict(title="C2: augmentation conditions (3M parameters)", items=items))
    # --- analysis
    n_items = len(list((ROOT / "results/items").glob("*.npz"))) if (ROOT / "results/items").exists() else 0
    res_md = ROOT / "docs/results.md"
    summary = ROOT / "results/summary/summary.json"
    last_run = max([r["mtime"] for r in ok if r["block"] in ("c3", "c2")] or [0])
    handover = ROOT / "HANDOVER.md"
    items = [
        dict(label="Per-item evaluation of every trained model", progress=[n_items, 110], done=n_items >= 110),
        dict(label="Aggregation: tables, bootstrap, Kruskal-Wallis / Dunn", done=summary.exists()),
        dict(label="docs/results.md written", done=res_md.exists() and res_md.stat().st_size > 1500),
        dict(label="HANDOVER.md rewritten after the last run", done=last_run > 0 and handover.stat().st_mtime > last_run and summary.exists()),
        dict(label="logs/AUTOPILOT_DONE written", done=finished),
    ]
    groups.append(dict(title="Analysis and wrap-up", items=items))
    setup = [
        dict(label="Reproduction gate passed (BiLSTM and Transformer)", done=len([r for r in ok if r["block"] == "gate"]) >= 2),
        dict(label="28 noisy test suites built", done=len(list((ROOT / "data/synth/noisy_test").glob("test.*.tsv"))) >= 28),
        dict(label="A3 sampled back-transliteration pool", done=(ROOT / "data/synth/a3_sampled.tsv").exists()),
        dict(label="Resume, retry and supervisor in place", done=(ROOT / "scripts/supervisor.py").exists()),
        dict(label="Analysis scripts written and tested", done=(ROOT / "scripts/aggregate.py").exists() and (ROOT / "scripts/evaluate_ckpt.py").exists()),
    ]
    groups.insert(0, dict(title="Set-up (done before the long runs)", items=setup))
    # --- time estimate (rough: assumes no crashes and that the final write-up happens when Claude is online)
    c3_end = max(rem3 / PARALLEL, rem_tune) + rem3_big / PARALLEL
    c2_end = c3_end + rem2 / PARALLEL
    eval_serial = EVAL_MIN * max(0, 110 - n_items)
    eval_end = max(c2_end + 2 * EVAL_MIN, eval_serial)
    total_min = 0.0 if finished else eval_end + AGG_MIN + DOCS_MIN
    est = dict(tuning=rem_tune, c3=c3_end, c2=c2_end - c3_end, evaluation=max(0.0, eval_end - c2_end), aggregation=AGG_MIN, writeup=DOCS_MIN)
    all_items = [i for g in groups for i in g["items"]]
    return dict(start=start, end=end, finished=finished, now=now, eta_min=total_min, eta_at=None if finished else now + total_min * 60,
                stage_est_min=est, done_items=sum(1 for i in all_items if i["done"]), total_items=len(all_items), groups=groups,
                note="Estimate from measured run times; assumes no crashes and that Claude is online for the write-up. Stages overlap, so the parts do not add up to the total.")


def clean(o):
    """JSON has no NaN/Infinity: map them to null."""
    if isinstance(o, float) and (o != o or o in (float("inf"), float("-inf"))):
        return None
    if isinstance(o, dict):
        return {k: clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [clean(v) for v in o]
    return o


def state() -> dict:
    now = time.time()
    runs, files = {}, []
    for p in sorted(LOGS.glob("*.log")):
        st = p.stat()
        parsed = parse_log(p)
        active = now - st.st_mtime < 240
        files.append(dict(name=p.name, size=st.st_size, mtime=st.st_mtime, active=active))
        for name, r in parsed["runs"].items():
            ck = ROOT / "runs" / name / "best.pt"
            cks = ck.stat() if ck.exists() else None
            runs[name] = dict(r, log=p.name, active=active and parsed["last"] == name, mtime=st.st_mtime,
                              ckpt=dict(path=f"runs/{name}/best.pt", mb=cks.st_size / 1e6, mtime=cks.st_mtime) if cks else None)
    status = json.loads(sh(["python3", str(ROOT / "scripts/autopilot_status.py"), "--json"]) or "{}")
    res = results()
    return dict(now=now, gpu=gpu(), system=system(), stage=status, runs=runs, results=res, logs=files, plan=plan(res, status),
                done=(LOGS / "AUTOPILOT_DONE").exists(), stuck=(LOGS / "AUTOPILOT_STUCK").exists())


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def send(self, code: int, body: bytes, ctype: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        u = urlparse(self.path)
        if u.path in ("/", "/index.html"):
            return self.send(200, (STATIC / "index.html").read_bytes(), "text/html; charset=utf-8")
        if u.path == "/favicon.ico":
            return self.send(204, b"", "image/x-icon")
        if u.path == "/api/state":
            return self.send(200, json.dumps(clean(state()), allow_nan=False).encode(), "application/json")
        if u.path == "/api/tail":
            q = parse_qs(u.query)
            name = Path(q.get("file", [""])[0]).name  # basename only: no path traversal
            n = min(int(q.get("n", ["200"])[0]), 2000)
            p = LOGS / name
            if not name.endswith(".log") or not p.exists():
                return self.send(404, b"no such log", "text/plain")
            lines = p.read_text(errors="ignore").splitlines()[-n:]
            return self.send(200, "\n".join(lines).encode(), "text/plain; charset=utf-8")
        if u.path == "/api/runlog":
            q = parse_qs(u.query)
            run = q.get("run", [""])[0]
            hit = [f for f in LOGS.glob("*.log") if f"[{run}]" in f.read_text(errors="ignore")] if re.fullmatch(r"[\w.\-]+", run) else []
            if not hit:
                return self.send(404, b"no such run", "text/plain")
            lines = [l for l in hit[0].read_text(errors="ignore").splitlines() if f"[{run}]" in l or l.startswith(run.rsplit("-s", 1)[0])]
            return self.send(200, "\n".join(lines[-600:]).encode(), "text/plain; charset=utf-8")
        self.send(404, b"not found", "text/plain")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8383)
    a = ap.parse_args()
    ThreadingHTTPServer(("0.0.0.0", a.port), H).serve_forever()
