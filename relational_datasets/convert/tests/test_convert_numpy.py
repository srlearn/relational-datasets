# Copyright © 2021 Alexander L. Hayes
# Apache 2.0 License

"""Tests for the `convert_numpy` module
"""

import pytest

numpy = pytest.importorskip("numpy")

from relational_datasets.convert import from_numpy


def test_convert_numpy_classification():
    """Test converting a classification problem."""
    X = numpy.array([[0, 1, 1], [1, 0, 2], [2, 2, 0], [1, 1, 1]])
    y = numpy.array([0, 0, 1, 1])
    data, modes = from_numpy(X, y)

    assert data.pos == ["v4(id3).", "v4(id4)."]
    assert data.neg == [
        "v4(id1).",
        "v4(id2).",
    ]
    assert data.facts == [
        "v1(id1,v1_0).",
        "v1(id2,v1_1).",
        "v1(id3,v1_2).",
        "v1(id4,v1_1).",
        "v2(id1,v2_1).",
        "v2(id2,v2_0).",
        "v2(id3,v2_2).",
        "v2(id4,v2_1).",
        "v3(id1,v3_1).",
        "v3(id2,v3_2).",
        "v3(id3,v3_0).",
        "v3(id4,v3_1).",
    ]
    assert modes == [
        "v1(+id,#varv1).",
        "v2(+id,#varv2).",
        "v3(+id,#varv3).",
        "v4(+id).",
    ]


def test_convert_numpy_regression():
    """Test converting a regression problem."""
    X = numpy.array([[0, 1, 1], [1, 0, 2], [2, 2, 0], [1, 1, 1]])
    y = numpy.array([0.1, 0.2, 0.3, 0.4])
    data, modes = from_numpy(X, y)

    assert data.pos == [
        "regressionExample(v4(id1),0.1).",
        "regressionExample(v4(id2),0.2).",
        "regressionExample(v4(id3),0.3).",
        "regressionExample(v4(id4),0.4).",
    ]
    assert data.neg == []
    assert data.facts == [
        "v1(id1,v1_0).",
        "v1(id2,v1_1).",
        "v1(id3,v1_2).",
        "v1(id4,v1_1).",
        "v2(id1,v2_1).",
        "v2(id2,v2_0).",
        "v2(id3,v2_2).",
        "v2(id4,v2_1).",
        "v3(id1,v3_1).",
        "v3(id2,v3_2).",
        "v3(id3,v3_0).",
        "v3(id4,v3_1).",
    ]
    assert modes == [
        "v1(+id,#varv1).",
        "v2(+id,#varv2).",
        "v3(+id,#varv3).",
        "v4(+id).",
    ]


def test_convert_multiclass():
    """Test converting a multiclass classification problem."""

    X = numpy.array([[0, 1, 1], [1, 0, 2], [2, 2, 0], [1, 1, 1]])
    y = numpy.array([0, 0, 1, 2])
    data, modes = from_numpy(X, y)

    assert data.pos == [
        "v4(id1,v4_0).",
        "v4(id2,v4_0).",
        "v4(id3,v4_1).",
        "v4(id4,v4_2).",
    ]
    assert data.neg == []
    assert data.facts == [
        "v1(id1,v1_0).",
        "v1(id2,v1_1).",
        "v1(id3,v1_2).",
        "v1(id4,v1_1).",
        "v2(id1,v2_1).",
        "v2(id2,v2_0).",
        "v2(id3,v2_2).",
        "v2(id4,v2_1).",
        "v3(id1,v3_1).",
        "v3(id2,v3_2).",
        "v3(id3,v3_0).",
        "v3(id4,v3_1).",
    ]
    assert modes == [
        "v1(+id,#varv1).",
        "v2(+id,#varv2).",
        "v3(+id,#varv3).",
        "v4(+id,#classlabel).",
    ]
