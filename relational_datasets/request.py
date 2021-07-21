# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

"""Download and use Relational Datasets

Notes
-----

Portions of this were originally based on how data sets were implemented in the
``imbalanced-learn`` repository.
"""

from typing import List

import json

import pathlib

from urllib.request import urlopen

from zipfile import ZipFile

import logging

from io import BytesIO
from io import TextIOWrapper

from ._base import get_data_home

# TODO(hayesall): zipfile.Path objects are only available in Python 3.8+
# TODO(hayesall): `LATEST_URL` is a valid download option, but I probably
#   should not recommend using it: Once I download the data, there is no other
#   way to know what version it is associated with (unless I maintain that
#   metadata elsewhere).

VERSION_URL = "https://github.com/srlearn/datasets/releases/download/{version}/{archive}.zip"
LATEST_URL = "https://github.com/srlearn/datasets/releases/latest/download/{archive}.zip"
DATASETS = [
    "toy_cancer",
    "toy_father",
    "citeseer",
    "cora",
    "uwcse",
    "webkb",
]


def _get_latest_version_number() -> str:
    """Get the latest ``srlearn/datasets`` version from GitHub's REST API."""
    with urlopen("https://api.github.com/repos/srlearn/datasets/releases/latest") as url:
        api_response = json.loads(url.read().decode('utf-8'))
    return api_response["tag_name"]



def _make_data_url(name: str, version: str = "") -> str:
    """Create a URL for a dataset with ``name`` and ``version``.

    If a ``version`` is not provided, the latest version is returned.
    """

    assert name in DATASETS

    if not version:
        version = _get_latest_version_number()
    return VERSION_URL.format(archive=name, version=version)


def _paths_in_zipfile(name: str, zip: ZipFile) -> List[str]:

    # TODO(hayesall): It feels unnatural to pass ``name`` here.

    file_names = zip.namelist()
    has_folds = any(['fold' in path for path in file_names])

    print(has_folds)


def latest_version() -> str:
    return _get_latest_version_number()

def fetch(name: str, version: str = "") -> List[str]:

    # TODO(hayesall): `mypy` doesn't like the incompatible types used to create
    #   a ZipFile(data) instance. Path vs. IO[bytes] and BinaryIO.

    download_url = _make_data_url(name, version)
    data_file = pathlib.Path(get_data_home()).joinpath(f"{name}_{version}.zip")

    if data_file.is_file():
        # The data exists in the cache.
        data = data_file
    else:
        # The data needs to be downloaded.
        with urlopen(download_url) as url:
            data = BytesIO(url.read())

        # Save a copy of the data to disk
        with open(data_file, "wb") as _fh:
            _fh.write(data.getbuffer())

    # Deserialize the contents
    with ZipFile(data) as myzip:

        _paths_in_zipfile(name, myzip)

        # TODO(hayesall): Does this work on Windows?

        with myzip.open(f"{name}/train/train_pos.txt", "r") as _fh:
            train_pos = TextIOWrapper(_fh).read().splitlines()

        # print(myzip.namelist())

    return train_pos
