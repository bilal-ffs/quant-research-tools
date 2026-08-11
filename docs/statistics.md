# Statistics

Statistical performance and trade analytics for quantitative strategies.

---

## Performance Metrics

---

## Drawdown Series

### Definition

Drawdown measures the decline of an equity curve from its previous peak.

QuantTools first constructs the compounded equity curve:

\[
E_t
=
\prod_{i=1}^{t}(1+r_i)
\]

The running peak is:

\[
P_t
=
\max_{i \leq t} E_i
\]

The drawdown at time \(t\) is:

\[
D_t
=
\frac{E_t}{P_t}-1
\]

Drawdowns are expressed as negative values, with `0.0` representing a new equity high.

### Usage

```python
import pandas as pd

from quanttools.statistics import drawdown_series

returns = pd.Series([
    0.05,
    -0.02,
    -0.03,
    0.04,
])

drawdowns = drawdown_series(
    returns,
)

print(drawdowns)
```

---

## Maximum Drawdown

### Definition

Maximum drawdown is the largest peak-to-trough decline experienced by the equity curve.

It is defined as:

\[
MDD
=
\min_t(D_t)
\]

where \(D_t\) is the drawdown series.

QuantTools reports maximum drawdown as a negative value.

For example:

```text
Maximum Drawdown = -0.18
```

represents a maximum decline of **18%** from a previous equity peak.

### Usage

```python
from quanttools.statistics import max_drawdown

result = max_drawdown(
    returns,
)

print(result)
```

---

## Drawdown Duration

### Definition

Drawdown duration measures how long the equity curve remains below its previous peak.

A drawdown period begins when the equity curve falls below its previous high and ends when a new high is reached.

### Usage

```python
from quanttools.statistics import drawdown_duration

result = drawdown_duration(
    returns,
)

print(result)
```

The result represents the duration of the drawdown according to the observation frequency of the supplied return series.

---

## CAGR

### Definition

Compound Annual Growth Rate (CAGR) measures the annualized compound growth of a return series.

The general formula is:

\[
CAGR
=
\left(
\frac{V_T}{V_0}
\right)^{\frac{1}{Y}}
-1
\]

where:

- \(V_0\) is the initial value.
- \(V_T\) is the final value.
- \(Y\) is the number of years.

For a periodic return series, the cumulative value is obtained by compounding the returns.

### Usage

```python
from quanttools.statistics import cagr

result = cagr(
    returns,
)

print(result)
```

CAGR is useful when comparing strategies with different cumulative returns over comparable time horizons.

---

## Sharpe Ratio

### Definition

The Sharpe Ratio measures excess return relative to total return volatility.

For periodic returns:

\[
S
=
\frac{
\overline{R-R_f}
}{
\sigma_R
}
\sqrt{N}
\]

where:

- \(R\) is the periodic return.
- \(R_f\) is the periodic risk-free rate.
- \(\sigma_R\) is the standard deviation of periodic returns.
- \(N\) is the number of return observations per year.

The annualization factor is:

\[
\sqrt{N}
\]

### Usage

```python
from quanttools.statistics import sharpe_ratio

result = sharpe_ratio(
    returns,
)

print(result)
```

A higher Sharpe Ratio indicates greater excess return per unit of total volatility.

---

## Sortino Ratio

### Definition

The Sortino Ratio measures excess return relative to downside deviation rather than total volatility.

QuantTools calculates the periodic risk-free rate as:

\[
R_{f,periodic}
=
\frac{R_f}{N}
\]

The excess return is:

\[
R_{excess}
=
R-R_{f,periodic}
\]

Downside deviation is calculated from observations where the excess return is below zero.

The annualized Sortino Ratio is:

\[
Sortino
=
\frac{
\overline{R_{excess}}
}{
DD
}
\sqrt{N}
\]

where \(DD\) is downside deviation.

### Usage

```python
from quanttools.statistics import sortino_ratio

result = sortino_ratio(
    returns,
)

print(result)
```

Unlike the Sharpe Ratio, the Sortino Ratio does not penalize returns above the target threshold as downside risk.

---

## Calmar Ratio

### Definition

The Calmar Ratio compares return performance with maximum drawdown.

It is generally expressed as:

\[
Calmar
=
\frac{CAGR}
{|MDD|}
\]

where:

- \(CAGR\) is compound annual growth rate.
- \(MDD\) is maximum drawdown.

Because maximum drawdown is negative in QuantTools, its absolute value represents the magnitude of the loss.

### Usage

```python
from quanttools.statistics import calmar_ratio

result = calmar_ratio(
    returns,
)

print(result)
```

A higher Calmar Ratio indicates greater annualized return relative to historical drawdown severity.

---

# Trade Analytics

---

## Profit Factor

### Definition

Profit Factor measures the ratio of gross profits to gross losses.

\[
PF
=
\frac{
\sum Winning\ Trades
}{
\left|
\sum Losing\ Trades
\right|
}
\]

For example:

```text
Profit Factor = 1.50
```

means that the strategy generated ₹1.50 of gross profit for every ₹1.00 of gross loss.

### Usage

```python
from quanttools.statistics import profit_factor

trade_results = pd.Series([
    100,
    -50,
    75,
    -25,
])

result = profit_factor(
    trade_results,
)

print(result)
```

A Profit Factor greater than `1.0` indicates that gross profits exceed gross losses.

---

## Expectancy

### Definition

Expectancy measures the average profit or loss expected per trade.

A common formulation is:

\[
E
=
P(W)\cdot AW
+
P(L)\cdot AL
\]

where:

- \(P(W)\) is the probability of a winning trade.
- \(P(L)\) is the probability of a losing trade.
- \(AW\) is average winning trade.
- \(AL\) is average losing trade.

The average losing trade is negative.

### Usage

```python
from quanttools.statistics import expectancy

result = expectancy(
    trade_results,
)

print(result)
```

Positive expectancy indicates that the historical trade distribution generated positive average profit per trade.

---

## Win Rate

### Definition

Win Rate measures the proportion of completed trades that generated a positive result.

\[
WinRate
=
\frac{
N_{wins}
}{
N_{trades}
}
\]

### Usage

```python
from quanttools.statistics import win_rate

result = win_rate(
    trade_results,
)

print(result)
```

The result is expressed as a decimal.

For example:

```text
0.60
```

represents a **60% win rate**.

Win Rate should not be evaluated independently from payoff and expectancy. A strategy can have a low win rate and still be profitable if its winning trades are sufficiently larger than its losing trades.

---

## Average Win

### Definition

Average Win is the mean profit among winning trades.

\[
AverageWin
=
\frac{
\sum Winning\ Trades
}{
N_{wins}
}
\]

Only positive trade results are included.

### Usage

```python
from quanttools.statistics import average_win

result = average_win(
    trade_results,
)

print(result)
```

---

## Average Loss

### Definition

Average Loss is the mean loss among losing trades.

\[
AverageLoss
=
\frac{
\sum Losing\ Trades
}{
N_{losses}
}
\]

Losing trades are represented as negative values.

### Usage

```python
from quanttools.statistics import average_loss

result = average_loss(
    trade_results,
)

print(result)
```

---

## Payoff Ratio

### Definition

Payoff Ratio measures the size of the average winning trade relative to the average losing trade.

\[
PayoffRatio
=
\frac{
AverageWin
}{
|AverageLoss|
}
\]

For example:

```text
Payoff Ratio = 2.0
```

means that the average winning trade is twice the magnitude of the average losing trade.

### Usage

```python
from quanttools.statistics import payoff_ratio

result = payoff_ratio(
    trade_results,
)

print(result)
```

Payoff Ratio should be considered together with Win Rate.

For example, a strategy with a 40% Win Rate can still have positive expectancy if its average winning trade is sufficiently larger than its average losing trade.

---

# Combining Performance and Trade Analytics

The individual statistics can be combined to evaluate a strategy from multiple perspectives.

```python
import pandas as pd

from quanttools.statistics import (
    average_loss,
    average_win,
    cagr,
    calmar_ratio,
    expectancy,
    max_drawdown,
    payoff_ratio,
    profit_factor,
    sharpe_ratio,
    sortino_ratio,
    win_rate,
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

print("CAGR:", cagr(returns))
print("Sharpe Ratio:", sharpe_ratio(returns))
print("Sortino Ratio:", sortino_ratio(returns))
print("Calmar Ratio:", calmar_ratio(returns))
print("Maximum Drawdown:", max_drawdown(returns))

print("Profit Factor:", profit_factor(trade_results))
print("Expectancy:", expectancy(trade_results))
print("Win Rate:", win_rate(trade_results))
print("Average Win:", average_win(trade_results))
print("Average Loss:", average_loss(trade_results))
print("Payoff Ratio:", payoff_ratio(trade_results))
```

---

# Interpreting the Metrics

These metrics describe different characteristics of a strategy:

| Metric | Measures |
| --- | --- |
| **CAGR** | Annualized compounded growth |
| **Sharpe Ratio** | Excess return relative to total volatility |
| **Sortino Ratio** | Excess return relative to downside volatility |
| **Calmar Ratio** | CAGR relative to maximum drawdown |
| **Maximum Drawdown** | Largest peak-to-trough decline |
| **Drawdown Duration** | Time spent below a previous equity peak |
| **Profit Factor** | Gross profits relative to gross losses |
| **Expectancy** | Average profit or loss per trade |
| **Win Rate** | Percentage of profitable trades |
| **Average Win** | Mean winning trade |
| **Average Loss** | Mean losing trade |
| **Payoff Ratio** | Average win relative to average loss |

No individual metric completely describes strategy quality. Performance, risk, and trade characteristics should be evaluated together.