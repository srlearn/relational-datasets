# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

"""Download Relational Datasets
"""

from io import BytesIO
from io import TextIOWrapper
import json
import pathlib
from urllib.request import urlopen
from zipfile import ZipFile
from typing import Tuple


from ._base import get_data_home
from ._base import RelationalDataset


VERSION_URL = (
    "https://github.com/srlearn/datasets/releases/download/{version}/{archive}.zip"
)
DATASETS = [
    "toy_cancer",
    "toy_father",
    "citeseer",
    "cora",
    "uwcse",
    "webkb",
]
LATEST_VERSION = "v0.0.3"


def latest_version() -> str:
    """Get the latest ``srlearn/datasets`` version from GitHub's REST API."""
    with urlopen(
        "https://api.github.com/repos/srlearn/datasets/releases/latest"
    ) as url:
        api_response = json.loads(url.read().decode("utf-8"))
    return api_response["tag_name"]


def load(
    name: str, version: str = "", fold: int = 1
) -> Tuple[RelationalDataset, RelationalDataset]:
    """Load version of dataset.

    Parameters
    ----------
    name : str
        Dataset name (e.g. ``toy_cancer``)
    version : str
        Dataset version (e.g. `v0.0.3`)
    fold : int
        In datasets with multiple folds, return the fold with this number


    Examples
    --------

    Load version ``v0.0.3`` of the ``toy_cancer`` dataset:

    >>> from relational_datasets import load
    >>> train, test = load("toy_cancer", "v0.0.3")
    >>> train.pos
    ['cancer(alice).', 'cancer(bob).', 'cancer(chuck).', 'cancer(fred).']
    """

    data_location = fetch(name, version)

    # Deserialize the contents
    with ZipFile(data_location) as myzip:

        folds = _n_folds(myzip)

        if folds == 0:
            # This dataset contains no folds.

            with myzip.open(f"{name}/train/train_pos.txt", "r") as _fh:
                train_pos = TextIOWrapper(_fh).read().splitlines()
            with myzip.open(f"{name}/train/train_neg.txt", "r") as _fh:
                train_neg = TextIOWrapper(_fh).read().splitlines()
            with myzip.open(f"{name}/train/train_facts.txt", "r") as _fh:
                train_facts = TextIOWrapper(_fh).read().splitlines()

            with myzip.open(f"{name}/test/test_pos.txt", "r") as _fh:
                test_pos = TextIOWrapper(_fh).read().splitlines()
            with myzip.open(f"{name}/test/test_neg.txt", "r") as _fh:
                test_neg = TextIOWrapper(_fh).read().splitlines()
            with myzip.open(f"{name}/test/test_facts.txt", "r") as _fh:
                test_facts = TextIOWrapper(_fh).read().splitlines()

        elif fold > folds:
            print(fold, folds)
            raise ValueError("Fold does not exist.")

        else:
            with myzip.open(f"{name}/fold{fold}/train/train_pos.txt", "r") as _fh:
                train_pos = TextIOWrapper(_fh).read().splitlines()
            with myzip.open(f"{name}/fold{fold}/train/train_neg.txt", "r") as _fh:
                train_neg = TextIOWrapper(_fh).read().splitlines()
            with myzip.open(f"{name}/fold{fold}/train/train_facts.txt", "r") as _fh:
                train_facts = TextIOWrapper(_fh).read().splitlines()

            with myzip.open(f"{name}/fold{fold}/test/test_pos.txt", "r") as _fh:
                test_pos = TextIOWrapper(_fh).read().splitlines()
            with myzip.open(f"{name}/fold{fold}/test/test_neg.txt", "r") as _fh:
                test_neg = TextIOWrapper(_fh).read().splitlines()
            with myzip.open(f"{name}/fold{fold}/test/test_facts.txt", "r") as _fh:
                test_facts = TextIOWrapper(_fh).read().splitlines()

    return (
        RelationalDataset._make([train_pos, train_neg, train_facts]),
        RelationalDataset._make([test_pos, test_neg, test_facts]),
    )


def fetch(name: str, version: str = "") -> str:
    """Get the file location of a dataset with a name/version. Download if unavailable.
    """

    data_file = pathlib.Path(get_data_home()).joinpath(f"{name}_{version}.zip")
    if data_file.is_file():
        return str(data_file)

    # Else the data needs to be downloaded.

    download_url = _make_data_url(name, version)

    with urlopen(download_url) as url:
        data = BytesIO(url.read())

    with open(data_file, "wb") as _fh:
        _fh.write(data.getbuffer())

    return str(data_file)


def _make_data_url(name: str, version: str = "") -> str:
    """Create a URL for a dataset with ``name`` and ``version``.

    If a ``version`` is not provided, the latest version is returned.
    """

    assert name in DATASETS

    if not version:
        version = LATEST_VERSION
    return VERSION_URL.format(archive=name, version=version)


def _has_folds(zip: ZipFile) -> bool:
    """Does this zipfile contain folds?"""
    file_names = zip.namelist()
    has_folds = any(["fold" in path for path in file_names])
    return has_folds


def _n_folds(zip: ZipFile) -> int:
    """How many folds does this zipfile contain?"""

    if not _has_folds(zip):
        return 0

    numbers = []
    for path in zip.namelist():
        if "fold" in path:
            numbers.append(int(path.split("fold")[1].split("/")[0]))
    return max(numbers)
