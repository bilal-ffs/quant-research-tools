import pandas as pd
import pytest

from quanttools.statistics.expectancy import (
    expectancy,
)


def test_expectancy_returns_float():
    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
            50,
        ]
    )

    result = expectancy(trade_results)

    assert isinstance(result, float)


def test_empty_series():
    trade_results = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        expectancy(trade_results)


def test_invalid_input_type():
    with pytest.raises(TypeError):
        expectancy(
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

    result = expectancy(trade_results)

    assert isinstance(result, float)


def test_no_winning_trades():
    trade_results = pd.Series(
        [
            -100,
            -50,
            -75,
        ]
    )

    with pytest.raises(ValueError):
        expectancy(trade_results)


def test_no_losing_trades():
    trade_results = pd.Series(
        [
            100,
            50,
            75,
        ]
    )

    with pytest.raises(ValueError):
        expectancy(trade_results)


def test_positive_expectancy():
    trade_results = pd.Series(
        [
            100,
            -25,
            75,
            -20,
            50,
        ]
    )

    result = expectancy(trade_results)

    assert result > 0
