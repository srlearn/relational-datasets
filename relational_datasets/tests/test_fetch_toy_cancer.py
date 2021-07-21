# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

from relational_datasets import fetch


def test_fetch_toy_cancer_v0_0_3():
    data = fetch("toy_cancer", "v0.0.3")
    assert data == ['cancer(alice).', 'cancer(bob).', 'cancer(chuck).', 'cancer(fred).']
