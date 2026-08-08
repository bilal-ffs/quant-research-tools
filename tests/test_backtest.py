import pandas as pd

from quanttools import (
    Backtest,
)


def create_backtest() -> Backtest:
    returns = pd.Series(
        [
            0.02,
            -0.01,
            0.03,
            -0.02,
            0.01,
            0.015,
        ]
    )

    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
            50,
            -40,
        ]
    )

    return Backtest(
        returns,
        trade_results,
    )


def test_report_returns_string():
    bt = create_backtest()

    assert isinstance(
        bt.report(),
        str,
    )


def test_sharpe_ratio_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.sharpe_ratio(),
        float,
    )


def test_sortino_ratio_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.sortino_ratio(),
        float,
    )


def test_cagr_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.cagr(),
        float,
    )


def test_calmar_ratio_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.calmar_ratio(),
        float,
    )


def test_max_drawdown_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.max_drawdown(),
        float,
    )


def test_drawdown_duration_returns_int():
    bt = create_backtest()

    assert isinstance(
        bt.drawdown_duration(),
        int,
    )


def test_profit_factor_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.profit_factor(),
        float,
    )


def test_expectancy_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.expectancy(),
        float,
    )


def test_win_rate_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.win_rate(),
        float,
    )


def test_average_win_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.average_win(),
        float,
    )


def test_average_loss_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.average_loss(),
        float,
    )


def test_payoff_ratio_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.payoff_ratio(),
        float,
    )
