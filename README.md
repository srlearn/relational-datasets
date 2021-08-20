# relational-datasets - (Pre-Alpha Release)

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
