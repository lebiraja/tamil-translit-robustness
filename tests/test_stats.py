"""Hand-computed checks for src/translit/stats.py."""

import numpy as np
import pytest

from translit.stats import cohens_d, corpus_cer, dunn, holm, kruskal, paired_bootstrap


def test_corpus_cer():
    assert corpus_cer(np.array([1, 2]), np.array([4, 6])) == pytest.approx(30.0)


def test_bootstrap_identical_is_null():
    e, ln = np.array([1, 0, 2, 1]), np.array([5, 4, 6, 5])
    r = paired_bootstrap(e, e, ln, n=500)
    assert r["diff_cer"] == 0 and r["ci95"] == [0.0, 0.0] and r["p"] == 1.0


def test_bootstrap_clear_difference():
    ln = np.full(200, 5)
    r = paired_bootstrap(np.ones(200), np.zeros(200), ln, n=2000)
    assert r["diff_cer"] == pytest.approx(20.0) and r["p"] == 0.0 and r["ci95"][0] > 0


def test_bootstrap_rejects_misaligned():
    with pytest.raises(ValueError):
        paired_bootstrap(np.ones(3), np.ones(4), np.ones(3))


def test_holm():
    # sorted 0.01*3=0.03, 0.03*2=0.06, 0.04*1=0.04 -> monotone 0.06
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])


def test_dunn_two_groups():
    # ranks 1,2 | 3,4; N=4; se = sqrt(4*5/12 * (1/2+1/2)) = 1.29099; z = -2/1.29099 = -1.5492; p = 0.1213
    (r,) = dunn({"a": [1, 2], "b": [3, 4]})
    assert r["z"] == pytest.approx(-1.5492, abs=1e-4)
    assert r["p"] == pytest.approx(0.1213, abs=1e-4)
    assert r["p_holm"] == pytest.approx(r["p"])


def test_kruskal_eta2():
    r = kruskal({"a": [1, 2, 3], "b": [4, 5, 6]})
    # H = 12/(6*7) * (6^2/3 + 15^2/3) - 3*7 = 3.857; eta2 = (H - 1) / 4
    assert r["H"] == pytest.approx(3.857, abs=1e-3)
    assert r["eta2"] == pytest.approx((r["H"] - 1) / 4)


def test_cohens_d():
    # means 2 and 5, both sd 1 -> d = -3
    assert cohens_d([1, 2, 3], [4, 5, 6]) == pytest.approx(-3.0)
