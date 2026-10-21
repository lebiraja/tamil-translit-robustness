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


def state() -> dict:
    now = time.time()
    runs, files = {}, []
    for p in sorted(LOGS.glob("*.log")):
        st = p.stat()
        parsed = parse_log(p)
        active = now - st.st_mtime < 240
        files.append(dict(name=p.name, size=st.st_size, mtime=st.st_mtime, active=active))
        for name, r in parsed["runs"].items():
            runs[name] = dict(r, log=p.name, active=active and parsed["last"] == name, mtime=st.st_mtime)
    status = json.loads(sh(["python3", str(ROOT / "scripts/autopilot_status.py"), "--json"]) or "{}")
    return dict(now=now, gpu=gpu(), system=system(), stage=status, runs=runs, results=results(), logs=files,
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
        if u.path == "/api/state":
            return self.send(200, json.dumps(state()).encode(), "application/json")
        if u.path == "/api/tail":
            q = parse_qs(u.query)
            name = Path(q.get("file", [""])[0]).name  # basename only: no path traversal
            n = min(int(q.get("n", ["200"])[0]), 2000)
            p = LOGS / name
            if not name.endswith(".log") or not p.exists():
                return self.send(404, b"no such log", "text/plain")
            lines = p.read_text(errors="ignore").splitlines()[-n:]
            return self.send(200, "\n".join(lines).encode(), "text/plain; charset=utf-8")
        self.send(404, b"not found", "text/plain")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8383)
    a = ap.parse_args()
    ThreadingHTTPServer(("0.0.0.0", a.port), H).serve_forever()
