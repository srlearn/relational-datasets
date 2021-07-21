# Copyright © 2021 Alexander L. Hayes
# MIT License

from setuptools import setup
from setuptools import find_packages

setup(
    name="srlearn_datasets",
    packages=find_packages(exclude=["tests"]),
    package_dir={"srlearn_datasets": "srlearn_datasets"},
    author="Alexander L. Hayes",
    author_email="alexander@batflyer.net",
    description="Relational datasets compatible with srlearn",
)
