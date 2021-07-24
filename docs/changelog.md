# Changelog

## Pre-Alpha

### v0.1.0 - 2021-07-21

Release basic specification:

- `load(name: str, version: str = "", fold: int = 1) -> Tuple[RelationalDataset, RelationalDataset]`: Load examples and facts for a dataset/version/fold
- `fetch(name: str, version: str = "") -> str`: Download and cache an archive locally
- `get_data_home(data_home=None) -> str`: Get the path to the cache directory
- `clear_data_home(data_home=None) -> None`: Remove the cache directory
- `latest_version() -> str`: Check latest version of datasets on GitHub
