"""
quanttools.statistics.average_win
=================================

Functions for calculating the Average Winning Trade.

References
----------
Van K. Tharp
"""

from __future__ import annotations

import pandas as pd

from quanttools.utils.trades import (
    split_trades,
)
from quanttools.utils.validation import (
    validate_trade_results,
)


def average_win(
    trade_results: pd.Series,
) -> float:
    """
    Calculate the average winning trade.

    Parameters
    ----------
    trade_results : pandas.Series
        Profit and loss values for completed trades.

    Returns
    -------
    float
        Average winning trade value.

    Raises
    ------
    TypeError
        If trade_results is not a pandas Series.

    ValueError
        If trade_results is empty, contains only
        missing values, or contains no winning
        trades.

    Examples
    --------
    >>> average_win(trade_results)
    125.5
    """

    # Step 1: Validate input

    trade_results = validate_trade_results(trade_results)

    # Step 2: Separate winning and losing trades

    winning_trades, _ = split_trades(trade_results)

    # Step 3: Validate winning trades

    if winning_trades.empty:
        raise ValueError("no winning trades.")

    # Step 4: Compute average winning trade

    return float(winning_trades.mean())
