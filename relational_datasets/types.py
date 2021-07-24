# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

"""
Custom Types
"""

from collections import namedtuple
from typing import List, NamedTuple

__all__ = ["RelationalDataset"]


RelationalDataset = NamedTuple(
    "RelationalDataset", [("pos", List[str]), ("neg", List[str]), ("facts", List[str]),]
)

RelationalDataset.__doc__ = """
```python
RelationalDataset(pos: List[str], neg: List[str], facts: List[str])
```

Examples:

    Create an instance of a `RelationalDataset` type:

    ```python
    from relational_datasets import RelationalDataset

    train = RelationalDataset(
        pos=["related(a,b)."],
        neg=["related(b,c)."],
        facts=["child(a,b)."],
    )
    ```

    Instances of `RelationalDataset` are returned by the
    [`load`](../api/request.load.md) function.

    ```python
    from relational_datasets import load

    train, _ = load("toy_cancer")
    print(type(train))
    # <class 'relational_datasets.types.RelationalDataset'>
    ```

    Keys may be accessed with dot notation:

    ```python
    from relational_datasets import load

    train, _ = load("toy_cancer")
    print(train.pos)
    # ['cancer(alice).', 'cancer(bob).', 'cancer(chuck).', 'cancer(fred).']
    ```
---
"""
RelationalDataset.pos.__doc__ += ": List of positive examples"
RelationalDataset.neg.__doc__ += ": List of negative examples"
RelationalDataset.facts.__doc__ += ": List of facts for the domain"
