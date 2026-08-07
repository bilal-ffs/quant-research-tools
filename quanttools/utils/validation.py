"""
quanttools.utils.validation
===========================

Shared validation utilities.
"""

from __future__ import annotations

import pandas as pd


def validate_returns(
    returns: pd.Series,
) -> pd.Series:
    """
    Validate a return series.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    Returns
    -------
    pandas.Series
        Return series with missing values removed.

    Raises
    ------
    TypeError
        If returns is not a pandas Series.

    ValueError
        If returns is empty or contains only missing values.
    """

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

    return returns