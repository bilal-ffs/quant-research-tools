<p align="center">
  <img src="images/banner.png" width="100%">
</p>

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

# Quant Research Tools

Open-source quantitative finance utilities for systematic trading, portfolio analytics, risk analysis, and financial research.

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

The Backtest API provides:

- Performance summaries
- Human-readable reports
- DataFrame export
- JSON export
- CSV export

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
print(
    "Volatility:",
    volatility(returns),
)

print(
    "VaR:",
    value_at_risk(
        returns,
        confidence_level=0.95,
    ),
)

print(
    "CVaR:",
    conditional_value_at_risk(
        returns,
        confidence_level=0.95,
    ),
)

# Portfolio
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
    "Information Ratio:",
    information_ratio(
        returns,
        benchmark_returns,
    ),
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

For development:

```bash
pip install -r requirements-dev.txt
```

---

# Documentation

Build and serve the documentation locally:

```bash
mkdocs serve
```

Build the documentation in strict mode:

```bash
mkdocs build --strict
```

The documentation covers:

- Statistics
- Portfolio Analytics
- Risk Analytics
- Backtest API
- Reports
- Metric definitions
- Mathematical formulas
- Usage examples
- Research workflows

---

# Running Tests

Run the complete test suite:

```bash
pytest
```

The project uses automated testing to validate:

- Statistical metrics
- Trade analytics
- Portfolio analytics
- Risk metrics
- Backtest functionality
- Input validation
- Edge cases
- Public API stability

Current test suite:

```text
188 tests
```

---

# Code Quality

The project uses:

- **Ruff** for linting
- **Black** for formatting
- **Pytest** for testing
- **MkDocs** for documentation

Before submitting changes:

```bash
ruff check . --fix
black .
pytest
mkdocs build --strict
```

---

# Continuous Integration

GitHub Actions validates the project across:

- Python 3.10
- Python 3.11
- Python 3.12
- Python 3.13

CI checks:

- Black formatting
- Ruff linting
- Pytest
- MkDocs strict documentation build

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

**Latest Release: v1.0.0**

Quant Research Tools v1.0.0 represents the first stable release of the core quantitative research toolkit.

The stable API includes:

- Performance metrics
- Trade analytics
- Portfolio analytics
- Risk analytics
- Backtest functionality
- Reporting functionality

The package is tested across Python 3.10–3.13 and includes automated validation for the public API, edge cases, package installation, and documentation.

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
- Additional quantitative research utilities
- Expanded backtest functionality
- Additional portfolio analytics

Future additions will aim to maintain compatibility with the stable v1.0 API.

---

# Contributing

Contributions are welcome.

Before opening a pull request, make sure:

```bash
ruff check . --fix
black .
pytest
mkdocs build --strict
```

Please open an issue before submitting large architectural changes.

---

# License

MIT License