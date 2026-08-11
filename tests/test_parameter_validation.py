import pandas as pd
import pytest

from quanttools.risk import (
    volatility,
)
from quanttools.statistics import (
    sharpe_ratio,
    sortino_ratio,
)


def test_volatility_zero_periods_per_year():
    returns = pd.Series(
        [0.01, -0.02, 0.03],
    )

    with pytest.raises(ValueError):
        volatility(
            returns,
            periods_per_year=0,
        )


def test_volatility_negative_periods_per_year():
    returns = pd.Series(
        [0.01, -0.02, 0.03],
    )

    with pytest.raises(ValueError):
        volatility(
            returns,
            periods_per_year=-252,
        )


def test_sharpe_zero_periods_per_year():
    returns = pd.Series(
        [0.01, -0.02, 0.03],
    )

    with pytest.raises(ValueError):
        sharpe_ratio(
            returns,
            periods_per_year=0,
        )


def test_sortino_zero_periods_per_year():
    returns = pd.Series(
        [0.01, -0.02, 0.03],
    )

    with pytest.raises(ValueError):
        sortino_ratio(
            returns,
            periods_per_year=0,
        )
