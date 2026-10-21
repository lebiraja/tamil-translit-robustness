from translit import retry
from translit.retry import with_retries


def test_retries_then_succeeds(monkeypatch, tmp_path):
    monkeypatch.setattr(retry, "ROOT", tmp_path)
    n = {"c": 0}

    def flaky():
        n["c"] += 1
        if n["c"] < 3:
            raise RuntimeError("boom")
        return 7

    assert with_retries(flaky, "t", tries=3, wait_s=0) == 7
    assert n["c"] == 3
    assert (tmp_path / "logs/failed_runs.txt").read_text().count(" try ") == 2


def test_gives_up_and_returns_none(monkeypatch, tmp_path):
    monkeypatch.setattr(retry, "ROOT", tmp_path)
    assert with_retries(lambda: 1 / 0, "t", tries=2, wait_s=0) is None
