import pandas as pd
import pytest

from quanttools.statistics.calmar import calmar_ratio


def test_calmar_returns_float():
    returns = pd.Series(
        [
            0.10,
            -0.05,
            0.20,
            -0.10,
            0.15,
        ]
    )

    result = calmar_ratio(returns)

    assert isinstance(result, float)


def test_empty_series():
    returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        calmar_ratio(returns)


def test_invalid_input_type():
    with pytest.raises(TypeError):
        calmar_ratio(
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
            -0.10,
        ]
    )

    result = calmar_ratio(returns)

    assert isinstance(result, float)


def test_zero_drawdown():
    returns = pd.Series(
        [
            0.01,
            0.01,
            0.01,
            0.01,
        ]
    )

    with pytest.raises(ValueError):
        calmar_ratio(returns)


def test_positive_calmar():
    returns = pd.Series(
        [
            0.10,
            -0.05,
            0.20,
            -0.10,
            0.15,
        ]
    )

    result = calmar_ratio(returns)

    assert result > 0


def test_negative_calmar():
    returns = pd.Series(
        [
            -0.10,
            0.02,
            -0.15,
            0.01,
            -0.08,
        ]
    )

    result = calmar_ratio(returns)

    assert result < 0