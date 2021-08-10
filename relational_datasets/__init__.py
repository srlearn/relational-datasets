# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

"""
Relational Datasets
===================
"""

from ._base import get_data_home
from ._base import clear_data_home
from .request import fetch
from .request import load
from .request import latest_version
from ._version import __version__

__all__ = [
    "get_data_home",
    "clear_data_home",
    "fetch",
    "load",
    "latest_version",
]
