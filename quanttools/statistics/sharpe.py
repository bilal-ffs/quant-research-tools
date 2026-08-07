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

    if not isinstance(returns, pd.Series):
        raise TypeError(
            "returns must be a pandas Series."
        )

    if returns.empty:
        raise ValueError(
            "returns cannot be empty."
        )

    returns = returns.dropna()

    if returns.empty:
        raise ValueError(
            "returns contains only missing values."
        )
