import pandas as pd
import pytest

from quanttools.statistics.sharpe import sharpe_ratio


def test_sharpe_returns_float():
    returns = pd.Series(
        [
            0.01,
            -0.005,
            0.02,
            0.015,
        ]
    )

    result = sharpe_ratio(returns)

    assert isinstance(result, float)


def test_empty_series():
    returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        sharpe_ratio(returns)


def test_invalid_input_type():
    with pytest.raises(TypeError):
        sharpe_ratio(
            [
                0.01,
                0.02,
            ]
        )


def test_nan_values():
    returns = pd.Series(
        [
            0.01,
            None,
            0.02,
            -0.01,
        ]
    )

    result = sharpe_ratio(returns)

    assert isinstance(result, float)


def test_zero_volatility():
    returns = pd.Series(
        [
            0.01,
            0.01,
            0.01,
            0.01,
        ]
    )

    with pytest.raises(ValueError):
        sharpe_ratio(returns)