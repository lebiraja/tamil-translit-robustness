"""Tamil-specific noise operators for romanized input (C1) and augmentation (C2).

Every operator maps a lowercase Latin word to a noisy Latin word, is deterministic
given a ``random.Random``, never returns an empty string and only emits a-z.
Severity ``p`` is the per-eligible-position application probability, except REPEAT
(per word) and KEY (per letter, scaled by KEY_SCALE so p=0.5 stays readable).
The realised edit rate per operator and severity is measured and logged by
``scripts/make_noisy_tests.py``; report that, not the nominal ``p``.
"""

from __future__ import annotations

import random
from collections.abc import Callable

VOWELS = set("aeiou")
SEVERITIES = (0.1, 0.2, 0.3, 0.5)
KEY_SCALE = 0.25

_ROWS = ("qwertyuiop", "asdfghjkl", "zxcvbnm")
_POS = {c: (r, i + (0.0, 0.25, 0.75)[r]) for r, row in enumerate(_ROWS) for i, c in enumerate(row)}
NEIGHBOURS: dict[str, list[str]] = {
    c: sorted(
        d for d, (r2, x2) in _POS.items()
        if d != c and abs(r2 - r) <= 1 and abs(x2 - x) <= 1.0 and (r2, x2) != (r, x)
    )
    for c, (r, x) in _POS.items()
}

# Symmetric digraph swaps. zh is one-way: typists write l or z for zh, not the reverse.
_SWAP_PAIRS = [("th", "t"), ("dh", "d"), ("sh", "s"), ("ch", "c"), ("ch", "s")]
_ONE_WAY = [("zh", "l"), ("zh", "z")]


def _nonempty(new: str, old: str) -> str:
    return new if new else old


def v_drop(word: str, p: float, rng: random.Random) -> str:
    """Delete non-initial vowels (kanakkil -> kankl)."""
    out = [c for i, c in enumerate(word) if not (i > 0 and c in VOWELS and rng.random() < p)]
    return _nonempty("".join(out), word)


def v_len(word: str, p: float, rng: random.Random) -> str:
    """Collapse doubled vowels (aa->a, ee->e, ii->i, oo->o, uu->u); also ee->i, oo->u half the time."""
    out: list[str] = []
    i = 0
    while i < len(word):
        c = word[i]
        if c in VOWELS and i + 1 < len(word) and word[i + 1] == c and rng.random() < p:
            if c == "e" and rng.random() < 0.3:
                c = "i"
            elif c == "o" and rng.random() < 0.3:
                c = "u"
            out.append(c)
            i += 2
        else:
            out.append(c)
            i += 1
    return _nonempty("".join(out), word)


def gem(word: str, p: float, rng: random.Random) -> str:
    """Collapse doubled consonants (irukku -> iruku)."""
    out: list[str] = []
    i = 0
    while i < len(word):
        c = word[i]
        if c not in VOWELS and i + 1 < len(word) and word[i + 1] == c and rng.random() < p:
            out.append(c)
            i += 2
        else:
            out.append(c)
            i += 1
    return _nonempty("".join(out), word)


def digraph(word: str, p: float, rng: random.Random) -> str:
    """Symmetric digraph confusions (th<->t, dh<->d, sh<->s, ch<->c/s) plus zh->l/z."""
    out: list[str] = []
    i = 0
    while i < len(word):
        two, one = word[i : i + 2], word[i]
        if two in {"zh", "th", "dh", "sh", "ch"}:
            opts = [b for a, b in _SWAP_PAIRS + _ONE_WAY if a == two]
            out.append(rng.choice(opts) if rng.random() < p else two)
            i += 2
            continue
        if one in {"t", "d", "s", "c"} and rng.random() < p:
            opts = [a for a, b in _SWAP_PAIRS if b == one] or [one]
            out.append(rng.choice(opts))
        else:
            out.append(one)
        i += 1
    return _nonempty("".join(out), word)


def key(word: str, p: float, rng: random.Random) -> str:
    """Adjacent-key QWERTY substitution."""
    q = p * KEY_SCALE
    out = [rng.choice(NEIGHBOURS[c]) if c in NEIGHBOURS and rng.random() < q else c for c in word]
    return "".join(out)


def repeat(word: str, p: float, rng: random.Random) -> str:
    """With probability p stretch one vowel (preferring the last) by 1-3 extra copies (semma -> semmaaa)."""
    pos = [i for i, c in enumerate(word) if c in VOWELS]
    if not pos or rng.random() >= p:
        return word
    i = pos[-1] if rng.random() < 0.7 else rng.choice(pos)
    return word[: i + 1] + word[i] * rng.randint(1, 3) + word[i + 1 :]


def random_char(word: str, p: float, rng: random.Random) -> str:
    """Baseline A1 noise: per-character deletion, insertion, substitution, adjacent swap, equal shares."""
    chars = list(word)
    out: list[str] = []
    i = 0
    letters = "abcdefghijklmnopqrstuvwxyz"
    while i < len(chars):
        if rng.random() >= p:
            out.append(chars[i])
            i += 1
            continue
        kind = rng.choice(("del", "ins", "sub", "swap"))
        if kind == "del":
            pass
        elif kind == "ins":
            out += [chars[i], rng.choice(letters)]
        elif kind == "sub":
            out.append(rng.choice(letters))
        elif i + 1 < len(chars):
            out += [chars[i + 1], chars[i]]
            i += 1
        else:
            out.append(chars[i])
        i += 1
    return _nonempty("".join(out), word)


OPS: dict[str, Callable[[str, float, random.Random], str]] = {
    "V-DROP": v_drop,
    "V-LEN": v_len,
    "GEM": gem,
    "DIGRAPH": digraph,
    "KEY": key,
    "REPEAT": repeat,
}
_MIX_ORDER = ("V-LEN", "GEM", "DIGRAPH", "V-DROP", "KEY", "REPEAT")


def mix(word: str, p: float, rng: random.Random, ops: tuple[str, ...] = _MIX_ORDER) -> str:
    """Random combination: each operator is included with probability 0.5 (at least one is applied)."""
    chosen = [o for o in ops if rng.random() < 0.5] or [rng.choice(ops)]
    for name in ops:
        if name in chosen:
            word = OPS[name](word, p, rng)
    return word


def apply(name: str, word: str, p: float, rng: random.Random, ops: tuple[str, ...] | None = None) -> str:
    """Apply a named operator (``MIX`` and ``RANDOM`` included)."""
    if name == "MIX":
        return mix(word, p, rng, ops or _MIX_ORDER)
    if name == "RANDOM":
        return random_char(word, p, rng)
    return OPS[name](word, p, rng)


def noisy_variant(word: str, name: str, p: float, seed: int, ops: tuple[str, ...] | None = None) -> str:
    """Deterministic noisy form of ``word``; the seed is derived from (seed, name, p, word)."""
    import hashlib

    h = hashlib.blake2b(f"{seed}|{name}|{p}|{word}".encode(), digest_size=8).digest()
    return apply(name, word, p, random.Random(int.from_bytes(h, "big")), ops)
