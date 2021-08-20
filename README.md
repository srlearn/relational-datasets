# relational-datasets - (Pre-Alpha Release)

*A small library for loading and downloading relational datasets.*

```bash
pip install relational-datasets
```

[![PyPi Version](https://img.shields.io/pypi/v/relational-datasets)](https://pypi.org/project/relational-datasets/)
[![License](https://img.shields.io/github/license/srlearn/relational-datasets)](https://github.com/srlearn/relational-datasets/blob/main/LICENSE)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/srlearn/relational-datasets.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/srlearn/relational-datasets/alerts/)
[![Python Package Builds](https://github.com/srlearn/relational-datasets/actions/workflows/python-package.yml/badge.svg)](https://github.com/srlearn/relational-datasets/actions/workflows/python-package.yml)
[![Documentation Deploy](https://github.com/srlearn/relational-datasets/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/srlearn/relational-datasets/actions/workflows/deploy-docs.yml)

## Pre-Alpha Release

This API and the datasets at
[https://github.com/srlearn/datasets/](https://github.com/srlearn/datasets/)
are currently being experimented with.

Open enhancements and bugs are tracked here:

- [Issues: relational-datasets package](https://github.com/srlearn/relational-datasets/issues)
- [Issues: datasets](https://github.com/srlearn/datasets/issues)

## Use Case 1: Fetching Zipfiles

**Running** the `fetch` method downloads a version of a datset to your local cache:

```python
import relational_datasets

relational_datasets.fetch("toy_cancer")
relational_datasets.fetch("toy_father", "v0.0.2")
relational_datasets.fetch("cora")
```

**Resulting in**:

```console
~/relational_datasets/
├── toy_cancer_v0.0.3.zip   <--- latest
├── toy_father_v0.0.2.zip   <--- specific version
└── cora_v0.0.3.zip         <--- latest
```

## Use Case 2: Loading Data

The `load` method returns train and test folds—each with `pos`, `neg`, and
`facts`. Internally it uses `fetch`, so it will automatically download a
dataset if it is not available.

For example: "*Load fold-2 of webkb*"

```python
from relational_datasets import load

train, test = load("webkb", "v0.0.3", fold=2)

print(len(train.facts))
# 1344
```

## Use Case 3: Working with Standard (Vector-based) Machine Learning Datasets

The `relational_datasets.convert` module has functions for
converting vector-based datasets into relational/ILP-style
datasets:

### Binary Classification

*When `y` is a vector of 0/1*

```python
from relational_datasets.convert import from_numpy
import numpy as np

X = np.array([[0, 1, 1], [0, 1, 2], [1, 2, 2]])
y = np.array([0, 0, 1])

data, modes = from_numpy(X, y)
```

### Regression

*When `y` is a vector of floats*

```python
from relational_datasets.convert import from_numpy
import numpy as np

X = np.array([[0, 1, 1], [0, 1, 2], [1, 2, 2]])
y = np.array([1.1, 0.9, 2.5])

data, modes = from_numpy(X, y)
```

### Example using scikit-learn's `load_breast_cancer`

"Breast Cancer" is based on the Breast Cancer Wisconsin
dataset.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import KBinsDiscretizer
from sklearn.model_selection import train_test_split

X, y = load_breast_cancer(return_X_y=True)

# Discretize continuous features into ordinal categories:
disc = KBinsDiscretizer(n_bins=5, encode="ordinal")
X = disc.fit_transform(X)
X = X.astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y)

# ---

from relational_datasets.convert import from_numpy

train, modes = from_numpy(X_train, y_train)
test, _ = from_numpy(X_test, y_test)
```

## Install

### From PyPi

```bash
pip install relational-datasets
```

### From GitHub Source

```bash
git clone https://github.com/srlearn/relational-datasets.git
cd relational-datasets
pip install -e .
```

## Contributions

- [Alexander Hayes](https://hayesall.com) - *Indiana University, Bloomington*

This package was partially based on datasets from the
[Starling Lab Datasets Collection](https://starling.utdallas.edu/datasets/),
which included specific contributions by
[Harsha Kokel](https://harshakokel.com/) and
[Devendra Singh Dhami](https://sites.google.com/view/devendradhami).
[Tushar Khot](https://allenai.org/team/tushark) converted many to the ILP
format from Alchemy 2 format, but that occurred before versions were tracked.
Some inspiration was drawn from the
"[RelationalDatasets](https://github.com/joschout/RelationalDatasets)" list that
[Jonas Schouterden](https://people.cs.kuleuven.be/~jonas.schouterden/) collected.
