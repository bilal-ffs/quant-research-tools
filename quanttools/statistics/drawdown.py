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
    compounded_equity,
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
    Drawdown uses starting equity 1.0 as the initial peak. Missing returns
    are removed; the remaining labels and order are preserved.
    """
    # Step 1: Validate input
    returns = validate_returns(returns)

    # Step 2: Compute cumulative equity curve

    equity_curve = compounded_equity(returns)

    # Step 3: Compute running equity peak

    running_peak = equity_curve.cummax().clip(lower=1.0)

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
    its previous peak and ends once that peak is reached or exceeded.
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


def drawdown_episodes(returns: pd.Series) -> pd.DataFrame:
    """Describe each drawdown in observation counts, retaining input labels.

    The initial peak has label None and position -1. Recovery is equity >=
    the prior peak. Underwater duration counts strictly underwater observations
    (excluding recovery); an open episode's count is its observed age.
    Trough-to-recovery duration is nullable for open episodes. Tied troughs use
    the first minimum; equal peaks reset the peak position to the latest label.
    """
    returns = validate_returns(returns)
    equity = compounded_equity(returns)
    rows = []
    peak_value, peak_position = 1.0, -1
    trough_position = None
    trough_value = None

    def append_episode(recovery_position):
        recovered = recovery_position is not None
        end = recovery_position if recovered else len(equity)
        rows.append(
            {
                "peak": None if peak_position == -1 else equity.index[peak_position],
                "trough": equity.index[trough_position],
                "recovery": equity.index[recovery_position] if recovered else None,
                "peak_position": peak_position,
                "trough_position": trough_position,
                "recovery_position": recovery_position,
                "depth": trough_value / peak_value - 1,
                "underwater_duration": end - peak_position - 1,
                "trough_to_recovery_duration": (
                    recovery_position - trough_position if recovered else None
                ),
                "recovered": recovered,
            }
        )

    for position, value in enumerate(equity):
        if value >= peak_value:
            if trough_position is not None:
                append_episode(position)
            peak_value, peak_position = value, position
            trough_position = trough_value = None
        elif trough_position is None or value < trough_value:
            trough_position, trough_value = position, value
    if trough_position is not None:
        append_episode(None)
    columns = [
        "peak",
        "trough",
        "recovery",
        "peak_position",
        "trough_position",
        "recovery_position",
        "depth",
        "underwater_duration",
        "trough_to_recovery_duration",
        "recovered",
    ]
    result = pd.DataFrame(rows, columns=columns)
    # Preserve exact labels, including integer IDs that float coercion would lose.
    for column in ["peak", "trough", "recovery"]:
        result[column] = pd.Series([row[column] for row in rows], dtype=object)
    result["depth"] = result["depth"].astype(float)
    result["recovered"] = result["recovered"].astype(bool)
    for column in [
        "peak_position",
        "trough_position",
        "recovery_position",
        "underwater_duration",
        "trough_to_recovery_duration",
    ]:
        result[column] = result[column].astype("Int64")
    return result


def recovery_time(returns: pd.Series) -> int | None:
    """Trough-to-recovery count for the deepest episode, or None if open.

    Return 0 if there is no drawdown. Equal-depth episodes select the first.
    An unfinished episode's age is never reported as completed recovery time.
    """
    episodes = drawdown_episodes(returns)
    if episodes.empty:
        return 0
    episode = episodes.loc[episodes["depth"].idxmin()]
    duration = episode["trough_to_recovery_duration"]
    return None if pd.isna(duration) else int(duration)
