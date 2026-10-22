"""Inference helper: load a trained checkpoint and transliterate words or whole sentences (CPU or GPU)."""

from __future__ import annotations

import re
from pathlib import Path

import torch

from .data import Vocab, collate
from .decode import beam_search
from .models import build

WORD = re.compile(r"[A-Za-z]+")
# Tamil chat words that look like (frequent) English words or are too short to judge: never treated as English.
TAMIL_COLLIDE = set("""da di pa ma la na nu ku ra ya po va ji ne un en ka kaa tha thala oru anna akka dei illa illai enna inga anga
avan ava ivan iva vera sema semma padam ponga vanga romba nalla mattum thaan dhan kitta mela pola mari machan macha bro""".split()) - {"bro"}
SHORT_EN = set("ok hi no is to so me my we he it in on at by of or if as up us an do go be am".split())

try:  # optional dependency; without it nothing is flagged as English
    from wordfreq import zipf_frequency
except ImportError:  # pragma: no cover
    zipf_frequency = None


def is_english(w: str, thr: float = 4.0) -> bool:
    """Heuristic: a frequent English word that is not a known Tamil chat word. Not a language ID model."""
    w = w.lower()
    if zipf_frequency is None or w in TAMIL_COLLIDE:
        return False
    if len(w) <= 2:
        return w in SHORT_EN
    return zipf_frequency(w, "en") >= thr


class Transliterator:
    def __init__(self, ckpt: str | Path, device: str = "cpu"):
        ck = torch.load(ckpt, map_location=device, weights_only=False)
        self.vocab = Vocab(**ck["vocab"])
        self.model = build(ck["arch"], len(self.vocab.src), len(self.vocab.tgt), **ck["kw"]).to(device)
        self.model.load_state_dict(ck["model"])
        self.model.eval()
        self.device, self.arch = device, ck["arch"]
        self._cache: dict[tuple[str, int], list[str]] = {}

    @torch.no_grad()
    def words(self, words: list[str], n_best: int = 5, beam: int = 10) -> list[list[str]]:
        """Top-``n_best`` Tamil candidates for each romanized word (lowercased); cached."""
        todo = sorted({w.lower() for w in words if (w.lower(), n_best) not in self._cache})
        for s in range(0, len(todo), 128):
            chunk = todo[s : s + 128]
            src, _ = collate([(self.vocab.enc_src(w), [1, 2]) for w in chunk])
            for w, fin in zip(chunk, beam_search(self.model, src.to(self.device), beam, n_best=n_best), strict=True):
                out: list[str] = []
                for _, ids in fin:
                    t = self.vocab.dec_tgt(ids)
                    if t and t not in out:
                        out.append(t)
                self._cache[(w, n_best)] = out or [w]
        return [self._cache[(w.lower(), n_best)] for w in words]

    def sentence(self, text: str, n_best: int = 5) -> list[dict]:
        """Split text into Latin words (converted) and everything else (kept as is)."""
        parts, pos, ws = [], 0, list(WORD.finditer(text))
        cands = self.words([m.group() for m in ws], n_best) if ws else []
        for m, c in zip(ws, cands, strict=True):
            if m.start() > pos:
                parts.append({"literal": text[pos : m.start()]})
            parts.append({"src": m.group(), "cands": c, "english": is_english(m.group())})
            pos = m.end()
        if pos < len(text):
            parts.append({"literal": text[pos:]})
        return parts
