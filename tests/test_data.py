import pytest

from translit import data as D

pytestmark = pytest.mark.skipif(not (D.DAKSHINA / "ta.translit.sampled.train.tsv").exists(), reason="Dakshina not fetched")


def test_counts_match_documented():
    assert [len(D.load_lexicon(s)) for s in D.SPLITS] == [68218, 6827, 6864]
    assert [len({n for n, _, _ in D.load_lexicon(s)}) for s in D.SPLITS] == [25000, 2500, 2500]


def test_splits_word_disjoint():
    w = {s: {n for n, _, _ in D.load_lexicon(s)} for s in D.SPLITS}
    assert not (w["train"] & w["dev"]) and not (w["train"] & w["test"]) and not (w["dev"] & w["test"])


def test_vocab_roundtrip():
    tp = D.pairs(D.load_lexicon("train"))
    v = D.Vocab.build(tp)
    r, n = tp[0]
    assert v.dec_tgt(v.enc_tgt(n)[1:]) == n
    assert v.enc_src(r)[-1] == 2
