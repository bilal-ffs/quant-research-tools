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
## Object-Oriented API

```python
from quanttools import Backtest

bt = Backtest(
    returns,
    trade_results,
)

print(bt.summary())
print(bt.report())

df = bt.to_dataframe()
json_data = bt.to_json()
bt.to_csv("metrics.csv")
```## Object-Oriented API

```python
from quanttools import Backtest

bt = Backtest(
    returns,
    trade_results,
)

print(bt.summary())
print(bt.report())

df = bt.to_dataframe()
json_data = bt.to_json()
bt.to_csv("metrics.csv")
```