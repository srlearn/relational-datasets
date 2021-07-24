# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

# `get_data_home` and `clear_data_home` are nearly identical to two
#  methods with the same name from `scikit-learn` (circa July 20, 2021).
#  The source file was distributed under the terms of a BSD 3 clause license.
# Copyright © 2007 David Cournapeau <cournape@gmail.com>
#             2010 Fabian Pedregosa <fabian.pedregosa@inria.fr>
#             2010 Olivier Grisel <olivier.grisel@ensta.org>
# License: BSD 3 clause

"""
Utility methods
"""

from os import environ
from os import makedirs
from os.path import join
from os.path import expanduser
import shutil
from typing import Optional

__all__ = ["get_data_home", "clear_data_home"]


def get_data_home(data_home: Optional[str] = None) -> str:
    """Return the path to the relational-datasets home directory.

    Examples:

    If the ``RELATIONAL_DATASETS`` environment variable is set, this will use
    the location.

    ```bash
    RELATIONAL_DATASETS=my_custom_directory python
    ```
    """
    if data_home is None:
        data_home = environ.get("RELATIONAL_DATASETS", join("~", "relational_datasets"))
    data_home = expanduser(data_home)
    makedirs(data_home, exist_ok=True)
    return data_home


def clear_data_home(data_home: Optional[str] = None) -> None:
    """Delete all content of the data home cache.
    """
    data_home = get_data_home(data_home)
    shutil.rmtree(data_home)
