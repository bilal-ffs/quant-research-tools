## Example

```python
import pandas as pd

from quanttools.reports import performance_report

returns = pd.Series([...])

trade_results = pd.Series([...])

print(
    performance_report(
        returns,
        trade_results,
    )
)
```
## Risk Analytics

### Risk Metrics

```python
from quanttools.risk import (
    volatility,
    downside_deviation,
    value_at_risk,
    conditional_value_at_risk,
    ulcer_index,
)
## Complete Analysis

The `complete_analysis.py` example demonstrates how QuantTools can combine:

- Risk analytics
- Portfolio analytics
- Backtest analysis
- Performance reporting

Run:

```bash
python examples/complete_analysis.py

## Recovery and bootstrap robustness

From the repository root, run `python -m examples.robustness_analysis`.
This synthetic monthly-data example shows configurable annualization,
label-preserving recovery episodes, an unrecovered drawdown, reproducible IID
and moving-block summaries, per-metric valid counts and ending-loss probability.
It does not download data or compound cash trade P&L.
