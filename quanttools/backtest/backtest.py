"""
quanttools.backtest.backtest
============================

Backtest object for quantitative strategy analysis.
"""

from __future__ import annotations

import pandas as pd


class Backtest:
    """
    Quantitative backtest object.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    trade_results : pandas.Series
        Profit and loss values for completed trades.
    """

    def __init__(
        self,
        returns: pd.Series,
        trade_results: pd.Series,
    ) -> None:

        self.returns = returns

        self.trade_results = trade_results