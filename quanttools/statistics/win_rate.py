"""
quanttools.statistics.win_rate
==============================

Functions for calculating Win Rate.

References
----------
Van K. Tharp
"""

from __future__ import annotations

import pandas as pd


def win_rate(
    trade_results: pd.Series,
) -> float:
    """
    Calculate the winning trade rate.

    Parameters
    ----------
    trade_results : pandas.Series
        Profit and loss values for completed trades.

    Returns
    -------
    float
        Winning trade rate expressed as a decimal.
    """

    # Step 1: Validate input

    trade_results = validate_trade_results(trade_results)

    # Step 2: Separate winning and losing trades

    winning_trades, _ = split_trades(trade_results)

    # Step 3: Compute win rate

    rate = len(winning_trades) / len(trade_results)

    return float(rate)
