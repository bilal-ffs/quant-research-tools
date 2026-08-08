import pandas as pd
import pytest

from quanttools.statistics.win_rate import (
    win_rate,
)


def test_win_rate_returns_float():
    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
            50,
        ]
    )

    result = win_rate(trade_results)

    assert isinstance(result, float)


def test_empty_series():
    trade_results = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        win_rate(trade_results)


def test_invalid_input_type():
    with pytest.raises(TypeError):
        win_rate(
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

    result = win_rate(trade_results)

    assert isinstance(result, float)


def test_no_winning_trades():
    trade_results = pd.Series(
        [
            -100,
            -50,
            -25,
        ]
    )

    assert win_rate(trade_results) == 0.0


def test_all_winning_trades():
    trade_results = pd.Series(
        [
            100,
            50,
            25,
        ]
    )

    assert win_rate(trade_results) == 1.0


def test_partial_win_rate():
    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
        ]
    )

    assert win_rate(trade_results) == pytest.approx(0.5)
