import pandas as pd
import pytest

from quanttools.statistics.cagr import cagr


def test_cagr_returns_float():
    returns = pd.Series(
        [
            0.10,
            -0.05,
            0.20,
            0.05,
        ]
    )

    result = cagr(returns)

    assert isinstance(result, float)


def test_empty_series():
    returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        cagr(returns)


def test_invalid_input_type():
    with pytest.raises(TypeError):
        cagr(
            [
                0.10,
                -0.05,
            ]
        )


def test_nan_values():
    returns = pd.Series(
        [
            0.10,
            None,
            -0.05,
            0.20,
        ]
    )

    result = cagr(returns)

    assert isinstance(result, float)


def test_zero_returns():
    returns = pd.Series(
        [
            0.0,
            0.0,
            0.0,
            0.0,
        ]
    )

    result = cagr(returns)

    assert result == pytest.approx(0.0)


def test_positive_returns():
    returns = pd.Series(
        [
            0.10,
            0.08,
            0.12,
            0.05,
        ]
    )

    result = cagr(returns)

    assert result > 0


def test_negative_returns():
    returns = pd.Series(
        [
            -0.05,
            -0.02,
            -0.08,
            -0.03,
        ]
    )

    result = cagr(returns)

    assert result < 0
