import pandas as pd
import pytest

from quanttools.risk import (
    downside_deviation,
)


def test_returns_float():
    returns = pd.Series(
        [
            0.02,
            -0.01,
            0.03,
            -0.02,
            0.01,
        ]
    )

    result = downside_deviation(
        returns,
    )

    assert isinstance(
        result,
        float,
    )


def test_empty_returns():
    returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        downside_deviation(
            returns,
        )


def test_invalid_input():
    with pytest.raises(TypeError):
        downside_deviation(
            [
                0.01,
                0.02,
            ],
        )


def test_nan_values():
    returns = pd.Series(
        [
            0.01,
            None,
            -0.02,
            0.03,
        ]
    )

    result = downside_deviation(
        returns,
    )

    assert isinstance(
        result,
        float,
    )


def test_no_downside_returns():
    returns = pd.Series(
        [
            0.01,
            0.02,
            0.03,
        ]
    )

    result = downside_deviation(
        returns,
    )

    assert result == 0.0
