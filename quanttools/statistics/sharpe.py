"""
quanttools.statistics.sharpe
============================

Functions for calculating the Sharpe Ratio.

References
----------
- William F. Sharpe (1966)
"""

from __future__ import annotations

import pandas as pd


from quanttools.utils.validation import (
    validate_returns,
)


def sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """
    Calculate the annualized Sharpe Ratio.

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
        Annualized Sharpe Ratio.
    """

    # Step 1: Validate input

    returns = validate_returns(returns)
    # Step 2: Compute excess returns

    periodic_risk_free_rate = risk_free_rate / periods_per_year

    excess_returns = returns - periodic_risk_free_rate
    # Step 3: Compute mean return and volatility

    mean_return = excess_returns.mean()

    volatility = excess_returns.std(ddof=1)

    # Step 4: Validate volatility

    if volatility == 0:
        raise ValueError("standard deviation is zero.")
    # Step 5: Compute annualized Sharpe Ratio

    sharpe = (mean_return / volatility) * (periods_per_year**0.5)

    return float(sharpe)
