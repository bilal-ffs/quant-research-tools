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

from quanttools.utils.trades import (
    split_trades,
)

from quanttools.utils.validation import (
    validate_trade_results,
)


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
    raise NotImplementedError