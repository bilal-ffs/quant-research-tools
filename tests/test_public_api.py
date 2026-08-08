from quanttools.statistics import (
    cagr,
    calmar_ratio,
    drawdown_duration,
    drawdown_series,
    expectancy,
    max_drawdown,
    profit_factor,
    sharpe_ratio,
    sortino_ratio,
)


def test_public_api_imports():
    assert callable(drawdown_series)
    assert callable(max_drawdown)
    assert callable(drawdown_duration)
    assert callable(sharpe_ratio)
    assert callable(sortino_ratio)
    assert callable(cagr)
    assert callable(calmar_ratio)
    assert callable(profit_factor)
    assert callable(expectancy)
