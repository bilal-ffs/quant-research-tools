"""
quanttools.portfolio.alpha
==========================

Functions for calculating portfolio alpha.
"""

from __future__ import annotations

import pandas as pd

from quanttools.portfolio.beta import (
    beta,
)
from quanttools.utils.validation import (
    validate_return_pair,
)


def alpha(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
    risk_free_rate: float = 0.0,
) -> float:
    """
    Calculate portfolio alpha.

    Parameters
    ----------
    portfolio_returns : pandas.Series
        Portfolio periodic returns.

    benchmark_returns : pandas.Series
        Benchmark periodic returns.

    risk_free_rate : float, default=0.0
        Risk-free rate expressed as a decimal.

    Returns
    -------
    float
        Portfolio alpha.
    """

    portfolio_returns, benchmark_returns = validate_return_pair(
        portfolio_returns,
        benchmark_returns,
    )

    beta_value = beta(
        portfolio_returns,
        benchmark_returns,
    )

    portfolio_mean = portfolio_returns.mean()

    benchmark_mean = benchmark_returns.mean()

    alpha_value = (
        portfolio_mean - risk_free_rate - beta_value * (benchmark_mean - risk_free_rate)
    )

    return float(
        alpha_value,
    )
