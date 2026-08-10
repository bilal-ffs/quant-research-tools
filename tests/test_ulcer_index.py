import pandas as pd
import pytest

from quanttools.risk import (
    ulcer_index,
)


def test_ulcer_index_returns_float():
    returns = pd.Series(
        [
            0.01,
            -0.02,
            0.03,
            -0.01,
            0.02,
        ]
    )

    result = ulcer_index(
        returns,
    )

    assert isinstance(
        result,
        float,
    )


def test_empty_returns():
    returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        ulcer_index(
            returns,
        )


def test_invalid_input():
    with pytest.raises(TypeError):
        ulcer_index(
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

    result = ulcer_index(
        returns,
    )

    assert isinstance(
        result,
        float,
    )


def test_no_drawdown():
    returns = pd.Series(
        [
            0.01,
            0.02,
            0.03,
        ]
    )

    result = ulcer_index(
        returns,
    )

    assert result == 0.0


def test_drawdown_produces_positive_value():
    returns = pd.Series(
        [
            0.10,
            -0.05,
            -0.05,
            0.02,
        ]
    )

    result = ulcer_index(
        returns,
    )

    assert result > 0.0
