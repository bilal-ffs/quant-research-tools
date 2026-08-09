"""
quanttools.portfolio.tracking_error
===================================

Functions for calculating tracking error.
"""

from __future__ import annotations

import pandas as pd


def tracking_error(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """
    Calculate tracking error.

    Parameters
    ----------
    portfolio_returns : pandas.Series
        Portfolio periodic returns.

    benchmark_returns : pandas.Series
        Benchmark periodic returns.

    Returns
    -------
    float
        Tracking error.
    """

    from quanttools.utils.validation import (
        validate_return_pair,
    )

    portfolio_returns, benchmark_returns = validate_return_pair(
        portfolio_returns,
        benchmark_returns,
    )

    active_returns = portfolio_returns - benchmark_returns

    return float(
        active_returns.std(
            ddof=1,
        )
    )
