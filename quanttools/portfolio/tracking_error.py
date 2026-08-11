"""
quanttools.portfolio.tracking_error
===================================

Functions for calculating tracking error.
"""

from __future__ import annotations

import pandas as pd

from quanttools.utils.validation import (
    validate_return_pair,
)


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

    Raises
    ------
    ValueError
        If tracking error is zero or undefined.
    """

    portfolio_returns, benchmark_returns = validate_return_pair(
        portfolio_returns,
        benchmark_returns,
    )

    active_returns = portfolio_returns - benchmark_returns

    tracking_error_value = active_returns.std(
        ddof=1,
    )

    if pd.isna(tracking_error_value) or tracking_error_value == 0:
        raise ValueError("tracking error is zero.")

    return float(
        tracking_error_value,
    )
