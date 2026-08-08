"""
quanttools.backtest.backtest
============================

Backtest object for quantitative strategy analysis.
"""

from __future__ import annotations

import pandas as pd

from quanttools.reports import (
    performance_report,
)
from quanttools.statistics import (
    average_loss,
    average_win,
    cagr,
    calmar_ratio,
    drawdown_duration,
    expectancy,
    max_drawdown,
    payoff_ratio,
    profit_factor,
    sharpe_ratio,
    sortino_ratio,
    win_rate,
)


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

    def report(self) -> str:
        """
        Generate a performance report.
        """

        return performance_report(
            self.returns,
            self.trade_results,
        )

    def sharpe_ratio(self) -> float:
        """
        Calculate the Sharpe ratio.
        """

        return sharpe_ratio(
            self.returns,
        )

    def sortino_ratio(self) -> float:
        """
        Calculate the Sortino ratio.
        """

        return sortino_ratio(
            self.returns,
        )

    def cagr(self) -> float:
        """
        Calculate the CAGR.
        """

        return cagr(
            self.returns,
        )

    def calmar_ratio(self) -> float:
        """
        Calculate the Calmar ratio.
        """

        return calmar_ratio(
            self.returns,
        )

    def max_drawdown(self) -> float:
        """
        Calculate the maximum drawdown.
        """

        return max_drawdown(
            self.returns,
        )

    def drawdown_duration(self) -> int:
        """
        Calculate the longest drawdown duration.
        """

        return drawdown_duration(
            self.returns,
        )

    def profit_factor(self) -> float:
        """
        Calculate the profit factor.
        """

        return profit_factor(
            self.trade_results,
        )

    def expectancy(self) -> float:
        """
        Calculate expectancy.
        """

        return expectancy(
            self.trade_results,
        )

    def win_rate(self) -> float:
        """
        Calculate the win rate.
        """

        return win_rate(
            self.trade_results,
        )

    def average_win(self) -> float:
        """
        Calculate the average winning trade.
        """

        return average_win(
            self.trade_results,
        )

    def average_loss(self) -> float:
        """
        Calculate the average losing trade.
        """

        return average_loss(
            self.trade_results,
        )

    def payoff_ratio(self) -> float:
        """
        Calculate the payoff ratio.
        """

        return payoff_ratio(
            self.trade_results,
        )
