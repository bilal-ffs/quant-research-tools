# Risk Analytics

Risk and downside measures for return series.

---

## Volatility

### Definition

Volatility measures the dispersion of periodic returns.

QuantTools annualizes periodic volatility using:

\[
\sigma_{\text{annual}}
=
\sigma_{\text{periodic}}
\sqrt{N}
\]

where:

- \(\sigma_{\text{periodic}}\) is the standard deviation of returns.
- \(N\) is the number of return observations per year.

The default is:

```python
periods_per_year = 252
```

### Usage

```python
import pandas as pd

from quanttools.risk import volatility

returns = pd.Series([
    0.01,
    -0.02,
    0.03,
    0.01,
])

result = volatility(
    returns,
)

print(result)
```

For daily returns, the default `252` periods per year is appropriate.

For other frequencies, specify the appropriate number of observations:

```python
volatility(
    returns,
    periods_per_year=12,
)
```

---

## Downside Deviation

### Definition

Downside deviation measures the variability of returns below a specified minimum acceptable return.

QuantTools calculates downside deviation using returns below the periodic risk-free rate.

The periodic risk-free rate is calculated as:

\[
r_{f,\text{periodic}}
=
\frac{r_f}{N}
\]

where:

- \(r_f\) is the annual risk-free rate.
- \(N\) is the number of return observations per year.

Returns below this threshold are treated as downside observations.

### Usage

```python
from quanttools.risk import downside_deviation

result = downside_deviation(
    returns,
    risk_free_rate=0.05,
)

print(result)
```

If there are no downside observations, QuantTools returns:

```text
0.0
```

---

## Historical Value at Risk

### Definition

Historical Value at Risk (VaR) estimates the loss threshold corresponding to a specified confidence level using the historical distribution of returns.

For confidence level \(\alpha\):

\[
VaR_{\alpha}
=
-Q_{1-\alpha}(R)
\]

where \(Q\) represents the historical return quantile.

QuantTools reports VaR as a **positive loss magnitude**.

For example:

```text
VaR = 0.025
```

represents a historical loss threshold of approximately **2.5%**.

### Usage

```python
from quanttools.risk import value_at_risk

var = value_at_risk(
    returns,
    confidence_level=0.95,
)

print(var)
```

The confidence level must satisfy:

```text
0 < confidence_level < 1
```

---

## Conditional Value at Risk

### Definition

Conditional Value at Risk (CVaR), also known as **Expected Shortfall**, measures the average loss in the historical tail beyond the VaR threshold.

At confidence level \(\alpha\):

\[
CVaR_{\alpha}
=
-\mathbb{E}
\left[
R
\mid
R \leq Q_{1-\alpha}(R)
\right]
\]

QuantTools reports CVaR as a **positive loss magnitude**.

Because CVaR considers observations beyond the VaR threshold, it provides information about the **severity of losses in the tail**, rather than only the loss threshold.

### Usage

```python
from quanttools.risk import conditional_value_at_risk

cvar = conditional_value_at_risk(
    returns,
    confidence_level=0.95,
)

print(cvar)
```

---

## Ulcer Index

### Definition

The Ulcer Index measures the depth of drawdowns in a compounded equity curve.

QuantTools first constructs the equity curve:

\[
E_t
=
\prod_{i=1}^{t}
(1+r_i)
\]

The running peak is:

\[
P_t
=
\max_{i \leq t}
E_i
\]

The percentage drawdown is:

\[
D_t
=
\frac{E_t}{P_t}
-
1
\]

The Ulcer Index is then calculated as:

\[
UI
=
\sqrt{
\frac{1}{T}
\sum_{t=1}^{T}
D_t^2
}
\]

Unlike conventional volatility, the Ulcer Index focuses specifically on **drawdowns from previous equity peaks**.

### Usage

```python
from quanttools.risk import ulcer_index

ui = ulcer_index(
    returns,
)

print(ui)
```

A monotonically increasing equity curve has:

```text
Ulcer Index = 0
```

---

## Complete Risk Analysis

The metrics can be combined to provide a broader view of portfolio or strategy risk:

```python
from quanttools.risk import (
    conditional_value_at_risk,
    downside_deviation,
    ulcer_index,
    value_at_risk,
    volatility,
)

print(
    "Volatility:",
    volatility(returns),
)

print(
    "Downside Deviation:",
    downside_deviation(returns),
)

print(
    "VaR:",
    value_at_risk(returns),
)

print(
    "CVaR:",
    conditional_value_at_risk(returns),
)

print(
    "Ulcer Index:",
    ulcer_index(returns),
)
```

### Risk Metrics Overview

| Metric | Measures |
| --- | --- |
| **Volatility** | Overall return dispersion |
| **Downside Deviation** | Downside variability |
| **VaR** | Historical loss threshold |
| **CVaR** | Average loss in the historical tail |
| **Ulcer Index** | Drawdown depth and persistence |

Together, these metrics provide complementary perspectives on risk, covering **overall variability, downside risk, tail losses, and drawdown behavior**.