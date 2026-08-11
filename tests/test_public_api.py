from quanttools import (
    Backtest,
)
from quanttools.portfolio import (
    active_return,
    alpha,
    beta,
    information_ratio,
    tracking_error,
    treynor_ratio,
)
from quanttools.risk import (
    conditional_value_at_risk,
    downside_deviation,
    ulcer_index,
    value_at_risk,
    volatility,
)
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


def test_portfolio_public_api_imports():
    assert callable(beta)
    assert callable(alpha)
    assert callable(active_return)
    assert callable(tracking_error)
    assert callable(information_ratio)
    assert callable(treynor_ratio)


def test_risk_public_api_imports():
    assert callable(volatility)
    assert callable(downside_deviation)
    assert callable(value_at_risk)
    assert callable(conditional_value_at_risk)
    assert callable(ulcer_index)


def test_top_level_public_api():
    assert callable(Backtest)
