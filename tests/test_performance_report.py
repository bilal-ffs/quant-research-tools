import pandas as pd

from quanttools.reports.performance import (
    performance_report,
)


def test_report_contains_sections():
    returns = pd.Series(
        [
            0.02,
            -0.01,
            0.03,
            -0.02,
            0.01,
        ]
    )

    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
            50,
        ]
    )

    report = performance_report(
        returns,
        trade_results,
    )

    assert "Performance Metrics" in report
    assert "Risk Metrics" in report
    assert "Trade Analytics" in report


def test_report_contains_metrics():
    returns = pd.Series(
        [
            0.02,
            -0.01,
            0.03,
            -0.02,
            0.01,
        ]
    )

    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
            50,
        ]
    )

    report = performance_report(
        returns,
        trade_results,
    )

    assert "Sharpe Ratio" in report
    assert "Sortino Ratio" in report
    assert "Profit Factor" in report
    assert "Payoff Ratio" in report
