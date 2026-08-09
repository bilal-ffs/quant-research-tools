"""
quanttools.portfolio.information_ratio
======================================

Functions for calculating the information ratio.
"""

from __future__ import annotations

import pandas as pd


def information_ratio(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """
    Calculate the information ratio.

    Parameters
    ----------
    portfolio_returns : pandas.Series
        Portfolio periodic returns.

    benchmark_returns : pandas.Series
        Benchmark periodic returns.

    Returns
    -------
    float
        Information ratio.
    """

    from quanttools.portfolio.tracking_error import (
        tracking_error,
    )
    from quanttools.utils.validation import (
        validate_return_pair,
    )

    portfolio_returns, benchmark_returns = validate_return_pair(
        portfolio_returns,
        benchmark_returns,
    )

    active_return = portfolio_returns.mean() - benchmark_returns.mean()

    te = tracking_error(
        portfolio_returns,
        benchmark_returns,
    )

    if te == 0:
        raise ValueError("tracking error is zero.")

    return float(active_return / te)
