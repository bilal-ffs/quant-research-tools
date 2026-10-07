"""
quanttools.backtest.backtest
============================

Backtest object for quantitative strategy analysis.
"""

from __future__ import annotations

import json

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
from quanttools.utils.validation import (
    validate_finite,
    validate_periods_per_year,
    validate_returns,
    validate_trade_results,
)
from quanttools.validation import BootstrapResult, iid_bootstrap, moving_block_bootstrap


class Backtest:
    """
    Quantitative backtest object.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    trade_results : pandas.Series
        Cash profit and loss values for completed trades; not percentage returns.

    periods_per_year : float, default=252
        Positive finite observation frequency, supplied as a keyword argument.

    risk_free_rate : float, default=0.0
        Annual rate, divided by periods_per_year for Sharpe and Sortino.
    """

    def __init__(
        self,
        returns: pd.Series,
        trade_results: pd.Series,
        *,
        periods_per_year: float = 252,
        risk_free_rate: float = 0.0,
    ) -> None:

        validate_periods_per_year(periods_per_year)
        validate_finite(risk_free_rate, "risk_free_rate")
        self.returns = validate_returns(returns)
        self.trade_results = validate_trade_results(trade_results)
        self.periods_per_year = periods_per_year
        self.risk_free_rate = risk_free_rate

    def report(self) -> str:
        """
        Generate a performance report.
        """

        return performance_report(
            self.returns,
            self.trade_results,
            periods_per_year=self.periods_per_year,
            risk_free_rate=self.risk_free_rate,
        )

    def sharpe_ratio(self) -> float:
        """
        Calculate the Sharpe ratio.
        """

        return sharpe_ratio(
            self.returns,
            periods_per_year=self.periods_per_year,
            risk_free_rate=self.risk_free_rate,
        )

    def sortino_ratio(self) -> float:
        """
        Calculate the Sortino ratio.
        """

        return sortino_ratio(
            self.returns,
            periods_per_year=self.periods_per_year,
            risk_free_rate=self.risk_free_rate,
        )

    def cagr(self) -> float:
        """
        Calculate the CAGR.
        """

        return cagr(
            self.returns,
            periods_per_year=self.periods_per_year,
        )

    def calmar_ratio(self) -> float:
        """
        Calculate the Calmar ratio.
        """

        return calmar_ratio(
            self.returns,
            periods_per_year=self.periods_per_year,
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

    def robustness(
        self,
        *,
        method: str = "iid",
        n_simulations: int = 1000,
        horizon: int | None = None,
        block_size: int = 5,
        confidence_level: float = 0.95,
        random_state: int | None = None,
        return_paths: bool = False,
    ) -> BootstrapResult:
        """Opt-in return bootstrap using this backtest's annualization settings.

        method is 'iid' or 'moving_block'. block_size applies only to moving
        blocks. Cash trade P&L is never resampled or compounded here.
        """
        options = dict(
            n_simulations=n_simulations,
            horizon=horizon,
            confidence_level=confidence_level,
            random_state=random_state,
            return_paths=return_paths,
            periods_per_year=self.periods_per_year,
            risk_free_rate=self.risk_free_rate,
        )
        if method == "iid":
            return iid_bootstrap(self.returns, **options)
        if method == "moving_block":
            return moving_block_bootstrap(
                self.returns, block_size=block_size, **options
            )
        raise ValueError("method must be 'iid' or 'moving_block'.")

    def summary(self) -> dict[str, float | int]:
        """
        Return a summary of backtest metrics.

        Returns
        -------
        dict[str, float | int]
            Dictionary containing all performance,
            risk, and trade analytics metrics.
        """

        return {
            "cagr": self.cagr(),
            "sharpe_ratio": self.sharpe_ratio(),
            "sortino_ratio": self.sortino_ratio(),
            "calmar_ratio": self.calmar_ratio(),
            "max_drawdown": self.max_drawdown(),
            "drawdown_duration": self.drawdown_duration(),
            "profit_factor": self.profit_factor(),
            "expectancy": self.expectancy(),
            "win_rate": self.win_rate(),
            "average_win": self.average_win(),
            "average_loss": self.average_loss(),
            "payoff_ratio": self.payoff_ratio(),
        }

    def to_dataframe(self) -> pd.DataFrame:
        """
        Return the backtest summary as a DataFrame.

        Returns
        -------
        pandas.DataFrame
            Summary metrics in tabular format.
        """

        return pd.DataFrame(
            self.summary().items(),
            columns=[
                "Metric",
                "Value",
            ],
        )

    def to_json(self) -> str:
        """
        Return the backtest summary as JSON.

        Returns
        -------
        str
            Summary metrics in JSON format.
        """

        return json.dumps(
            self.summary(),
            indent=4,
        )

    def to_csv(
        self,
        filename: str,
    ) -> None:
        """
        Export the backtest summary to a CSV file.

        Parameters
        ----------
        filename : str
            Output CSV filename.
        """

        self.to_dataframe().to_csv(
            filename,
            index=False,
        )
