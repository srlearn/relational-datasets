# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

from relational_datasets import load


def test_fetch_toy_cancer_v0_0_3():
    train, _ = load("toy_cancer", "v0.0.3")
    assert train.pos == [
        "cancer(alice).",
        "cancer(bob).",
        "cancer(chuck).",
        "cancer(fred).",
    ]


def test_fetch_webkb_v_0_0_3_fold_2():
    train, _ = load("webkb", "v0.0.3")
    assert len(train.pos) == 107
    assert len(train.neg) == 444
    assert len(train.facts) == 1439
