import pandas as pd
import pytest

from quanttools.statistics.sortino import sortino_ratio


def test_sortino_returns_float():
    returns = pd.Series(
        [
            0.01,
            -0.005,
            -0.01,
            0.02,
            0.015,
        ]
    )

    result = sortino_ratio(returns)

    assert isinstance(result, float)


def test_empty_series():
    returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        sortino_ratio(returns)


def test_invalid_input_type():
    with pytest.raises(TypeError):
        sortino_ratio(
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
            -0.02,
            -0.01,
            0.02,
        ]
    )

    result = sortino_ratio(returns)

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
        sortino_ratio(returns)


def test_risk_free_rate_changes_result():
    returns = pd.Series(
        [
            0.01,
            -0.02,
            -0.01,
            0.015,
        ]
    )

    sortino_no_rf = sortino_ratio(
        returns,
        risk_free_rate=0.0,
    )

    sortino_with_rf = sortino_ratio(
        returns,
        risk_free_rate=0.05,
    )

    assert sortino_with_rf < sortino_no_rf


def test_periods_per_year_changes_result():
    returns = pd.Series(
        [
            0.01,
            -0.01,
            0.02,
            -0.015,
        ]
    )

    daily = sortino_ratio(
        returns,
        periods_per_year=252,
    )

    monthly = sortino_ratio(
        returns,
        periods_per_year=12,
    )

    assert daily != monthly
