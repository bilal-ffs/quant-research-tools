# Reports

QuantTools provides formatted performance reports that combine strategy performance, risk, and trade analytics into a single human-readable output.

The main reporting function is `performance_report()`.

The `Backtest.report()` method provides a convenient interface to the same reporting functionality.

---

## Performance Report

### Definition

`performance_report()` generates a formatted report from:

- Periodic strategy returns.
- Completed trade results.

```python
from quanttools.reports import (
    performance_report,
)

report = performance_report(
    returns,
    trade_results,
)

print(report)
```

---

## Report Sections

The performance report is divided into three sections.

### Performance Metrics

The performance section contains:

- CAGR
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio

These metrics describe the strategy's return and risk-adjusted performance.

---

### Risk Metrics

The risk section contains:

- Maximum Drawdown
- Drawdown Duration

These metrics describe the severity and duration of historical drawdowns.

---

### Trade Analytics

The trade analytics section contains:

- Profit Factor
- Expectancy
- Win Rate
- Average Win
- Average Loss
- Payoff Ratio

These metrics describe the characteristics of the completed trade distribution.

---

## Example

```python
import pandas as pd

from quanttools.reports import (
    performance_report,
)

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

report = performance_report(
    returns,
    trade_results,
)

print(report)
```

The resulting report is intended to be directly readable in a terminal, notebook, log, or research workflow.

---

## Backtest Integration

The reporting functionality is also available through the `Backtest` API.

```python
from quanttools import Backtest

bt = Backtest(
    returns,
    trade_results,
)

print(
    bt.report(),
)
```

This provides a convenient workflow:

```text
Strategy Results
       │
       ├── Periodic Returns
       │
       └── Trade Results
               │
               ▼
           Backtest
               │
               ▼
         Performance Report
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
   Performance Risk   Trades
```

---

## Report Output

A typical report is structured as:

```text
==================================================
        QuantTools Performance Report
==================================================

Performance Metrics
--------------------------------------------------
CAGR
Sharpe Ratio
Sortino Ratio
Calmar Ratio

Risk Metrics
--------------------------------------------------
Maximum Drawdown
Drawdown Duration

Trade Analytics
--------------------------------------------------
Profit Factor
Expectancy
Win Rate
Average Win
Average Loss
Payoff Ratio

==================================================
```

The report is returned as a Python string, allowing callers to print it, store it, or incorporate it into a larger research workflow.

---

## When to Use Reports

The reporting API is useful when a compact overview of a backtest is required.

For programmatic analysis, individual metrics can be imported directly:

```python
from quanttools.statistics import (
    cagr,
    sharpe_ratio,
)

cagr_value = cagr(
    returns,
)

sharpe = sharpe_ratio(
    returns,
)
```

For a human-readable summary, use:

```python
report = performance_report(
    returns,
    trade_results,
)
```

The two approaches are complementary:

| Approach | Use Case |
| --- | --- |
| Individual metrics | Programmatic analysis and custom research |
| `performance_report()` | Human-readable performance summary |
| `Backtest.report()` | Reporting directly from a backtest object |