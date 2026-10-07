# Input and metric conventions

## Returns and cash P&L

Return APIs require a pandas Series of real numeric periodic **simple returns**
in decimal units, not log returns or currency P&L. Missing values are removed,
as in the existing API; empty/all-missing inputs raise `ValueError`. Retained index
labels and order are preserved. Strings, booleans, and complex values are rejected
with `TypeError`; infinities raise `ValueError`. Inputs are not mutated. Supply a
regular observation frequency; the library does not infer frequency from dates.
Missing values reduce observation counts and can join formerly separated blocks.

A simple return of exactly `-1.0` means bankruptcy. Starting from equity 1,
compounded equity becomes zero and remains zero, even if later input returns are
positive; no recapitalization is assumed. Total return and CAGR are `-1.0`,
maximum drawdown is `-1.0`, and Calmar is `-1.0`. Return-distribution metrics such
as Sharpe still describe **all supplied periodic observations**, including those
after bankruptcy, rather than replacing them with zeros. Constant returns and
one-observation samples have undefined Sharpe and raise `ValueError`.

Returns below `-1.0` are rejected by return APIs because they imply negative equity
and ambiguous compounding under this capital model. Leveraged cash losses must be
converted using an explicit external capital model. Trade APIs accept finite
currency P&L of any magnitude (including below -1), drop missing trades, and never
compound it or assign trade-level CAGR. Backtest return and trade samples need not
have the same length or indices.

## Annualization and risk-free rates

`periods_per_year` must be a finite positive real number. Defaults remain 252;
use 12 for monthly returns or 52 for weekly returns. Counts such as bootstrap
horizon, simulations, and block size must be positive integers. Booleans are not
accepted as numeric configuration. Risk-free rates must be finite real scalars.

| API | Risk-free-rate convention |
| --- | --- |
| `sharpe_ratio`, `sortino_ratio` | Annual rate, converted by `annual_rate / periods_per_year` |
| `Backtest`, `performance_report` | Annual rate, forwarded to Sharpe and Sortino |
| `iid_bootstrap`, `moving_block_bootstrap` | Annual rate, used for each path's Sharpe |
| `downside_deviation` | Per-period threshold; no annualization internally |
| `alpha`, `treynor_ratio` | Per-period rate, matching their periodic mean returns |

Arithmetic conversion of the annual risk-free rate is intentional and preserves
existing metric behavior; it is not an effective-rate geometric conversion.
Sharpe uses sample standard deviation (`ddof=1`) of excess returns and multiplies
by `sqrt(periods_per_year)`. Sortino preserves the existing denominator: sample
standard deviation of **only the negative excess observations**, rather than a
root mean square shortfall across all observations. Fewer than two downside
observations or constant downside observations give zero downside deviation;
Sortino then raises `ValueError`. Alpha, active return, tracking error, information
ratio, and Treynor remain periodic rather than newly annualized.

CAGR is `(ending_equity ** (periods_per_year / observation_count)) - 1`.
Zero equity has CAGR -1. Standalone equity metrics raise on numerical overflow,
and CAGR raises if its annualized result is nonfinite. Bootstrap records undefined
or nonfinite metrics as NaN and reports valid counts rather than dropping paths.

## Benchmark alignment

All paired portfolio metrics require **matching unique index label sets** before
missing-value removal. Different order is allowed: the benchmark is reindexed to
portfolio order. Different labels, different lengths, and duplicate labels raise
`ValueError`, even if the samples happen to have the same number of observations.
There is no implicit positional matching or automatic inner join of unrelated
samples. If intentional intersection is needed, align inputs explicitly first.

For matching indices, an observation with a missing value on either side is
dropped from **both** inputs. All paired calculations use this same cleaned pair,
including means, covariance and variance. Infinities and invalid returns on either
side are rejected even when the partner is missing. No complete pairs raises
`ValueError`; metrics needing variance require at least two complete pairs and
nonzero denominators. Default RangeIndex labels represent observation positions;
use meaningful timestamp labels when comparing dated returns.

## Undefined ratios and compatibility

Standalone metrics, `Backtest.summary()` and reports retain the existing exception
behavior for undefined ratios (zero variance, downside deviation, drawdown, beta,
tracking error, or missing winners/losers in trade ratios). They do not silently
substitute zero. Bootstrap handles undefined path metrics individually with NaN.

Intentional corrections include the starting-equity high-water mark, label-based
paired alignment and joint missing-value deletion, finite numeric validation,
simple-return lower bound, CAGR annualization validation, and exact-constant sample
checks so floating-point residual variance does not create huge spurious ratios.
Valid existing calls and default Backtest summary keys remain unchanged. Backtest
now validates and stores cleaned copies at construction, so invalid inputs fail
early. Robustness is opt-in and summary/report never run bootstrap simulations.
