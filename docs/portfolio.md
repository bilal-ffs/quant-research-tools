# Portfolio Analytics

Benchmark-relative metrics for evaluating portfolio performance against a reference benchmark.

---

## Beta

### Definition

Beta measures the sensitivity of portfolio returns to movements in benchmark returns.

QuantTools calculates beta using the covariance between portfolio and benchmark returns divided by the variance of benchmark returns:

\[
\beta
=
\frac{
\operatorname{Cov}(R_p,R_b)
}{
\operatorname{Var}(R_b)
}
\]

where:

- \(R_p\) is the portfolio return.
- \(R_b\) is the benchmark return.

### Interpretation

A beta of:

- `1.0` indicates sensitivity similar to the benchmark.
- Greater than `1.0` indicates greater sensitivity than the benchmark.
- Between `0` and `1.0` indicates lower sensitivity.
- A negative beta indicates an inverse relationship with the benchmark.

### Usage

```python
import pandas as pd

from quanttools.portfolio import beta

portfolio_returns = pd.Series([
    0.02,
    -0.01,
    0.03,
    0.01,
])

benchmark_returns = pd.Series([
    0.01,
    -0.02,
    0.02,
    0.00,
])

result = beta(
    portfolio_returns,
    benchmark_returns,
)

print(result)
```

---

## Alpha

### Definition

Alpha measures portfolio performance relative to the return expected from its exposure to the benchmark.

QuantTools calculates alpha using the portfolio and benchmark mean returns together with portfolio beta.

The general relationship is:

\[
\alpha
=
R_p
-
\left[
R_f
+
\beta(R_b-R_f)
\right]
\]

where:

- \(R_p\) is portfolio return.
- \(R_b\) is benchmark return.
- \(R_f\) is the risk-free rate.
- \(\beta\) is portfolio beta.

### Interpretation

Positive alpha indicates performance above the return implied by the portfolio's benchmark exposure.

Negative alpha indicates performance below the implied return.

### Usage

```python
from quanttools.portfolio import alpha

result = alpha(
    portfolio_returns,
    benchmark_returns,
)

print(result)
```

---

## Active Return

### Definition

Active Return measures the difference between portfolio return and benchmark return.

\[
ActiveReturn
=
R_p-R_b
\]

QuantTools calculates active return from the difference between portfolio and benchmark returns.

### Interpretation

- Positive active return indicates portfolio outperformance.
- Negative active return indicates portfolio underperformance.
- Zero active return indicates performance equal to the benchmark.

### Usage

```python
from quanttools.portfolio import active_return

result = active_return(
    portfolio_returns,
    benchmark_returns,
)

print(result)
```

---

## Tracking Error

### Definition

Tracking Error measures the variability of active returns.

Active returns are defined as:

\[
A_t
=
R_{p,t}-R_{b,t}
\]

Tracking Error is the standard deviation of these active returns:

\[
TE
=
\sigma(A)
\]

### Interpretation

A low Tracking Error indicates that portfolio returns closely follow the benchmark.

A high Tracking Error indicates greater deviation from benchmark performance.

Tracking Error is commonly used when evaluating how closely an investment strategy follows a benchmark.

### Usage

```python
from quanttools.portfolio import tracking_error

result = tracking_error(
    portfolio_returns,
    benchmark_returns,
)

print(result)
```

---

## Information Ratio

### Definition

The Information Ratio measures active return relative to Tracking Error.

\[
IR
=
\frac{
E[R_p-R_b]
}{
\sigma(R_p-R_b)
}
\]

where:

- \(R_p-R_b\) is the active return.
- \(\sigma(R_p-R_b)\) is Tracking Error.

### Interpretation

The Information Ratio measures how much active return is generated per unit of benchmark-relative risk.

Higher values indicate stronger active performance relative to the variability of that active performance.

### Usage

```python
from quanttools.portfolio import information_ratio

result = information_ratio(
    portfolio_returns,
    benchmark_returns,
)

print(result)
```

---

## Treynor Ratio

### Definition

The Treynor Ratio measures excess portfolio return relative to systematic risk.

Systematic risk is represented by portfolio beta.

The general formula is:

\[
Treynor
=
\frac{
R_p-R_f
}{
\beta
}
\]

where:

- \(R_p\) is portfolio return.
- \(R_f\) is the risk-free rate.
- \(\beta\) is portfolio beta.

### Interpretation

The Treynor Ratio answers:

> How much excess return was generated for each unit of systematic risk?

Unlike the Sharpe Ratio, which uses total volatility, the Treynor Ratio uses beta as its risk measure.

### Usage

```python
from quanttools.portfolio import treynor_ratio

result = treynor_ratio(
    portfolio_returns,
    benchmark_returns,
)

print(result)
```

---

# Complete Portfolio Analysis

The portfolio metrics can be combined to evaluate benchmark-relative performance from multiple perspectives.

```python
from quanttools.portfolio import (
    active_return,
    alpha,
    beta,
    information_ratio,
    tracking_error,
    treynor_ratio,
)

print(
    "Beta:",
    beta(
        portfolio_returns,
        benchmark_returns,
    ),
)

print(
    "Alpha:",
    alpha(
        portfolio_returns,
        benchmark_returns,
    ),
)

print(
    "Active Return:",
    active_return(
        portfolio_returns,
        benchmark_returns,
    ),
)

print(
    "Tracking Error:",
    tracking_error(
        portfolio_returns,
        benchmark_returns,
    ),
)

print(
    "Information Ratio:",
    information_ratio(
        portfolio_returns,
        benchmark_returns,
    ),
)

print(
    "Treynor Ratio:",
    treynor_ratio(
        portfolio_returns,
        benchmark_returns,
    ),
)
```

---

# Portfolio Metrics Overview

| Metric | Measures |
| --- | --- |
| **Beta** | Sensitivity to benchmark movements |
| **Alpha** | Return relative to benchmark-adjusted expected performance |
| **Active Return** | Difference between portfolio and benchmark returns |
| **Tracking Error** | Variability of active returns |
| **Information Ratio** | Active return relative to Tracking Error |
| **Treynor Ratio** | Excess return relative to systematic risk |

These metrics should be interpreted together. Beta describes benchmark sensitivity, Active Return describes relative performance, Tracking Error describes benchmark-relative risk, and Information Ratio evaluates the efficiency of active performance.