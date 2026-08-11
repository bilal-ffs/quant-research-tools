import pandas as pd

from quanttools.risk import (
    conditional_value_at_risk,
    downside_deviation,
    ulcer_index,
    value_at_risk,
    volatility,
)

returns = pd.Series(
    [
        0.012,
        -0.008,
        0.015,
        -0.021,
        0.007,
        -0.013,
        0.018,
        -0.004,
        0.011,
        -0.009,
    ]
)

print(
    "Volatility:",
    volatility(returns),
)

print(
    "Downside Deviation:",
    downside_deviation(returns),
)

print(
    "VaR (95%):",
    value_at_risk(
        returns,
        confidence_level=0.95,
    ),
)

print(
    "CVaR (95%):",
    conditional_value_at_risk(
        returns,
        confidence_level=0.95,
    ),
)

print(
    "Ulcer Index:",
    ulcer_index(returns),
)