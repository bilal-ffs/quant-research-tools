import pandas as pd
import pytest

from quanttools.portfolio import (
    beta,
    information_ratio,
    tracking_error,
)
from quanttools.statistics import (
    sharpe_ratio,
)


def test_single_return_sharpe():
    returns = pd.Series(
        [0.05],
    )

    with pytest.raises(ValueError):
        sharpe_ratio(returns)


def test_single_return_sharpe():
    returns = pd.Series(
        [0.05],
    )

    with pytest.raises(ValueError):
        sharpe_ratio(returns)


def test_single_return_tracking_error():
    portfolio = pd.Series(
        [0.05],
    )

    benchmark = pd.Series(
        [0.03],
    )

    with pytest.raises(ValueError):
        tracking_error(
            portfolio,
            benchmark,
        )


def test_beta_single_observation():
    portfolio = pd.Series(
        [0.05],
    )

    benchmark = pd.Series(
        [0.03],
    )

    with pytest.raises(ValueError):
        beta(
            portfolio,
            benchmark,
        )


def test_information_ratio_single_observation():
    portfolio = pd.Series(
        [0.05],
    )

    benchmark = pd.Series(
        [0.03],
    )

    with pytest.raises(ValueError):
        information_ratio(
            portfolio,
            benchmark,
        )
