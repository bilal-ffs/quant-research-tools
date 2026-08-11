# Backtest API

The `Backtest` object provides a unified interface for analyzing periodic returns and completed trade results.

## Creating a Backtest

```python
import pandas as pd

from quanttools import Backtest

returns = pd.Series([...])

trade_results = pd.Series([...])

bt = Backtest(
    returns,
    trade_results,
)
