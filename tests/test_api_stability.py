import quanttools
import quanttools.portfolio as portfolio
import quanttools.risk as risk
import quanttools.statistics as statistics


def test_top_level_api():
    assert hasattr(
        quanttools,
        "Backtest",
    )


def test_statistics_api():
    expected = {
        "drawdown_series",
        "max_drawdown",
        "drawdown_duration",
        "cagr",
        "sharpe_ratio",
        "sortino_ratio",
        "calmar_ratio",
        "profit_factor",
        "expectancy",
        "win_rate",
        "average_win",
        "average_loss",
        "payoff_ratio",
    }

    assert set(statistics.__all__) == expected


def test_portfolio_api():
    expected = {
        "beta",
        "alpha",
        "active_return",
        "tracking_error",
        "information_ratio",
        "treynor_ratio",
    }

    assert set(portfolio.__all__) == expected


def test_risk_api():
    expected = {
        "volatility",
        "downside_deviation",
        "value_at_risk",
        "conditional_value_at_risk",
        "ulcer_index",
    }

    assert set(risk.__all__) == expected
