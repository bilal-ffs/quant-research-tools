"""
quanttools.statistics.cagr
==========================

Functions for calculating Compound Annual Growth Rate (CAGR).

References
----------
- CFA Institute
"""

from __future__ import annotations

import pandas as pd

from quanttools.utils.validation import (
    compounded_equity,
    validate_finite,
    validate_periods_per_year,
    validate_returns,
)


def cagr(
    returns: pd.Series,
    periods_per_year: int = 252,
) -> float:
    """
    Calculate the Compound Annual Growth Rate.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    periods_per_year : int, default=252
        Number of observations per year.

    Returns
    -------
    float
        Annualized compound growth rate.
    """

    # Step 1: Validate input

    returns = validate_returns(returns)
    validate_periods_per_year(periods_per_year)
    # Step 2: Compute cumulative equity curve

    equity_curve = compounded_equity(returns)
    # Step 3: Compute investment duration

    periods = len(returns)

    years = periods / periods_per_year

    # Step 4: Compute CAGR

    ending_value = equity_curve.iloc[-1]

    cagr = (ending_value ** (1 / years)) - 1

    validate_finite(cagr, "CAGR")
    return float(cagr)
