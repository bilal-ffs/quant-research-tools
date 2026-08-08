"""
quanttools.statistics.expectancy
================================

Functions for calculating trade expectancy.

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


def expectancy(
    trade_results: pd.Series,
) -> float:
    """
    Calculate trade expectancy.

    Parameters
    ----------
    trade_results : pandas.Series
        Profit and loss values for completed trades.

    Returns
    -------
    float
        Expected profit or loss per trade.
    """
    # Step 1: Validate input

    trade_results = validate_trade_results(trade_results)
    # Step 2: Separate winning and losing trades

    winning_trades, losing_trades = split_trades(trade_results)
    # Step 3: Validate winning and losing trades

    if winning_trades.empty:
        raise ValueError("no winning trades.")

    if losing_trades.empty:
        raise ValueError("no losing trades.")
    # Step 4: Compute trade statistics

    win_rate = len(winning_trades) / len(trade_results)

    loss_rate = len(losing_trades) / len(trade_results)

    average_win = winning_trades.mean()

    average_loss = abs(losing_trades.mean())
    # Step 5: Compute expectancy

    expectancy = (win_rate * average_win) - (loss_rate * average_loss)

    return float(expectancy)
