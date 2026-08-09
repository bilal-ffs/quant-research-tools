"""
quanttools.portfolio.active_return
==================================

Functions for calculating active return.
"""

from __future__ import annotations

import pandas as pd

from quanttools.utils.validation import (
    validate_return_pair,
)


def active_return(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> float:
    """
    Calculate active return.

    Parameters
    ----------
    portfolio_returns : pandas.Series
        Portfolio periodic returns.

    benchmark_returns : pandas.Series
        Benchmark periodic returns.

    Returns
    -------
    float
        Active return.
    """

    portfolio_returns, benchmark_returns = validate_return_pair(
        portfolio_returns,
        benchmark_returns,
    )

    return float(portfolio_returns.mean() - benchmark_returns.mean())
