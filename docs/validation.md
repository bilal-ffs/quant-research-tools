# Bootstrap robustness testing

Bootstrap analysis resamples historical periodic simple returns to examine how
reported performance varies across alternative samples. It is an analytics tool;
it does not execute trades, download data, or optimize strategies.

```python
import pandas as pd
from quanttools.validation import iid_bootstrap, moving_block_bootstrap

returns = pd.Series([-0.03, 0.02, 0.01, -0.01, 0.04, 0.015])
result = moving_block_bootstrap(
    returns, n_simulations=1000, horizon=24, block_size=3,
    confidence_level=0.95, periods_per_year=12, risk_free_rate=0.03,
    random_state=42,
)
print(result.summary)
print(result.probability_of_loss)
print(result.probability_valid_count)
```

## Public APIs and defaults

Both `iid_bootstrap(returns, *, ...)` and
`moving_block_bootstrap(returns, *, ...)` return a `BootstrapResult`.

| Keyword | Default | Meaning |
| --- | --- | --- |
| `n_simulations` | `1000` | Positive integer number of sampled paths |
| `horizon` | `None` | Positive observation count; None uses cleaned sample length |
| `block_size` | `5` (moving blocks only) | Positive block length no larger than cleaned sample |
| `confidence_level` | `0.95` | Central percentile interval coverage, strictly between 0 and 1 |
| `periods_per_year` | `252` | Finite positive observation frequency |
| `risk_free_rate` | `0.0` | Annual rate for Sharpe; divided by periods_per_year |
| `random_state` | `None` | Nonnegative integer seed, or unseeded local generator |
| `return_paths` | `False` | Save compounded equity paths, including initial equity |

IID bootstrap samples individual observations uniformly with replacement.
Moving-block bootstrap samples uniformly from overlapping **non-circular** blocks
starting at indices `0` through `sample_length - block_size`, inclusive. It joins
whole blocks, then truncates the final block to the requested horizon. Horizons
may exceed the historical sample length. `block_size=1` is equivalent to IID;
`block_size=sample_length` repeats the historical sample deterministically.
For short samples, explicitly choose a block size that fits.

The supplied observation order is used, with missing observations removed.
No date sorting, gap filling, or calendar inference occurs. Blocks preserve some
local dependence within blocks, but not across newly joined block boundaries.
Both methods use `numpy.random.default_rng` locally and never seed or consume
NumPy's global random state. The same seed, input, parameters, and NumPy version
produce the same simulations; cross-version bitwise identity is not guaranteed.

## Structured results

`result.metrics` is a DataFrame indexed by simulation, with these columns:

- `total_return`: ending equity minus 1.
- `cagr`: ending equity raised to `periods_per_year / horizon`, minus 1.
- `max_drawdown`: minimum negative drawdown, including starting equity as a peak.
- `sharpe_ratio`: annualized sample Sharpe using all sampled periodic returns.

`result.summary` has one row per metric and columns `lower`, `median`, `upper`,
and integer `valid_count`. For confidence level c, the bounds are empirical
percentiles `(1-c)/2` and `(1+c)/2`; the median is the 50th percentile. Percentiles
use linear interpolation over that metric's finite simulation values. These are
distribution summaries, not a claimed confidence interval for a future return.

Undefined metrics (for example Sharpe with a one-observation or constant path)
and numerical overflow are recorded as NaN **without removing the simulation**.
Each metric is summarized using its own valid values. Zero valid values means
NaN percentile bounds and a count of zero. Drawdowns are negative decimals.

`result.probability_of_loss` is the empirical fraction of finite ending equities
**strictly below 1.0**. Equality is not a loss. Undefined Sharpe does not exclude
an ending equity from this probability. `probability_valid_count` reports its
denominator, which normally equals n_simulations; nonfinite ending equities are
excluded explicitly, with NaN probability if none are finite. Numerical overflow
can leave nonfinite values in requested paths, while metric outputs use NaN.

`result.paths` is None by default. With `return_paths=True`, it is a NumPy array
of equity values with shape `(n_simulations, horizon + 1)`, where column 0 is 1.0.
Retaining it costs approximately `8 * n_simulations * (horizon + 1)` bytes.
Without saved paths, temporary path storage is proportional to horizon, while
metric storage is proportional to simulations. Result metadata includes method,
horizon, block_size, confidence_level, periods_per_year and risk_free_rate.

A -100% sampled return is absorbing bankruptcy; equity stays zero and drawdown
is -100%. Sharpe describes sampled observations even after bankruptcy. Returns
below -100%, infinities and nonnumeric observations are rejected. See
[input conventions](conventions.md) for missing values and ratio definitions.

## Backtest wrapper

```python
from quanttools import Backtest

bt = Backtest(returns, pd.Series([100.0, -50.0]),
              periods_per_year=12, risk_free_rate=0.03)
result = bt.robustness(method="moving_block", block_size=3, random_state=42)
```

`Backtest.robustness` forwards to the standalone functions using the object's
annualization and annual risk-free-rate settings. `method` defaults to `"iid"`;
`"moving_block"` is the other accepted value. Its other defaults match the table;
block_size is used only for moving blocks. Cash trade P&L is never resampled or
compounded. `summary()` and `report()` do not compute robustness.

## Interpretation and example

The simulated distributions are **conditional on the historical sample, not
forecasts**. They cannot introduce unseen regimes or tail events. IID sampling
breaks serial dependence; blocks retain only some dependence and results depend
on the chosen block length and horizon. These functions do not select an optimal
block size or tune a strategy.

Run the synthetic monthly-return example from the repository root:

```bash
python -m examples.robustness_analysis
```

It demonstrates configurable annualization, labeled recovery episodes, a clearly
unrecovered episode, and reproducible IID and moving-block percentile summaries.
