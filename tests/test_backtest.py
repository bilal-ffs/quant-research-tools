import pandas as pd

from quanttools.backtest.backtest import (
    Backtest,
)


def test_sharpe_method_returns_float():
    returns = pd.Series(
        [
            0.01,
            -0.02,
            0.03,
            0.01,
        ]
    )

    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
        ]
    )

    bt = Backtest(
        returns,
        trade_results,
    )

    result = bt.sharpe_ratio()

    assert isinstance(result, float)
