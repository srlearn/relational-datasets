# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

"""Request copies of relational datasets.
"""

# TODO(hayesall): Modes. Where do I put them, how do I store them?
#   A more-general "schema" would be helpful. Plus it would probably be
#   cleaner if I separated advice about structure, types, and search procedures.

# TODO(hayesall): `load` could be made iterable with a generator expression.
#   Possibly useful for iterating over all folds, e.g. for cross validation.

# TODO(hayesall): It doesn't make sense to allow a `data_home` parameter
#   when a user cannot modify the parameter in the `_make_file_path`
#   function.

from io import BytesIO
from io import TextIOWrapper
import json
import logging
import pathlib
from urllib.request import urlopen
from zipfile import ZipFile
from typing import Tuple
from typing import Optional


from ._base import get_data_home
from .types import RelationalDataset


VERSION_URL = (
    "https://github.com/srlearn/datasets/releases/download/{version}/{archive}_{version}.zip"
)
OLD_VERSION_URL = (
    # TODO(hayesall): Used in v0.0.2 and v0.0.3, remove in the beta release.
    "https://github.com/srlearn/datasets/releases/download/{version}/{archive}.zip"
)
DATASETS = [
    "toy_cancer",
    "toy_father",
    "citeseer",
    "cora",
    "uwcse",
    "webkb",
    "financial_nlp_small",
    "nell_sports",
    "icml",
    "boston_housing",
]
LATEST_VERSION = "v0.0.4"


def latest_version() -> str:
    """Get the latest ``srlearn/datasets`` version from GitHub's REST API.

    !!! danger end
        GitHub's REST API is limited to 60 requests per hour when an OAuth
        token is not passed. This function is included for convenience, but
        should only be used interactively.

        Usually you'll be better looking at the latest version from your browser,
        see the [Releases Page](https://github.com/srlearn/datasets/tags).

        Read more on the
        [GitHub REST API Authentication](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#authentication).

    Returns:
        The latest version of datasets stored in the
        [`srlearn/datasets`](https://github.com/srlearn/datasets/) repository.

    Examples:

    ```python
    from relational_datasets.request import latest_version
    latest_version()
    # 'v0.0.3'
    ```
    """

    with urlopen(
        "https://api.github.com/repos/srlearn/datasets/releases/latest"
    ) as url:
        api_response = json.loads(url.read().decode("utf-8"))
    return api_response["tag_name"]


def deserialize_zipfile(
    data_location: str, name: str, *, fold: int = 1
) -> Tuple[RelationalDataset, RelationalDataset]:
    """Deserialize a zipfile, returning train and test sets.

    !!! warning end
        This method is presented here to illustrate how data are unpacked from
        zip archives. The user is responsible for the structure of custom archives.

        The [`srlearn/datasets`](https://github.com/srlearn/datasets/tree/main/srlearn)
        repository defines the assumptions for how datasets are stored.

        Structure generally falls into two categories, where `{{ name }}`
        represents the dataset (e.g. `cora`, `toy_cancer`):

        ```
        {{ name }}
        ├── README.md
        └── {{ name }}
            ├─── background.txt
            ├─── train ─── train_pos.txt, train_neg.txt, train_facts.txt
            └─── test ──── test_pos.txt, test_neg.txt, test_facts.txt
        ```

        ... or:

        ```
        {{ name }}
        ├── README.md
        └── {{ name }}
            ├─── background.txt
            ├─── fold1
            │      ├─── train ─── train_pos.txt, train_neg.txt, train_facts.txt
            │      └─── test ──── test_pos.txt, test_neg.txt, test_facts.txt
            ├─── fold2
            .
            .
        ```

    Arguments:
        data_location: Location of a zipfile.
        name: Name of the dataset.
        fold: In datasets with multiple folds, return this fold. This value is
            ignored if the data is not split into multiple folds.

    Returns:
        Tuple of training and test sets.

    Examples:

    This loads fold-2 of cora-v0.0.3 using an absolute path to the dataset,
    assuming that it is already downloaded:

    ```python
    from relational_datasets.request import deserialize_zipfile

    train, test = deserialize_zipfile(
        '/home/user/relational_datasets/cora_v0.0.3.zip',
        'cora',
        fold=2,
    )
    ```

    This can also load from the current directory:

    ```python
    from relational_datasets.request import deserialize_zipfile

    train, test = deserialize_zipfile(
        './cora_v0.0.3.zip',
        'cora',
    )
    ```
    """

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


def load(
    name: str, version: Optional[str] = None, *, fold: int = 1
) -> Tuple[RelationalDataset, RelationalDataset]:
    """Get train/test instances of a dataset

    Arguments:
        name: Dataset name (e.g. `toy_cancer`)
        version: Dataset version (e.g. `v0.0.3`)
        fold: In datasets with multiple folds, return this fold. This value is
            ignored if the data is not split into multiple folds.

    Returns:
        Returns the training and test.

    Raises:
        urllib.error.URLError: If the data is not in the cache and cannot be
            downloaded, a failed request will raise this exception.

    Examples:

    Load version ``v0.0.3`` of the ``toy_cancer`` dataset:

    ```python
    >>> from relational_datasets import load
    >>> train, test = load("toy_cancer", "v0.0.3")
    >>> train.pos
    ['cancer(alice).', 'cancer(bob).', 'cancer(chuck).', 'cancer(fred).']
    ```
    """
    data_location = fetch(name, version)
    return deserialize_zipfile(data_location, name=name, fold=fold)


def fetch(name: str, version: Optional[str] = None) -> str:
    """Get a dataset with a name/version. Return path to a zipfile.

    Something else.

    Arguments:
        name: Dataset name, usually lowercase with underscores.
        version: Dataset version. Downloads a default (`v0.0.3`) if not provided.

    Returns:
        A string representing the path to the downloaded dataset. For example:

        ```python
        '/home/user/relational_datasets/toy_cancer_v0.0.3.zip'
        ```

        The path is converted to a string from a `pathlib` object, so it should
        work cross-platform.

    Raises:
        urllib.error.URLError: If the data is not in the cache and cannot be
            downloaded, a failed request will raise this exception.

    Examples:

    Fetch `toy_cancer` dataset, version `v0.0.3`:

    ```python
    from relational_datasets import fetch

    fetch('toy_cancer', 'v0.0.3')
    # '/home/user/relational_datasets/toy_cancer_v0.0.3.zip'
    ```
    """

    # TODO(hayesall): This logic might be moved into the same function.
    data_file = _make_file_path(name, version)
    if data_file.is_file():
        return str(data_file)

    # Else the data needs to be downloaded.

    download_url = _make_data_url(name, version)

    with urlopen(download_url) as url:
        data = BytesIO(url.read())

    with open(data_file, "wb") as _fh:
        _fh.write(data.getbuffer())

    return str(data_file)


def _make_file_path(name: str, version: str = ""):
    """Create a file path where data are stored.

    If a `version` is not provided, the `LATEST_VERSION` is used.
    """
    if not version:
        return pathlib.Path(get_data_home()).joinpath(f"{name}_{LATEST_VERSION}.zip")
    return pathlib.Path(get_data_home()).joinpath(f"{name}_{version}.zip")


def _make_data_url(name: str, version: str = "") -> str:
    """Create a URL for a dataset with ``name`` and ``version``.

    If a ``version`` is not provided, the latest version is returned.
    """

    assert name in DATASETS

    if version in ["v0.0.2", "v0.0.3"]:
        logging.warning("Versions v0.0.2, v0.0.3 will be deprecated in the future.")
        return OLD_VERSION_URL.format(archive=name, version=version)
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
