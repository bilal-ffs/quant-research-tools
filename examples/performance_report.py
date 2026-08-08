import pandas as pd

from quanttools.reports import (
    performance_report,
)

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

print(
    performance_report(
        returns,
        trade_results,
    )
)
