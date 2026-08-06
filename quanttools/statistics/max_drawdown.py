"""
quanttools.statistics.max_drawdown
=================================

Functions for calculating drawdown-related performance metrics.

Description
-----------
Provides reusable utilities for measuring portfolio drawdowns from a
series of periodic returns.

Functions
---------
- drawdown_series
- max_drawdown
- drawdown_duration
- recovery_time

References
----------
- Magdon-Ismail, M., & Atiya, A. (2004)
- Quantopian Empyrical Library
"""

from __future__ import annotations

import pandas as pd

def drawdown_series(
    returns: pd.Series,
) -> pd.Series:
    """
    Calculate the drawdown series.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns expressed as decimal values.

    Returns
    -------
    pandas.Series
        Drawdown values for every observation.

    Raises
    ------
    TypeError
        If returns is not a pandas Series.

    ValueError
        If returns is empty.

    Examples
    --------
    >>> drawdown_series(returns)

    Notes
    -----
    Drawdown is measured relative to the running equity peak.
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

    # Step 2: Remove missing values

    returns = returns.dropna()

    if returns.empty:
        raise ValueError(
            "returns contains only missing values."
        )

    # Step 3: Compute cumulative equity curve

    growth_factor = 1 + returns

    equity_curve = growth_factor.cumprod()

    # Step 4: Compute running equity peak

    running_peak = equity_curve.cummax()

    # Step 5: Compute drawdown series

    drawdown = (equity_curve / running_peak) - 1

    return drawdown

def max_drawdown(
    returns: pd.Series,
) -> float:
    """
    Calculate the maximum drawdown.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns expressed as decimal values.

    Returns
    -------
    float
        Largest drawdown expressed as a negative decimal.

    Raises
    ------
    TypeError
        If returns is not a pandas Series.

    ValueError
        If returns is empty.

    Examples
    --------
    >>> max_drawdown(returns)
    -0.25
    """
    drawdown = drawdown_series(returns)

    return float(drawdown.min())

def drawdown_duration(
    returns: pd.Series,
) -> int:
    """
    Calculate the longest drawdown duration.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    Returns
    -------
    int
        Maximum number of consecutive periods spent below the previous equity peak.
    """
    raise NotImplementedError

def recovery_time(
    returns: pd.Series,
) -> int:
    """
    Calculate the recovery time after the maximum drawdown.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    Returns
    -------
    int
        Number of periods required to recover from the maximum drawdown.
    """
    raise NotImplementedError

