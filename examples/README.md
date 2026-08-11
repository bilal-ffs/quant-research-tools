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