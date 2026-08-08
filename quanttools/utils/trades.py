"""
quanttools.utils.trades
=======================

Shared utilities for trade statistics.
"""

from __future__ import annotations

import pandas as pd


def split_trades(
    trade_results: pd.Series,
) -> tuple[pd.Series, pd.Series]:
    """
    Split trade results into winners and losers.

    Parameters
    ----------
    trade_results : pandas.Series
        Profit and loss values.

    Returns
    -------
    tuple[pandas.Series, pandas.Series]
        Winning trades and losing trades.
    """

    winning_trades = trade_results[
        trade_results > 0
    ]

    losing_trades = trade_results[
        trade_results < 0
    ]

    return (
        winning_trades,
        losing_trades,
    )