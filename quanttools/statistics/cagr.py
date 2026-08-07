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

    returns = validate_returns(
        returns
    )
    # Step 2: Compute cumulative equity curve

    growth_factor = 1 + returns

    equity_curve = growth_factor.cumprod(
        
    )
    # Step 3: Compute investment duration

    periods = len(returns)

    years = periods / periods_per_year