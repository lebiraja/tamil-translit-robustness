from translit.metrics import edit_distance, score


def test_edit_distance():
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("", "abc") == 3
    assert edit_distance("வணக்கம்", "வணக்கம்") == 0


def test_score_hand_computed():
    nbest = [["abc", "abd"], ["xyz", "xyy"], ["q", "r"]]
    refs = [["abc"], ["xyy"], ["zz", "r"]]
    m = score(nbest, refs, ks=(1, 2))
    assert m["top1"] == pytest_approx(100 / 3)
    assert m["top2"] == pytest_approx(100.0)
    assert m["mrr"] == pytest_approx((1 + 0.5 + 0.5) / 3)
    # edits: 0 + 1 (xyz vs xyy) + 1 (q vs r) over ref lengths 3 + 3 + 1
    assert m["cer"] == pytest_approx(100 * 2 / 7)


def pytest_approx(x):
    import pytest

    return pytest.approx(x)
