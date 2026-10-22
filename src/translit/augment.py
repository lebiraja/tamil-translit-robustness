"""Training-time augmentation policies (C2). Noise is re-sampled every epoch from a per-epoch seed."""

from __future__ import annotations

import random
from dataclasses import dataclass, field

from . import noise

PHON_OPS = ("V-DROP", "V-LEN", "GEM", "DIGRAPH")
ALL_OPS = PHON_OPS + ("KEY", "REPEAT")
TRAIN_SEVERITIES = (0.1, 0.2, 0.3, 0.5)


@dataclass
class Policy:
    """clean_frac: share of items left clean. kind: none | random | phon | all (A0, A1, A2, all six operators). held_out removes operators."""

    kind: str = "none"
    clean_frac: float = 0.4
    held_out: tuple[str, ...] = ()
    ops: tuple[str, ...] = field(init=False, default=())

    def __post_init__(self) -> None:
        self.ops = tuple(o for o in (ALL_OPS if self.kind == "all" else PHON_OPS) if o not in self.held_out)

    def noisy(self, roman: str, rng: random.Random) -> str:
        if self.kind == "none" or rng.random() < self.clean_frac:
            return roman
        p = rng.choice(TRAIN_SEVERITIES)
        if self.kind == "random":
            return noise.random_char(roman, p / 3, rng)  # per-char rate lowered: A1 edits are not word-aligned
        return noise.apply("MIX", roman, p, rng, self.ops)
