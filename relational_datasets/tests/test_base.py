# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

from os.path import expanduser
from os.path import join
from relational_datasets import get_data_home


def test_default_data_home():
    dir = get_data_home()
    assert dir == expanduser(join("~", "relational_datasets"))
