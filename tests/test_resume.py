"""A run interrupted after 2 epochs and resumed must reproduce an uninterrupted 4-epoch run (CPU, tiny model)."""

import pytest
import torch

from translit.train import Config, run

KW = dict(arch="lstm", model_kw={"emb": 16, "hidden": 32, "layers": 1}, batch_size=512, patience=99, noisy_suite=None,
          independent_suite=None, eval_test=False, beam=1, seed=3)


def test_resume_matches_uninterrupted(tmp_path, monkeypatch):
    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)  # keep the test off the GPU used by real jobs
    torch.set_num_threads(2)
    d = lambda n: dict(out_dir=str(tmp_path / n / "res"), ckpt_dir=str(tmp_path / n / "ck"))  # noqa: E731
    full = run(Config(name="full", epochs=4, **KW, **d("a")))
    run(Config(name="part", epochs=2, **KW, **d("b")))
    resumed = run(Config(name="part", epochs=4, **KW, **d("b")))
    a = [h["train_loss"] for h in full["history"]]
    b = [h["train_loss"] for h in resumed["history"]]
    assert len(b) == 4
    assert b == pytest.approx(a, rel=1e-6)
    assert resumed["dev"]["cer"] == pytest.approx(full["dev"]["cer"], rel=1e-6)
