"""
quanttools.statistics.payoff_ratio
==================================

Functions for calculating the Payoff Ratio.

References
----------
Van K. Tharp
"""

from __future__ import annotations

import pandas as pd

from quanttools.statistics.average_loss import (
    average_loss,
)
from quanttools.statistics.average_win import (
    average_win,
)


def payoff_ratio(
    trade_results: pd.Series,
) -> float:
    """
    Calculate the payoff ratio.

    Parameters
    ----------
    trade_results : pandas.Series
        Profit and loss values for completed trades.

    Returns
    -------
    float
        Ratio of average winning trade to
        average losing trade.
    """

    # Step 1: Compute average winning trade

    avg_win = average_win(trade_results)

    # Step 2: Compute average losing trade

    avg_loss = average_loss(trade_results)

    # Step 3: Compute payoff ratio

    return float(avg_win / avg_loss)
