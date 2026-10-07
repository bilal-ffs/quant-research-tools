# Sharpe Ratio

`sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=252)` calculates
`mean(excess_returns) / std(excess_returns, ddof=1) * sqrt(periods_per_year)`.
The risk-free rate is **annual** and the per-period excess return is
`return - risk_free_rate / periods_per_year`. Arithmetic conversion preserves
the existing convention. Periods per year must be finite and positive.

```python
import pandas as pd
from quanttools.statistics import sharpe_ratio

returns = pd.Series([0.02, -0.03, 0.04, -0.01])
print(sharpe_ratio(returns, risk_free_rate=0.03, periods_per_year=12))
```

Missing observations are removed. Empty samples, nonfinite returns and returns
below -100% are rejected. One observation or constant returns produce an
undefined ratio and raise ValueError; bootstrap stores this metric as NaN for
the affected path and reports valid counts. See [input conventions](conventions.md)
and [bootstrap robustness](validation.md).

Reference: William F. Sharpe (1966).
