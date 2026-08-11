<p align="center">
  <img src="images/banner.png" width="100%">
</p>

# Quant Research Tools

Open-source quantitative finance utilities for systematic trading, portfolio analytics, risk analysis, and financial research.

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## Overview

Quant Research Tools is a Python library for quantitative researchers and systematic traders.

The project provides reusable building blocks for:

- Performance analysis
- Trade analytics
- Portfolio analytics
- Risk analysis
- Backtest reporting

The goal is to provide small, composable, well-tested utilities that can be used independently or combined into a complete research workflow.

---

# Features

## Performance Metrics

- ✅ Drawdown Series
- ✅ Maximum Drawdown
- ✅ Drawdown Duration
- ✅ CAGR
- ✅ Sharpe Ratio
- ✅ Sortino Ratio
- ✅ Calmar Ratio

## Trade Analytics

- ✅ Profit Factor
- ✅ Expectancy
- ✅ Win Rate
- ✅ Average Win
- ✅ Average Loss
- ✅ Payoff Ratio

## Portfolio Analytics

- ✅ Beta
- ✅ Alpha
- ✅ Active Return
- ✅ Tracking Error
- ✅ Information Ratio
- ✅ Treynor Ratio

## Risk Analytics

- ✅ Volatility
- ✅ Downside Deviation
- ✅ Historical Value at Risk (VaR)
- ✅ Conditional Value at Risk (CVaR)
- ✅ Ulcer Index

---

# Backtest API

Quant Research Tools provides a `Backtest` object for combining return data and trade results.

```python
import pandas as pd

from quanttools import Backtest

returns = pd.Series([...])

trade_results = pd.Series([...])

bt = Backtest(
    returns,
    trade_results,
)

print(bt.summary())

print(bt.report())

df = bt.to_dataframe()

json_data = bt.to_json()

bt.to_csv("summary.csv")
```

---

# Example

A complete research workflow can combine portfolio and risk analytics with backtest reporting.

```python
import pandas as pd

from quanttools import Backtest
from quanttools.portfolio import (
    alpha,
    beta,
    information_ratio,
)
from quanttools.risk import (
    conditional_value_at_risk,
    value_at_risk,
    volatility,
)

returns = pd.Series([...])

benchmark_returns = pd.Series([...])

trade_results = pd.Series([...])

# Risk
print(volatility(returns))

print(
    value_at_risk(
        returns,
        confidence_level=0.95,
    )
)

print(
    conditional_value_at_risk(
        returns,
        confidence_level=0.95,
    )
)

# Portfolio
print(
    beta(
        returns,
        benchmark_returns,
    )
)

print(
    alpha(
        returns,
        benchmark_returns,
    )
)

print(
    information_ratio(
        returns,
        benchmark_returns,
    )
)

# Backtest
bt = Backtest(
    returns,
    trade_results,
)

print(bt.report())
```

For a complete runnable example, see:

```text
examples/complete_analysis.py
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/bilal-ffs/quant-research-tools.git

cd quant-research-tools
```

Install in editable mode:

```bash
pip install -e .
```

---

# Running Tests

Run the complete test suite:

```bash
pytest
```

The project uses automated testing to validate the statistical, portfolio, risk, reporting, and backtest functionality.

---

# Code Quality

The project uses:

- **Ruff** for linting
- **Black** for formatting
- **Pytest** for testing

Before submitting changes:

```bash
ruff check . --fix
black .
pytest
```

---

# Project Structure

```text
quant-research-tools/
│
├── quanttools/
│   ├── statistics/
│   ├── portfolio/
│   ├── risk/
│   ├── reports/
│   ├── backtest/
│   └── utils/
│
├── tests/
├── docs/
├── examples/
└── notebooks/
```

---

# Current Version

**Latest Release: v0.8.0**

### Release Highlights

**v0.8.0 — Risk Analytics**

- Added Volatility
- Added Downside Deviation
- Added Historical VaR
- Added Conditional VaR / Expected Shortfall
- Added Ulcer Index
- Expanded automated test coverage

---

# Roadmap

## Performance

- Recovery Factor
- Recovery Time

## Portfolio

- Correlation Matrix
- Covariance Matrix

## Future

- Visualization tools
- Additional research utilities
- Expanded backtest functionality

---

# Contributing

Contributions are welcome.

Before opening a pull request, make sure:

```bash
ruff check . --fix
black .
pytest
```

Please open an issue before submitting large architectural changes.

---

# License

MIT License