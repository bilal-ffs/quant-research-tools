"""
quanttools.statistics.average_loss
==================================

Functions for calculating the Average Losing Trade.

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


def average_loss(
    trade_results: pd.Series,
) -> float:
    """
    Calculate the average losing trade.

    Parameters
    ----------
    trade_results : pandas.Series
        Profit and loss values for completed trades.

    Returns
    -------
    float
        Average losing trade value expressed as a
        positive number.

    Raises
    ------
    TypeError
        If trade_results is not a pandas Series.

    ValueError
        If trade_results is empty, contains only
        missing values, or contains no losing
        trades.
    """

    # Step 1: Validate input

    trade_results = validate_trade_results(trade_results)

    # Step 2: Separate winning and losing trades

    _, losing_trades = split_trades(trade_results)

    # Step 3: Validate losing trades

    if losing_trades.empty:
        raise ValueError("no losing trades.")

    # Step 4: Compute average losing trade

    return float(abs(losing_trades.mean()))
