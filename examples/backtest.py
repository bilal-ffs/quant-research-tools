import pandas as pd

from quanttools import Backtest

returns = pd.Series(
    [
        0.02,
        -0.01,
        0.03,
        -0.02,
        0.01,
    ]
)

trade_results = pd.Series(
    [
        100,
        -50,
        75,
        -25,
        50,
    ]
)

bt = Backtest(
    returns,
    trade_results,
)

print(bt.summary())
print(bt.report())
