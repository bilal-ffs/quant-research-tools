import pandas as pd
import pytest

from quanttools.statistics.profit_factor import (
    profit_factor,
)


def test_profit_factor_returns_float():
    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
            50,
        ]
    )

    result = profit_factor(trade_results)

    assert isinstance(result, float)


def test_empty_series():
    trade_results = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        profit_factor(trade_results)


def test_invalid_input_type():
    with pytest.raises(TypeError):
        profit_factor(
            [
                100,
                -50,
                75,
            ]
        )


def test_nan_values():
    trade_results = pd.Series(
        [
            100,
            None,
            -50,
            75,
        ]
    )

    result = profit_factor(
        trade_results
    )

    assert isinstance(result, float)


def test_zero_gross_loss():
    trade_results = pd.Series(
        [
            100,
            50,
            25,
        ]
    )

    with pytest.raises(ValueError):
        profit_factor(
            trade_results
        )


def test_positive_profit_factor():
    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
        ]
    )

    result = profit_factor(
        trade_results
    )

    assert result > 1


def test_loss_greater_than_profit():
    trade_results = pd.Series(
        [
            50,
            -150,
            25,
            -75,
        ]
    )

    result = profit_factor(
        trade_results
    )

    assert result < 1