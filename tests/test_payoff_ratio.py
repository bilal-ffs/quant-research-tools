import pandas as pd
import pytest

from quanttools.statistics.payoff_ratio import (
    payoff_ratio,
)


def test_payoff_ratio_returns_float():
    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
        ]
    )

    result = payoff_ratio(
        trade_results
    )

    assert isinstance(result, float)


def test_empty_series():
    trade_results = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        payoff_ratio(
            trade_results
        )


def test_invalid_input_type():
    with pytest.raises(TypeError):
        payoff_ratio(
            [
                100,
                -50,
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

    result = payoff_ratio(
        trade_results
    )

    assert isinstance(result, float)


def test_no_winning_trades():
    trade_results = pd.Series(
        [
            -100,
            -50,
        ]
    )

    with pytest.raises(ValueError):
        payoff_ratio(
            trade_results
        )


def test_no_losing_trades():
    trade_results = pd.Series(
        [
            100,
            50,
        ]
    )

    with pytest.raises(ValueError):
        payoff_ratio(
            trade_results
        )


def test_payoff_ratio_calculation():
    trade_results = pd.Series(
        [
            100,
            50,
            -50,
            -100,
        ]
    )

    result = payoff_ratio(
        trade_results
    )

    assert result == pytest.approx(1.0)