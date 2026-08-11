"""
Complete QuantTools analysis example.

Demonstrates statistics, portfolio analytics,
risk metrics, and backtest reporting.
"""

import pandas as pd

from quanttools.backtest import (
    Backtest,
)
from quanttools.portfolio import (
    active_return,
    alpha,
    beta,
    information_ratio,
    tracking_error,
    treynor_ratio,
)
from quanttools.risk import (
    conditional_value_at_risk,
    downside_deviation,
    ulcer_index,
    value_at_risk,
    volatility,
)

# Example periodic portfolio returns.

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


# Example benchmark returns.

benchmark_returns = pd.Series(
    [
        0.010,
        -0.006,
        0.012,
        -0.015,
        0.006,
        -0.009,
        0.014,
        -0.003,
        0.009,
        -0.007,
    ]
)


# Example completed trade P&L.

trade_results = pd.Series(
    [
        120.0,
        -50.0,
        85.0,
        -30.0,
        150.0,
        -40.0,
        95.0,
    ]
)


# --------------------------------------------------
# Risk Analytics
# --------------------------------------------------

print("Risk Analytics")
print("=" * 50)

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


# --------------------------------------------------
# Portfolio Analytics
# --------------------------------------------------

print()
print("Portfolio Analytics")
print("=" * 50)

print(
    "Beta:",
    beta(
        returns,
        benchmark_returns,
    ),
)

print(
    "Alpha:",
    alpha(
        returns,
        benchmark_returns,
    ),
)

print(
    "Active Return:",
    active_return(
        returns,
        benchmark_returns,
    ),
)

print(
    "Tracking Error:",
    tracking_error(
        returns,
        benchmark_returns,
    ),
)

print(
    "Information Ratio:",
    information_ratio(
        returns,
        benchmark_returns,
    ),
)

print(
    "Treynor Ratio:",
    treynor_ratio(
        returns,
        benchmark_returns,
    ),
)


# --------------------------------------------------
# Backtest
# --------------------------------------------------

backtest = Backtest(
    returns,
    trade_results,
)

print()
print("Backtest Report")
print("=" * 50)

print(
    backtest.report(),
)
