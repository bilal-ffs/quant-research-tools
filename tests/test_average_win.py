import pandas as pd
import pytest

from quanttools.statistics.average_win import (
    average_win,
)


def test_average_win_returns_float():
    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
            50,
        ]
    )

    result = average_win(
        trade_results
    )

    assert isinstance(result, float)


def test_empty_series():
    trade_results = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        average_win(
            trade_results
        )


def test_invalid_input_type():
    with pytest.raises(TypeError):
        average_win(
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

    result = average_win(
        trade_results
    )

    assert isinstance(result, float)


def test_no_winning_trades():
    trade_results = pd.Series(
        [
            -100,
            -50,
            -25,
        ]
    )

    with pytest.raises(ValueError):
        average_win(
            trade_results
        )


def test_average_calculation():
    trade_results = pd.Series(
        [
            100,
            -50,
            50,
            -25,
        ]
    )

    result = average_win(
        trade_results
    )

    assert result == pytest.approx(75.0)


def test_single_winning_trade():
    trade_results = pd.Series(
        [
            -100,
            200,
            -50,
        ]
    )

    result = average_win(
        trade_results
    )

    assert result == pytest.approx(200.0)