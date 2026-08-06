import pandas as pd

from quanttools.statistics.max_drawdown import drawdown_series

returns = pd.Series(
    [
        0.10,
        -0.05,
        0.02,
        -0.08,
        0.03,
    ]
)

print(drawdown_series(returns))
