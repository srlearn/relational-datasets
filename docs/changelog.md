# Changelog

## Beta

### v0.2.1 - 2021-12-01

Software Changes:

- Add `drug_interactions` and `toy_machines` datasets
- Add `v0.0.5` as the latest `srlearn/datasets` release

### v0.2.0 - 2021-08-27

Software Changes:

- Add `convert` module with `from_numpy` implementation to convert binary
  classification and regression datasets based on ordinal encodings.
- Fix type annotations in `relational_datasets.request`
- Fix type annotations in `relational_datasets.types`

Documentation:

- Add tutorial for converting vector/propositional datasets to relational
- Add `mkdocs` dependency: `pymdownx.tasklist`
- Add `binder` and `colab` launch badges to Jupyter notebook tutorials

Testing:

- Add `lgtm` build step + README badge
- Add `codecov` build step + README badge
- Add `numpy>=1.20.0` as an optional setup target, and test against it
  (this is the earliest version of `numpy` where type annotations for `mypy`
  seem to be consistently available)

## Pre-Alpha

### v0.1.1 - 2021-08-10

Software Changes:

- Bump default dataset version: `v0.0.3` → `v0.0.4`.
- Between `v0.0.3` and `v0.0.4` of `srlearn/datasets`, all zipfiles now have the version number appended
  (e.g. `toy_cancer_v0.0.4.zip`). Add logic to request the correct filename from GitHub.
- Add `deserialize_zipfile` function, split out code for pulling zipfile content from the `load` method.
- Add private `_make_file_path` function to handle where zipfiles are stored on a user's filesystem.
- Move `RelationalDataset` type into `relational_datasets/types.py`
- Fix `hayesall/relational_datasets` → `srlearn/relational_datasets` in `setup.py`
- Clarify `typing.Optional` in function signatures where default file paths are allowed.
- Add `__version__` to the main `__init__`, so `print(relational_datasets.__version__)` is valid.

Documentation:

- Add `mkdocs` builds with each push to the `main` branch.
- Add `requirements_dev.txt` with requirements to build documentation.
- Add `docs/build._docs.py` to build a *Downloads* page and an overview of each dataset pulled from the `srlearn/datasets` repository.
- Add `docs/notebooks/` directory for literate tutorials
    - Add `00_loading_and_fetching.ipynb`
- Pages for functions and types:
    - `types.RelationalDataset`
    - `request.deserialize_zipfile`
    - `request.fetch`
    - `request.latest_version`
    - `request.load`

### v0.1.0 - 2021-07-21

Release basic specification:

- `load(name: str, version: str = "", fold: int = 1) -> Tuple[RelationalDataset, RelationalDataset]`: Load examples and facts for a dataset/version/fold
- `fetch(name: str, version: str = "") -> str`: Download and cache an archive locally
- `get_data_home(data_home=None) -> str`: Get the path to the cache directory
- `clear_data_home(data_home=None) -> None`: Remove the cache directory
- `latest_version() -> str`: Check latest version of datasets on GitHub
