"""
quanttools.portfolio.information_ratio
======================================

Functions for calculating the information ratio.
"""

from __future__ import annotations

import pandas as pd

from quanttools.utils.validation import (
        validate_return_pair,
    )

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