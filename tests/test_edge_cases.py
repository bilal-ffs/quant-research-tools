import pandas as pd
import pytest

from quanttools.portfolio import (
    beta,
    information_ratio,
    tracking_error,
    treynor_ratio,
)
from quanttools.risk import (
    downside_deviation,
    volatility,
)
from quanttools.statistics import (
    calmar_ratio,
)


def test_constant_returns_volatility():
    returns = pd.Series(
        [0.01, 0.01, 0.01, 0.01],
    )

    with pytest.raises(ValueError):
        volatility(returns)


def test_constant_benchmark_beta():
    portfolio = pd.Series(
        [0.01, 0.02, 0.03, 0.04],
    )

    benchmark = pd.Series(
        [0.01, 0.01, 0.01, 0.01],
    )

    with pytest.raises(ValueError):
        beta(
            portfolio,
            benchmark,
        )


def test_zero_tracking_error():
    portfolio = pd.Series(
        [0.01, 0.02, 0.03, 0.04],
    )

    benchmark = pd.Series(
        [0.01, 0.02, 0.03, 0.04],
    )

    with pytest.raises(ValueError):
        tracking_error(
            portfolio,
            benchmark,
        )


def test_zero_tracking_error_information_ratio():
    portfolio = pd.Series(
        [0.01, 0.02, 0.03, 0.04],
    )

    benchmark = pd.Series(
        [0.01, 0.02, 0.03, 0.04],
    )

    with pytest.raises(ValueError):
        information_ratio(
            portfolio,
            benchmark,
        )


def test_zero_beta_treynor():
    portfolio = pd.Series(
        [0.01, 0.01, 0.01, 0.01],
    )

    benchmark = pd.Series(
        [0.02, 0.03, 0.01, 0.04],
    )

    with pytest.raises(ValueError):
        treynor_ratio(
            portfolio,
            benchmark,
        )


def test_no_downside_deviation():
    returns = pd.Series(
        [0.01, 0.02, 0.03, 0.04],
    )

    with pytest.raises(ValueError):
        downside_deviation(
            returns,
        )


def test_no_downside_deviation():
    returns = pd.Series(
        [0.01, 0.02, 0.03, 0.04],
    )

    result = downside_deviation(
        returns,
    )

    assert result == 0.0


def test_zero_drawdown_calmar():
    returns = pd.Series(
        [0.01, 0.02, 0.03, 0.04],
    )

    with pytest.raises(ValueError):
        calmar_ratio(
            returns,
        )
