"""Character-level seq2seq models: BiLSTM + Luong attention and a small pre-LN Transformer.

Shared interface (used by teacher-forced training and by beam search):
  forward(src, tgt_in) -> logits [B, T, V]
  init_state(src) -> dict of tensors, every value batch-first
  step(state, tok[B]) -> (log_probs [B, V], new_state)
Token ids: PAD=0, SOS=1, EOS=2, UNK=3.
"""

from __future__ import annotations

import math

import torch
import torch.nn as nn
import torch.nn.functional as F

State = dict[str, torch.Tensor]


class BiLSTMAttn(nn.Module):
    def __init__(self, n_src: int, n_tgt: int, emb: int = 128, hidden: int = 256, layers: int = 2, dropout: float = 0.2):
        super().__init__()
        self.hidden, self.layers = hidden, layers
        self.src_emb = nn.Embedding(n_src, emb, padding_idx=0)
        self.tgt_emb = nn.Embedding(n_tgt, emb, padding_idx=0)
        self.enc = nn.LSTM(emb, hidden, layers, batch_first=True, bidirectional=True, dropout=dropout if layers > 1 else 0.0)
        self.bridge_h = nn.Linear(2 * hidden, hidden)
        self.bridge_c = nn.Linear(2 * hidden, hidden)
        self.dec = nn.LSTM(emb, hidden, layers, batch_first=True, dropout=dropout if layers > 1 else 0.0)
        self.att_q = nn.Linear(hidden, 2 * hidden, bias=False)  # Luong "general"
        self.comb = nn.Linear(3 * hidden, hidden)
        self.out = nn.Linear(hidden, n_tgt)
        self.drop = nn.Dropout(dropout)

    def _encode(self, src: torch.Tensor):
        mask = src != 0
        lens = mask.sum(1).cpu()
        x = self.drop(self.src_emb(src))
        packed = nn.utils.rnn.pack_padded_sequence(x, lens, batch_first=True, enforce_sorted=False)
        mem, (h, c) = self.enc(packed)
        mem, _ = nn.utils.rnn.pad_packed_sequence(mem, batch_first=True, total_length=src.size(1))
        # last layer forward/backward final states -> decoder init for every layer
        hc = torch.cat([h[-2], h[-1]], -1)
        cc = torch.cat([c[-2], c[-1]], -1)
        h0 = torch.tanh(self.bridge_h(hc)).unsqueeze(0).repeat(self.layers, 1, 1)
        c0 = torch.tanh(self.bridge_c(cc)).unsqueeze(0).repeat(self.layers, 1, 1)
        return mem, mask, h0.contiguous(), c0.contiguous()

    def _attend(self, dec_out: torch.Tensor, mem: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
        scores = torch.bmm(self.att_q(dec_out), mem.transpose(1, 2))  # [B, T, S]
        scores = scores.masked_fill(~mask.unsqueeze(1), float("-inf"))
        ctx = torch.bmm(F.softmax(scores, -1), mem)
        return self.out(self.drop(torch.tanh(self.comb(torch.cat([dec_out, ctx], -1)))))

    def forward(self, src: torch.Tensor, tgt_in: torch.Tensor) -> torch.Tensor:
        mem, mask, h0, c0 = self._encode(src)
        dec_out, _ = self.dec(self.drop(self.tgt_emb(tgt_in)), (h0, c0))
        return self._attend(dec_out, mem, mask)

    def init_state(self, src: torch.Tensor) -> State:
        mem, mask, h0, c0 = self._encode(src)
        return {"mem": mem, "mask": mask, "h": h0.transpose(0, 1).contiguous(), "c": c0.transpose(0, 1).contiguous()}

    def step(self, state: State, tok: torch.Tensor):
        h, c = state["h"].transpose(0, 1).contiguous(), state["c"].transpose(0, 1).contiguous()
        out, (h, c) = self.dec(self.tgt_emb(tok).unsqueeze(1), (h, c))
        logits = self._attend(out, state["mem"], state["mask"]).squeeze(1)
        new = dict(state, h=h.transpose(0, 1).contiguous(), c=c.transpose(0, 1).contiguous())
        return F.log_softmax(logits, -1), new


class TransformerS2S(nn.Module):
    def __init__(self, n_src: int, n_tgt: int, d_model: int = 192, heads: int = 4, enc_layers: int = 3,
                 dec_layers: int = 3, ff: int = 512, dropout: float = 0.1, max_len: int = 64):
        super().__init__()
        self.d = d_model
        self.src_emb = nn.Embedding(n_src, d_model, padding_idx=0)
        self.tgt_emb = nn.Embedding(n_tgt, d_model, padding_idx=0)
        self.pos = nn.Embedding(max_len, d_model)
        self.tr = nn.Transformer(d_model, heads, enc_layers, dec_layers, ff, dropout, batch_first=True, norm_first=True)
        self.out = nn.Linear(d_model, n_tgt)
        self.drop = nn.Dropout(dropout)

    def _embed(self, emb: nn.Embedding, x: torch.Tensor) -> torch.Tensor:
        p = torch.arange(x.size(1), device=x.device)
        return self.drop(emb(x) * math.sqrt(self.d) + self.pos(p))

    def _memory(self, src: torch.Tensor):
        pad = src == 0
        return self.tr.encoder(self._embed(self.src_emb, src), src_key_padding_mask=pad), pad

    def _decode(self, tgt_in: torch.Tensor, mem: torch.Tensor, pad: torch.Tensor) -> torch.Tensor:
        t = tgt_in.size(1)
        causal = torch.triu(torch.ones(t, t, dtype=torch.bool, device=tgt_in.device), 1)
        dec = self.tr.decoder(self._embed(self.tgt_emb, tgt_in), mem, tgt_mask=causal, tgt_key_padding_mask=tgt_in == 0,
                              memory_key_padding_mask=pad)
        return self.out(dec)

    def forward(self, src: torch.Tensor, tgt_in: torch.Tensor) -> torch.Tensor:
        mem, pad = self._memory(src)
        return self._decode(tgt_in, mem, pad)

    def init_state(self, src: torch.Tensor) -> State:
        mem, pad = self._memory(src)
        return {"mem": mem, "pad": pad, "prefix": torch.full((src.size(0), 0), 0, dtype=torch.long, device=src.device)}

    def step(self, state: State, tok: torch.Tensor):
        prefix = torch.cat([state["prefix"], tok.unsqueeze(1)], 1)
        logits = self._decode(prefix, state["mem"], state["pad"])[:, -1]
        return F.log_softmax(logits, -1), dict(state, prefix=prefix)


def n_params(m: nn.Module) -> int:
    return sum(p.numel() for p in m.parameters() if p.requires_grad)


def build(arch: str, n_src: int, n_tgt: int, **kw) -> nn.Module:
    if arch == "lstm":
        return BiLSTMAttn(n_src, n_tgt, **kw)
    if arch == "transformer":
        return TransformerS2S(n_src, n_tgt, **kw)
    raise ValueError(arch)


def config_for_budget(arch: str, target: int, n_src: int, n_tgt: int) -> dict:
    """Pick width so the model has ~``target`` parameters (depth fixed per architecture)."""
    best, best_gap = None, 1 << 60
    if arch == "lstm":
        for hidden in range(32, 1025, 16):
            kw = {"emb": max(32, hidden // 2), "hidden": hidden, "layers": 2}
            gap = abs(n_params(build(arch, n_src, n_tgt, **kw)) - target)
            if gap < best_gap:
                best, best_gap = kw, gap
    else:
        for d in range(32, 769, 32):
            kw = {"d_model": d, "heads": 4 if d % 4 == 0 else 2, "enc_layers": 3, "dec_layers": 3, "ff": 4 * d}
            if d % kw["heads"]:
                continue
            gap = abs(n_params(build(arch, n_src, n_tgt, **kw)) - target)
            if gap < best_gap:
                best, best_gap = kw, gap
    assert best is not None
    return best
