"""Batched greedy and beam-search decoding over the shared model interface."""

from __future__ import annotations

import torch

SOS, EOS = 1, 2


def _expand(state: dict[str, torch.Tensor], k: int) -> dict[str, torch.Tensor]:
    return {n: v.repeat_interleave(k, 0) for n, v in state.items()}


@torch.no_grad()
def beam_search(model, src: torch.Tensor, beam: int = 10, max_len: int = 48, n_best: int = 5):
    """Return per-input lists of (token ids, log-prob) sorted best-first (length-normalised ranking off:
    word-level outputs are short, raw log-prob is used, matching common transliteration practice)."""
    model.eval()
    b, dev = src.size(0), src.device
    state = _expand(model.init_state(src), beam)
    tok = torch.full((b * beam,), SOS, dtype=torch.long, device=dev)
    scores = torch.full((b, beam), float("-inf"), device=dev)
    scores[:, 0] = 0.0
    hist = torch.zeros(b * beam, 0, dtype=torch.long, device=dev)
    finished: list[list[tuple[float, list[int]]]] = [[] for _ in range(b)]
    for _ in range(max_len):
        logp, state = model.step(state, tok)  # [B*K, V]
        v = logp.size(-1)
        logp[:, 0] = float("-inf")  # never emit PAD
        logp[:, 1] = float("-inf")  # never emit SOS
        cand = (scores.view(-1, 1) + logp).view(b, beam * v)
        top, idx = cand.topk(beam, -1)
        prev, nxt = idx // v, idx % v
        base = (torch.arange(b, device=dev) * beam).unsqueeze(1)
        sel = (base + prev).view(-1)
        state = {n: x.index_select(0, sel) for n, x in state.items()}
        hist = torch.cat([hist.index_select(0, sel), nxt.view(-1, 1)], 1)
        scores, tok = top.clone(), nxt.view(-1)
        ended = (nxt == EOS) & torch.isfinite(top)
        if ended.any():
            for i, j in ended.nonzero().tolist():
                finished[i].append((top[i, j].item(), hist[i * beam + j, :-1].tolist()))
            scores[ended] = float("-inf")
        done = all(len(f) >= beam for f in finished) or not torch.isfinite(scores).any()
        if done:
            break
    out = []
    for i in range(b):
        fin = sorted(finished[i], key=lambda x: -x[0])[:n_best]
        out.append(fin)
    return out


@torch.no_grad()
def greedy(model, src: torch.Tensor, max_len: int = 48) -> list[list[int]]:
    model.eval()
    state = model.init_state(src)
    tok = torch.full((src.size(0),), SOS, dtype=torch.long, device=src.device)
    outs = torch.zeros(src.size(0), 0, dtype=torch.long, device=src.device)
    alive = torch.ones(src.size(0), dtype=torch.bool, device=src.device)
    for _ in range(max_len):
        logp, state = model.step(state, tok)
        logp[:, 0] = float("-inf")
        logp[:, 1] = float("-inf")
        tok = logp.argmax(-1)
        outs = torch.cat([outs, tok.unsqueeze(1)], 1)
        alive &= tok != EOS
        if not alive.any():
            break
    return outs.tolist()


@torch.no_grad()
def sample(model, src: torch.Tensor, temperature: float = 1.0, max_len: int = 48) -> list[list[int]]:
    """Ancestral sampling (A3 back-transliteration variation)."""
    model.eval()
    state = model.init_state(src)
    tok = torch.full((src.size(0),), SOS, dtype=torch.long, device=src.device)
    outs = torch.zeros(src.size(0), 0, dtype=torch.long, device=src.device)
    alive = torch.ones(src.size(0), dtype=torch.bool, device=src.device)
    for _ in range(max_len):
        logp, state = model.step(state, tok)
        logp[:, 0] = float("-inf")
        logp[:, 1] = float("-inf")
        tok = torch.multinomial(torch.softmax(logp / temperature, -1), 1).squeeze(1)
        outs = torch.cat([outs, tok.unsqueeze(1)], 1)
        alive &= tok != EOS
        if not alive.any():
            break
    return outs.tolist()
