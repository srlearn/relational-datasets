# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

"""Convert vector-based ML datasets to tuple-based ILP datasets.
"""

from typing import List, Tuple, Optional

import numpy as np

from ..types import RelationalDataset


def _get_task(y: np.ndarray) -> str:
    """Return classification/regression"""

    if str(y.dtype)[:3] == 'int':
        return 'classification'
    elif str(y.dtype)[:5] == 'float':
        return 'regression'
    raise TypeError("Could not determine classification or regression from `y` with type: " + str(y.dtype))


def from_numpy(X: np.ndarray, y: np.ndarray, names: Optional[List[str]] = None) -> Tuple[RelationalDataset, List[str]]:
    """Convert numpy data (`X`) and target (`y`) arrays to a RelationalDataset
    with modes.

    Arguments:
        X: Integer matrix of covariates
        y: Integer or float array containing the target variable
        names: List of strings representing the variable names

    Returns:
        Tuple of `RelationalDataset` and a list of strings containing the modes

    Raises:
        TypeError: When classification vs. regression cannot be determined from
            the types of the input values.

    Examples:

    Demonstrates converting a set of binary classification data.

    ```python
    from relational_datasets.convert import from_numpy
    import numpy as np

    data, modes = from_numpy(
      np.array([[0, 1, 1], [0, 1, 2], [1, 2, 2]]),
      np.array([0, 0, 1]),
    )
    ```

    """

    assert X.shape[0] == y.shape[0]

    # TODO(hayesall): All `enumerate` calls start from `1` to maintain
    #   parity with Julia module.

    # TODO(hayesall): This is a way to "fail fast": if we cannot determine
    #   type of the `y` vector, the conversion is not possible.
    _task = _get_task(y)

    if names:
        assert len(names) == X.shape[1] + 1
    else:
        # + 2 to start from 1.
        names = [f"v{i}" for i in range(1, X.shape[1] + 2)]

    pos, neg, facts = [], [], []

    if _task == "classification":
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
