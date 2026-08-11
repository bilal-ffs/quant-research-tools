"""
quanttools.portfolio.beta
=========================

Functions for calculating portfolio beta.
"""

from __future__ import annotations

import pandas as pd

from quanttools.utils.validation import (
    validate_return_pair,
)


def beta(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """
    Calculate portfolio beta relative to a benchmark.

    Parameters
    ----------
    portfolio_returns : pandas.Series
        Portfolio periodic returns.

    benchmark_returns : pandas.Series
        Benchmark periodic returns.

    Returns
    -------
    float
        Portfolio beta.
    """

    if len(portfolio_returns) < 2:
        raise ValueError("at least two observations are required.")

    portfolio_returns, benchmark_returns = validate_return_pair(
        portfolio_returns,
        benchmark_returns,
    )

    covariance = portfolio_returns.cov(
        benchmark_returns,
    )

    variance = benchmark_returns.var()

    if pd.isna(covariance):
        raise ValueError("covariance could not be computed.")

    if pd.isna(variance) or variance == 0:
        raise ValueError("benchmark variance is zero.")

    return float(covariance / variance)
