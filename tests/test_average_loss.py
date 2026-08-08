import pandas as pd
import pytest

from quanttools.statistics.average_loss import (
    average_loss,
)


def test_average_loss_returns_float():
    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
            50,
        ]
    )

    result = average_loss(trade_results)

    assert isinstance(result, float)


def test_empty_series():
    trade_results = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        average_loss(trade_results)


def test_invalid_input_type():
    with pytest.raises(TypeError):
        average_loss(
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

    result = average_loss(trade_results)

    assert isinstance(result, float)


def test_no_losing_trades():
    trade_results = pd.Series(
        [
            100,
            50,
            25,
        ]
    )

    with pytest.raises(ValueError):
        average_loss(trade_results)


def test_average_calculation():
    trade_results = pd.Series(
        [
            100,
            -50,
            -100,
            75,
        ]
    )

    result = average_loss(trade_results)

    assert result == pytest.approx(75.0)


def test_single_losing_trade():
    trade_results = pd.Series(
        [
            100,
            -200,
            50,
        ]
    )

    result = average_loss(trade_results)

    assert result == pytest.approx(200.0)
