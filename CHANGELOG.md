# Changelog

## Unreleased

### Added

- `quanttools.statistics.drawdown_episodes`: labeled peaks, troughs and recoveries,
  negative depth, observation counts and explicit unrecovered status.
- Implemented and exported `recovery_time`: deepest episode's trough-to-recovery
  count, None if unrecovered, zero if no drawdown; first episode wins depth ties.
- `quanttools.validation.iid_bootstrap`, `moving_block_bootstrap`, and
  `BootstrapResult`: reproducible local RNG, per-simulation metrics, central
  percentile summaries, valid counts, ending-loss probability and optional paths.
- `Backtest.robustness`: opt-in thin wrapper; summaries and reports stay unchanged
  in scope and do not trigger simulations.
- Keyword-only periods_per_year and annual risk_free_rate configuration on
  Backtest and performance_report, propagated to applicable metrics.
- Runnable synthetic monthly-data example and documented metric conventions.
- NumPy declared explicitly as a dependency (also used by existing risk metrics).

### Intentional corrections

- Drawdowns include starting equity 1.0 as the first high-water mark without adding
  a row; first-period losses now affect maximum drawdown, duration, Calmar and ulcer
  index. For [-0.10, 0.05], drawdown is [-0.10, -0.055].
- Benchmark metrics require matching unique label sets, align order by label, and
  delete missing pairs jointly, rather than comparing unrelated means/variances.
  Mismatched or duplicate indices raise ValueError; no silent intersection.
- Real finite numeric validation and positive finite annualization validation;
  Backtest validates and stores cleaned copies at construction.
- Exactly -100% returns mean absorbing bankruptcy; below -100% simple returns
  raise ValueError. Cash trade P&L has no simple-return lower bound.
- Constant samples are recognized explicitly despite floating-point residual
  variance. Undefined ratios retain standalone ValueError behavior. Bootstrap
  keeps their paths, records undefined metrics as NaN, and reports valid counts.
- Equity compounding overflow raises in standalone metrics; bootstrap reports
  nonfinite metrics and probability denominators explicitly.
- Corrected downside-deviation documentation: its threshold is per-period,
  whereas Sharpe and Sortino accept an annual rate and divide by frequency.

### Compatibility and limitations

All previous public exports and valid calls remain available; Backtest's default
summary keys are unchanged. Annual risk-free conversion remains arithmetic;
Sortino's denominator remains sample standard deviation of negative excess
observations. Portfolio metrics remain periodic. Counts do not infer calendar time.
Bootstrap distributions are conditional on observed history, not forecasts.
Block sampling preserves dependence within blocks only, uses cleaned input order,
and does not infer an optimal block length. No execution, data downloads, brokers,
strategy optimization or trade-level CAGR are introduced. No release is published.
