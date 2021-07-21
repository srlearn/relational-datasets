# relational-datasets

*A small library for loading and downloading relational datasets.*

## Use Case 1: Managing Zipfiles of Data

**Running** the `fetch` method downloads a version of a datset to your local cache:

```python
import relational_datasets

relational_datasets.fetch("toy_cancer")
relational_datasets.fetch("toy_father", "v0.0.2")
relational_datasets.fetch("webkb")
```

**Resulting in**:

```console
~/relational_datasets/
├── toy_cancer_v0.0.3.zip   <--- latest
├── toy_father_v0.0.2.zip   <--- specific version
└── webkb_v0.0.3.zip        <--- latest
```

## Use Case 2: Loading Data

The `load` method returns train and test folds—each with `pos`, `neg`, and `facts`.

For example: "*Load fold-2 of webkb*"

```python
from relational_datsets import load

train, test = load("webkb", fold=2)

print(len(train.facts))
# 1344 facts in fold-2 of webkb
```

## Install

### From PyPi

```bash
pip install relational-datasets
```

### From GitHub Source

```bash
git clone git@github.com:hayesall/relational-datasets.git
cd relational-datasets
pip install -e .
```

---

## Function Signatures: Quick Reference

Load or fetch data:

```python
load(name: str, version: str = "", fold: int = 1) -> Tuple[RelationalDataset, RelationalDataset]
fetch(name: str, version: str = "") -> str
```

Get or clear the cache directory:

```python
get_data_home(data_home=None) -> str
clear_data_home(data_home=None) -> None
```

Helper method to check the latest version of datasets on GitHub:

```python
latest_version() -> str
```
