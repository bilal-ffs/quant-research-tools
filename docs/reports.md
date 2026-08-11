# Reports

Quant Research Tools provides formatted performance reporting through `performance_report()` and the `Backtest.report()` method.

## Performance Report

```python
from quanttools.reports import (
    performance_report,
)

report = performance_report(
    returns,
    trade_results,
)

print(report)