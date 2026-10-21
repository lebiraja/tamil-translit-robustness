"""Loaders, vocabulary and batching for word-level Latin -> Tamil transliteration."""

from __future__ import annotations

import random
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import torch
from torch.utils.data import Dataset

PAD, SOS, EOS, UNK = "<pad>", "<s>", "</s>", "<unk>"
ROOT = Path(__file__).resolve().parents[2]
DAKSHINA = ROOT / "data" / "dakshina-ta"
SPLITS = ("train", "dev", "test")


def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def norm_roman(s: str) -> str:
    return s.strip().lower()


def load_lexicon(split: str, root: Path = DAKSHINA) -> list[tuple[str, str, int]]:
    """Return (native, roman, attestation_count) rows from the Dakshina lexicon."""
    rows = []
    for line in (root / f"ta.translit.sampled.{split}.tsv").read_text(encoding="utf-8").splitlines():
        native, roman, *rest = line.split("\t")
        rows.append((nfc(native), norm_roman(roman), int(rest[0]) if rest else 1))
    return rows


def pairs(rows: list[tuple[str, str, int]]) -> list[tuple[str, str]]:
    """Unique (roman, native) training pairs."""
    return sorted({(r, n) for n, r, _ in rows})


def reference_table(rows: list[tuple[str, str, int]]) -> dict[str, list[str]]:
    """roman -> sorted list of all attested native forms (multi-reference evaluation)."""
    t: dict[str, set[str]] = defaultdict(set)
    for n, r, _ in rows:
        t[r].add(n)
    return {r: sorted(v) for r, v in t.items()}


@dataclass
class Vocab:
    src: list[str]
    tgt: list[str]

    def __post_init__(self) -> None:
        self.s2i = {c: i for i, c in enumerate(self.src)}
        self.t2i = {c: i for i, c in enumerate(self.tgt)}

    @classmethod
    def build(cls, train_pairs: list[tuple[str, str]]) -> Vocab:
        """Vocabulary from training data only; PAD=0, SOS=1, EOS=2, UNK=3."""
        sp, tp = [PAD, SOS, EOS, UNK], [PAD, SOS, EOS, UNK]
        sp += sorted({c for r, _ in train_pairs for c in r} | set("abcdefghijklmnopqrstuvwxyz"))
        tp += sorted({c for _, n in train_pairs for c in n})
        return cls(sp, tp)

    def enc_src(self, s: str) -> list[int]:
        return [self.s2i.get(c, 3) for c in s] + [2]

    def enc_tgt(self, s: str) -> list[int]:
        return [1] + [self.t2i.get(c, 3) for c in s] + [2]

    def dec_tgt(self, ids: list[int]) -> str:
        out = []
        for i in ids:
            if i == 2:
                break
            if i > 3:
                out.append(self.tgt[i])
        return "".join(out)

    def to_json(self) -> dict[str, list[str]]:
        return {"src": self.src, "tgt": self.tgt}


class PairDataset(Dataset):
    """Pairs; optionally re-noises the source every access (A1/A2 online augmentation)."""

    def __init__(self, items: list[tuple[str, str]], vocab: Vocab):
        self.items, self.vocab = items, vocab

    def __len__(self) -> int:
        return len(self.items)

    def __getitem__(self, i: int) -> tuple[list[int], list[int]]:
        r, n = self.items[i]
        return self.vocab.enc_src(r), self.vocab.enc_tgt(n)


def collate(batch: list[tuple[list[int], list[int]]]) -> tuple[torch.Tensor, torch.Tensor]:
    sl, tl = max(len(s) for s, _ in batch), max(len(t) for _, t in batch)
    src = torch.zeros(len(batch), sl, dtype=torch.long)
    tgt = torch.zeros(len(batch), tl, dtype=torch.long)
    for i, (s, t) in enumerate(batch):
        src[i, : len(s)] = torch.tensor(s)
        tgt[i, : len(t)] = torch.tensor(t)
    return src, tgt


def seeded_shuffle(items: list, seed: int) -> list:
    out = list(items)
    random.Random(seed).shuffle(out)
    return out
