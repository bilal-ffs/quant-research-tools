"""
quanttools.risk.volatility
==========================

Functions for calculating return volatility.
"""

from __future__ import annotations

import pandas as pd

from quanttools.utils.validation import (
    validate_returns,
)


def volatility(
    returns: pd.Series,
    periods_per_year: int = 252,
) -> float:
    """
    Calculate annualized volatility.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    periods_per_year : int, default=252
        Number of periods in one year.

    Returns
    -------
    float
        Annualized volatility.
    """

    returns = validate_returns(
        returns,
    )

    volatility_value = returns.std(ddof=1) * periods_per_year**0.5

    return float(
        volatility_value,
    )
