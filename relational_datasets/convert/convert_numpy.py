# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

"""Convert vector-based ML datasets to tuple-based ILP datasets.
"""

from typing import List, Tuple, Optional

import numpy as np

from ..types import RelationalDataset


def _get_task(y: np.ndarray) -> str:
    """Return classification/regression"""

    if str(y.dtype) == 'int64':
        return 'classification'
    elif str(y.dtype) == 'float64':
        return 'regression'
    raise TypeError("Could not determine classification or regression from `y`")


def from_numpy(X: np.ndarray, y: np.ndarray, names: Optional[List[str]] = None) -> Tuple[RelationalDataset, List[str]]:
    """Convert a pair of numpy data (X) and target (y) arrays to a
    RelationalDataset"""

    # TODO(hayesall): All `enumerate` calls start from `1` to maintain
    #   parity with Julia module.

    if not names:
        # + 2 to start from 1.
        names = [f"v{i}" for i in range(1, X.shape[1] + 2)]

    pos, neg, facts = [], [], []

    # TODO(hayesall): This is a way to "fail fast": if we cannot determine
    #   type of the `y` vector, the conversion is not possible.
    if _get_task(y) == "classification":
        for i, row in enumerate(y, 1):
            if row:
                pos.append(f"{names[-1]}(id{i}).")
            else:
                neg.append(f"{names[-1]}(id{i}).")

    else:
        # _get_task(y) == "regression"
        for i, row in enumerate(y, 1):
            pos.append(f"regressionExample({names[-1]}(id{i}),{row}).")

    for i, col in enumerate(X.T):
        var = names[i]
        facts += [f"{var}(id{j},{row})." for j, row in enumerate(col, 1)]

    modes = [f"{name}(+id,#var{name})." for name in names[:-1]]
    modes += [f"{names[-1]}(+id)."]

    return RelationalDataset(pos=pos, neg=neg, facts=facts), modes
