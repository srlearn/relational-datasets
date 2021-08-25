# relational-datasets

*A small library for loading and downloading relational datasets.*

```bash
pip install relational-datasets
```

[![PyPi Version](https://img.shields.io/pypi/v/relational-datasets)](https://pypi.org/project/relational-datasets/)
[![License](https://img.shields.io/github/license/srlearn/relational-datasets)](https://github.com/srlearn/relational-datasets/blob/main/LICENSE)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/srlearn/relational-datasets.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/srlearn/relational-datasets/alerts/)
[![codecov](https://codecov.io/gh/srlearn/relational-datasets/branch/main/graph/badge.svg?token=lutvcUSBRF)](https://codecov.io/gh/srlearn/relational-datasets)
[![Python Package Builds](https://github.com/srlearn/relational-datasets/actions/workflows/python-package.yml/badge.svg)](https://github.com/srlearn/relational-datasets/actions/workflows/python-package.yml)
[![Documentation Deploy](https://github.com/srlearn/relational-datasets/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/srlearn/relational-datasets/actions/workflows/deploy-docs.yml)

## Beta Release

This API and the datasets at
[https://github.com/srlearn/datasets/](https://github.com/srlearn/datasets/)
are currently being experimented with.

- <img src='https://avatars.githubusercontent.com/u/743164?s=200&v=4' height='20' width='20'/></a> Prefer *Julia*? Check out [**RelationalDatasets.jl**](https://github.com/srlearn/RelationalDatasets.jl).

Open enhancements and bugs are tracked here:

- [Issues: relational-datasets package](https://github.com/srlearn/relational-datasets/issues)
- [Issues: datasets](https://github.com/srlearn/datasets/issues)

But here is a short-term Roadmap:

- [ ] Modes: https://github.com/srlearn/datasets/issues/11
- [ ] Converting propositional->relational
  - [ ] Problem Settings
    - [X] Binary Classification
      - [X] Classification: (0, 1)
      - [ ] Classification: (-1, 1)
      - [ ] Classification: maybe recommend [`sklearn.preprocessing.LabelBinarizer`](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelBinarizer.html)
    - [X] Regression
      - [X] Regression: y ∈ `float`
    - [ ] Multiclass Classification: When target is `int` and in `[0, 1, 2, ...]`
  - [ ] Categorical datatype support in `X` matrix.
  - [ ] Dataframes: `pandas`

## Use Case 1: Fetching Zipfiles

**Running** the `fetch` method downloads a version of a datset to your local cache:

```python
import relational_datasets

relational_datasets.fetch("toy_cancer")
relational_datasets.fetch("toy_father", "v0.0.3")
relational_datasets.fetch("cora")
```

**Resulting in**:

```console
~/relational_datasets/
├── toy_cancer_v0.0.4.zip   <--- latest
├── toy_father_v0.0.3.zip   <--- specific version
└── cora_v0.0.4.zip         <--- latest
```

## Use Case 2: Loading Data

The `load` method returns train and test folds—each with `pos`, `neg`, and
`facts`. Internally it uses `fetch`, so it will automatically download a
dataset if it is not available.

For example: "*Load fold-2 of webkb*"

```python
from relational_datasets import load

train, test = load("webkb", "v0.0.4", fold=2)

len(train.facts)
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

data, modes = from_numpy(
  np.array([[0, 1, 1], [0, 1, 2], [1, 2, 2]]),
  np.array([0, 0, 1]),
)

data, modes
```

```console
(RelationalDataset(pos=['v4(id3).'], neg=['v4(id1).', 'v4(id2).'], facts=['v1(id1,0).', 'v1(id2,0).', 'v1(id3,1).', 'v2(id1,1).', 'v2(id2,1).', 'v2(id3,2).', 'v3(id1,1).', 'v3(id2,2).', 'v3(id3,2).']),
['v1(+id,#varv1).', 'v2(+id,#varv2).', 'v3(+id,#varv3).', 'v4(+id).'])
```

### Regression

*When `y` is a vector of floats*

```python
from relational_datasets.convert import from_numpy
import numpy as np

data, modes = from_numpy(
  np.array([[0, 1, 1], [0, 1, 2], [1, 2, 2]]),
  np.array([1.1, 0.9, 2.5]),
)

data, modes
```

```console
(RelationalDataset(pos=['regressionExample(v4(id1),1.1).', 'regressionExample(v4(id2),0.9).', 'regressionExample(v4(id3),2.5).'], neg=[], facts=['v1(id1,0).', 'v1(id2,0).', 'v1(id3,1).', 'v2(id1,1).', 'v2(id2,1).', 'v2(id3,2).', 'v3(id1,1).', 'v3(id2,2).', 'v3(id3,2).']),
['v1(+id,#varv1).', 'v2(+id,#varv2).', 'v3(+id,#varv3).', 'v4(+id).'])
```

### Preprocessing scikit-learn's `load_breast_cancer`

[`load_breast_cancer`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_breast_cancer.html)
is based on the
[Breast Cancer Wisconsin dataset](https://archive.ics.uci.edu/ml/datasets/Breast+Cancer+Wisconsin+(Diagnostic)).

Here we: (**1**) load the data and class labels,
(**2**) split into training and test sets, (**3**) bin the continuous
features to discrete, and (**4**) convert to the relational format.

```python
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import KBinsDiscretizer

# (1) Load
X, y = load_breast_cancer(return_X_y=True)

# (2) Split
X_train, X_test, y_train, y_test = train_test_split(X, y)

# (3) Discretize
disc = KBinsDiscretizer(n_bins=5, encode="ordinal")
X_train = disc.fit_transform(X_train)
X_test = disc.transform(X_test)
X_train = X_train.astype(int)
X_test = X_test.astype(int)

# (4) Convert
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
