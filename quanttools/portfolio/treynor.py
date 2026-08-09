"""
quanttools.portfolio.treynor
============================

Functions for calculating the Treynor ratio.
"""

from __future__ import annotations

import pandas as pd

from quanttools.portfolio.beta import (
    beta,
)
from quanttools.utils.validation import (
    validate_return_pair,
)


def treynor_ratio(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
    risk_free_rate: float = 0.0,
) -> float:
    """
    Calculate the Treynor ratio.

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
        Treynor ratio.
    """
    portfolio_returns, benchmark_returns = validate_return_pair(
        portfolio_returns,
        benchmark_returns,
    )

    beta_value = beta(
        portfolio_returns,
        benchmark_returns,
    )

    if beta_value == 0:
        raise ValueError("beta is zero.")

    portfolio_return = portfolio_returns.mean()

    return float((portfolio_return - risk_free_rate) / beta_value)
