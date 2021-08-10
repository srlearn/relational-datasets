# Copyright © 2021 Alexander L. Hayes
# MIT License

from setuptools import setup
from setuptools import find_packages

from codecs import open
from os import path

# Get __version__ from _version.py
with open(path.join("relational_datasets", "_version.py")) as _fh:
    exec(_fh.read())

_here = path.abspath(path.dirname(__file__))
with open(path.join(_here, "README.md"), "r", encoding="utf-8") as _fh:
    LONG_DESCRIPTION = _fh.read()

setup(
    name="relational-datasets",
    packages=find_packages(exclude=["tests"]),
    package_dir={"relational_datasets": "relational_datasets"},
    author="Alexander L. Hayes",
    author_email="alexander@batflyer.net",
    description="A small library for loading and downloading relational datasets",
    version=__version__,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://srlearn.github.io/relational-datasets/",
    download_url="https://github.com/srlearn/relational-datasets",
    license="Apache License, Version 2.0",
    python_requires=">=3.7",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    extra_requires={
        "tests": ["coverage", "pytest"],
    },
)
