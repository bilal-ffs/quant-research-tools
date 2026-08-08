from quanttools.statistics import (
    drawdown_series,
    max_drawdown,
    drawdown_duration,
    sharpe_ratio,
    sortino_ratio,
    cagr,
    calmar_ratio,
    profit_factor,
    expectancy,
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
