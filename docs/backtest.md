# Backtest API

The `Backtest` object provides a unified interface for analyzing periodic strategy returns and completed trade results.

It combines the statistical metrics available in QuantTools with reporting and export functionality.

---

## Creating a Backtest

A `Backtest` requires two `pandas.Series` objects:

- `returns` — periodic strategy returns.
- `trade_results` — profit and loss values for completed trades.

```python
import pandas as pd

from quanttools import Backtest

returns = pd.Series([
    0.012,
    -0.008,
    0.015,
    -0.021,
    0.007,
])

trade_results = pd.Series([
    120.0,
    -50.0,
    85.0,
    -30.0,
])

bt = Backtest(
    returns,
    trade_results,
)
```

---

## Summary

The summary provides a structured representation of the backtest performance.

```python
summary = bt.summary()

print(summary)
```

Use the summary when you want to access the backtest results programmatically rather than only displaying a formatted report.

---

## Performance Report

The `report()` method generates a formatted performance report containing performance, risk, and trade analytics.

```python
print(
    bt.report(),
)
```

The report includes metrics such as:

### Performance

- CAGR
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio

### Risk

- Maximum Drawdown
- Drawdown Duration

### Trade Analytics

- Profit Factor
- Expectancy
- Win Rate
- Average Win
- Average Loss
- Payoff Ratio

---

## DataFrame Export

The backtest results can be converted into a pandas DataFrame.

```python
df = bt.to_dataframe()

print(df)
```

This is useful when further analysis is required using pandas.

For example:

```python
df.to_excel(
    "backtest_results.xlsx",
)
```

---

## JSON Export

Results can also be exported as JSON.

```python
json_data = bt.to_json()

print(json_data)
```

JSON output is useful when passing backtest results to other applications or APIs.

---

## CSV Export

Backtest results can be written directly to a CSV file.

```python
bt.to_csv(
    "backtest_results.csv",
)
```

The resulting file can be opened with spreadsheet software or imported into other research workflows.

---

## Complete Backtest Workflow

A typical workflow looks like:

```python
import pandas as pd

from quanttools import Backtest

returns = pd.Series([
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
])

trade_results = pd.Series([
    120.0,
    -50.0,
    85.0,
    -30.0,
    150.0,
    -40.0,
    95.0,
])

bt = Backtest(
    returns,
    trade_results,
)

# Human-readable report
print(
    bt.report(),
)

# Structured results
summary = bt.summary()

# DataFrame
df = bt.to_dataframe()

# JSON
json_data = bt.to_json()

# CSV
bt.to_csv(
    "backtest_results.csv",
)
```

---

## Backtest Workflow

The `Backtest` API is designed to provide a simple interface between raw strategy results and quantitative analysis:

```text
Strategy
   │
   ▼
Periodic Returns
   │
   ├───────────────┐
   │               │
   ▼               ▼
Performance     Risk
Metrics         Metrics
   │               │
   └───────┬───────┘
           │
           ▼
       Backtest
           │
           ├── Summary
           ├── Report
           ├── DataFrame
           ├── JSON
           └── CSV
```

This allows strategy research to remain focused on the strategy itself while QuantTools handles the analysis and presentation of its results.