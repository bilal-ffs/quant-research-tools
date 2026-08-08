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

from quanttools.utils.validation import (
    validate_returns,
)


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
    returns = validate_returns(returns)

    # Step 2: Compute cumulative equity curve

    growth_factor = 1 + returns

    equity_curve = growth_factor.cumprod()

    # Step 3: Compute running equity peak

    running_peak = equity_curve.cummax()

    # Step 4: Compute drawdown series

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
        Periodic returns expressed as decimal values.

    Returns
    -------
    int
        Maximum number of consecutive periods spent below the
        previous equity peak.

    Raises
    ------
    TypeError
        If returns is not a pandas Series.

    ValueError
        If returns is empty.

    Examples
    --------
    >>> drawdown_duration(returns)
    15

    Notes
    -----
    A drawdown period begins when the equity curve falls below
    its previous peak and ends once a new peak is reached.
    """
    # Step 1: Compute drawdown series

    drawdown = drawdown_series(returns)

    # Step 2: Initialize counters

    longest_duration = 0
    current_duration = 0

    # Step 3: Iterate through the drawdown series

    for value in drawdown:
        if value < 0:
            current_duration += 1
        else:
            longest_duration = max(
                longest_duration,
                current_duration,
            )
            current_duration = 0

    # Step 4: Handle drawdowns that continue until the final observation

    longest_duration = max(
        longest_duration,
        current_duration,
    )

    return longest_duration


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
