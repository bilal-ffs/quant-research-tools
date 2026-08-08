"""
quanttools.statistics.sortino
============================

Functions for calculating the Sortino Ratio.

References
----------
- Frank Sortino (1980)
"""

from __future__ import annotations

import pandas as pd

from quanttools.utils.validation import (
    validate_returns,
)


def sortino_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Calculate the annualized Sortino ratio.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    risk_free_rate : float, default=0.0
        Annual risk-free rate expressed as a decimal.

    periods_per_year : int, default=252
        Number of return observations per year.

    Returns
    -------
    float
        Annualized Sortino ratio.
    """

    # Step 1: Validate input

    returns = validate_returns(returns)

    # Step 2: Compute excess returns

    periodic_risk_free_rate = risk_free_rate / periods_per_year

    excess_returns = returns - periodic_risk_free_rate

    # Step 3: Keep only downside returns

    downside_returns = excess_returns[excess_returns < 0]

    # Step 4: Compute downside deviation

    downside_deviation = downside_returns.std(ddof=1)
    # Step 5: Validate downside deviation

    if downside_returns.empty or pd.isna(downside_deviation) or downside_deviation == 0:
        raise ValueError("downside deviation is zero.")

    # Step 6: Compute annualized Sortino Ratio

    mean_return = excess_returns.mean()

    sortino = (mean_return / downside_deviation) * (periods_per_year**0.5)

    return float(sortino)
