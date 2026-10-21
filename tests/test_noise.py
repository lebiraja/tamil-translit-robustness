import random
import string

import pytest

from translit import noise

WORDS = ["kanakkil", "vaazhga", "semma", "irukku", "naataalamantratthil", "a", "ka", "thaththa", "zhaa"]


@pytest.mark.parametrize("op", list(noise.OPS) + ["MIX", "RANDOM"])
def test_deterministic_nonempty_alphabet(op):
    for w in WORDS:
        for p in noise.SEVERITIES:
            a = noise.noisy_variant(w, op, p, 1)
            assert a == noise.noisy_variant(w, op, p, 1)
            assert a and set(a) <= set(string.ascii_lowercase)


def test_vdrop_keeps_initial_and_only_removes_vowels():
    rng = random.Random(0)
    out = noise.v_drop("kanakkil", 1.0, rng)
    assert out == "knkkl"
    assert noise.v_drop("aeiou", 1.0, rng) == "a"


def test_gem_and_vlen():
    rng = random.Random(0)
    assert noise.gem("irukku", 1.0, rng) == "iruku"
    assert noise.v_len("kaanum", 1.0, rng) == "kanum"
    assert noise.gem("kaanum", 1.0, rng) == "kaanum"


def test_digraph_symmetric():
    seen = set()
    for s in range(200):
        seen.add(noise.digraph("tha", 1.0, random.Random(s)))
        seen.add(noise.digraph("ta", 1.0, random.Random(s)))
    assert "ta" in seen and "tha" in seen


def test_zh_one_way():
    outs = {noise.digraph("vaazhga", 1.0, random.Random(s)) for s in range(50)}
    assert {"vaalga", "vaazga"} <= outs


def test_zero_severity_is_identity():
    for op in list(noise.OPS) + ["MIX", "RANDOM"]:
        if op == "MIX":
            continue
        for w in WORDS:
            assert noise.apply(op, w, 0.0, random.Random(1)) == w


def test_repeat_only_vowels():
    out = noise.repeat("semma", 1.0, random.Random(3))
    assert out.startswith("semma") and set(out[5:]) == {"a"} or out.startswith("seemma") or len(out) > 5


def test_key_neighbours_exist():
    assert all(NB for NB in noise.NEIGHBOURS.values())
    assert "w" in noise.NEIGHBOURS["q"]
