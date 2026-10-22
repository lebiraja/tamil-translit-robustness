"""Tanglish -> Tamil typing demo. Run: python app/server.py [--ckpt models/v1-a4-transformer-3m.pt] [--port 8000]"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, Response
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from translit.infer import Transliterator  # noqa: E402

app = FastAPI(title="Tanglish to Tamil")
T: Transliterator | None = None
INFO = {"name": "v1 · A4 Transformer 3M", "dev_cer": 8.47, "test_cer": 9.02, "note": "Tamil-style noise + back-transliteration pairs"}


class Req(BaseModel):
    text: str = Field(max_length=2000)
    n_best: int = Field(default=5, ge=1, le=10)


@app.post("/api/transliterate")
def transliterate(r: Req) -> dict:
    t0 = time.perf_counter()
    assert T is not None
    return {"parts": T.sentence(r.text, r.n_best), "ms": round(1000 * (time.perf_counter() - t0), 1)}


@app.get("/api/info")
def info() -> dict:
    return INFO


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    return Response(status_code=204)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(ROOT / "app/static/index.html")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=str(ROOT / "models/v1-a4-transformer-3m.pt"))
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--host", default="127.0.0.1")
    a = ap.parse_args()
    T = Transliterator(a.ckpt)
    uvicorn.run(app, host=a.host, port=a.port, log_level="warning")
