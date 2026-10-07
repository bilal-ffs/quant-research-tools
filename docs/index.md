# Quant Research Tools

Quant Research Tools is an open-source Python library for quantitative finance, systematic trading, portfolio analytics, risk analysis, and financial research.

## Modules

### Statistics

Performance and trade-level statistical metrics.

- Drawdown Series
- Maximum Drawdown
- Drawdown Duration
- CAGR
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio
- Profit Factor
- Expectancy
- Win Rate
- Average Win
- Average Loss
- Payoff Ratio

[Statistics →](statistics.md)

### Portfolio

Benchmark-relative portfolio analytics.

- Beta
- Alpha
- Active Return
- Tracking Error
- Information Ratio
- Treynor Ratio

[Portfolio →](portfolio.md)

### Risk

Risk and downside analytics.

- Volatility
- Downside Deviation
- Historical Value at Risk
- Conditional Value at Risk
- Ulcer Index

[Risk →](risk.md)

### Backtest

The `Backtest` API provides a unified interface for analyzing return series and completed trade results.

[Backtest →](backtest.md)

### Reports

Generate formatted performance reports from return and trade data.

[Reports →](reports.md)

### Recovery and robustness

[Drawdown recovery](drawdown.md) documents `drawdown_episodes` and `recovery_time`.
[Bootstrap robustness](validation.md) covers IID and moving-block simulation APIs,
percentile summaries, valid counts and optional equity paths. Review
[input conventions](conventions.md) for bankruptcy, index alignment and annual
versus per-period risk-free rates.
