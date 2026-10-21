"""Run a model over (input, references) lists and score it."""

from __future__ import annotations

import torch

from .data import Vocab, collate
from .decode import beam_search, greedy
from .metrics import score


def _batches(inputs: list[str], vocab: Vocab, bs: int, device: str):
    order = sorted(range(len(inputs)), key=lambda i: len(inputs[i]))
    for s in range(0, len(order), bs):
        idx = order[s : s + bs]
        src, _ = collate([(vocab.enc_src(inputs[i]), [1, 2]) for i in idx])
        yield idx, src.to(device)


def translate(model, vocab: Vocab, inputs: list[str], beam: int = 10, n_best: int = 5, bs: int = 256,
              device: str = "cuda") -> list[list[str]]:
    out: list[list[str]] = [[] for _ in inputs]
    for idx, src in _batches(inputs, vocab, bs, device):
        if beam <= 1:
            for i, ids in zip(idx, greedy(model, src), strict=True):
                out[i] = [vocab.dec_tgt(ids)]
        else:
            for i, fin in zip(idx, beam_search(model, src, beam, n_best=n_best), strict=True):
                hyps: list[str] = []
                for _, ids in fin:
                    s = vocab.dec_tgt(ids)
                    if s not in hyps:
                        hyps.append(s)
                out[i] = hyps or [""]
    return out


def evaluate(model, vocab: Vocab, inputs: list[str], refs: list[list[str]], beam: int = 10, device: str = "cuda"):
    """Return (metrics dict, n-best lists) for parallel ``inputs`` / ``refs``."""
    nbest = translate(model, vocab, inputs, beam=beam, device=device)
    return score(nbest, refs), nbest
