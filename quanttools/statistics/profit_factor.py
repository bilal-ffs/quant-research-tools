"""
quanttools.statistics.profit_factor
==================================

Functions for calculating Profit Factor.

References
----------
Van K. Tharp
"""

from __future__ import annotations

import pandas as pd

from quanttools.utils.validation import (
    validate_trade_results,
)

from quanttools.utils.trades import (
    split_trades,
)


def profit_factor(
    trade_results: pd.Series,
) -> float:
    """
    Calculate the Profit Factor.

    Parameters
    ----------
    trade_results : pandas.Series
        Profit and loss values for completed trades.

    Returns
    -------
    float
        Profit Factor.

    Raises
    ------
    TypeError
        If trade_results is not a pandas Series.

    ValueError
        If trade_results is empty.

    Examples
    --------
    >>> profit_factor(trade_results)
    1.85
    """

    # Step 1: Validate input

    trade_results = validate_trade_results(trade_results)

    # Step 2: Separate winning and losing trades

    winning_trades, losing_trades = split_trades(trade_results)

    # Step 3: Compute gross profit and gross loss

    gross_profit = winning_trades.sum()

    gross_loss = abs(losing_trades.sum())

    # Step 4: Validate gross loss

    if gross_loss == 0:
        raise ValueError("gross loss is zero.")

    # Step 5: Compute Profit Factor

    profit_factor = gross_profit / gross_loss

    return float(profit_factor)
