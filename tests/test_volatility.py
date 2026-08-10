import pandas as pd
import pytest

from quanttools.risk import (
    volatility,
)


def test_volatility_returns_float():
    returns = pd.Series(
        [
            0.01,
            -0.02,
            0.03,
            0.01,
        ]
    )

    result = volatility(
        returns,
    )

    assert isinstance(
        result,
        float,
    )


def test_empty_returns():
    returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        volatility(
            returns,
        )


def test_invalid_input():
    with pytest.raises(TypeError):
        volatility(
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
            0.03,
            -0.02,
        ]
    )

    result = volatility(
        returns,
    )

    assert isinstance(
        result,
        float,
    )
