import json
from pathlib import Path

import pandas as pd

from quanttools import (
    Backtest,
)


def create_backtest() -> Backtest:
    returns = pd.Series(
        [
            0.02,
            -0.01,
            0.03,
            -0.02,
            0.01,
            0.015,
        ]
    )

    trade_results = pd.Series(
        [
            100,
            -50,
            75,
            -25,
            50,
            -40,
        ]
    )

    return Backtest(
        returns,
        trade_results,
    )


def test_report_returns_string():
    bt = create_backtest()

    assert isinstance(
        bt.report(),
        str,
    )


def test_sharpe_ratio_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.sharpe_ratio(),
        float,
    )


def test_sortino_ratio_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.sortino_ratio(),
        float,
    )


def test_cagr_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.cagr(),
        float,
    )


def test_calmar_ratio_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.calmar_ratio(),
        float,
    )


def test_max_drawdown_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.max_drawdown(),
        float,
    )


def test_drawdown_duration_returns_int():
    bt = create_backtest()

    assert isinstance(
        bt.drawdown_duration(),
        int,
    )


def test_profit_factor_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.profit_factor(),
        float,
    )


def test_expectancy_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.expectancy(),
        float,
    )


def test_win_rate_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.win_rate(),
        float,
    )


def test_average_win_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.average_win(),
        float,
    )


def test_average_loss_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.average_loss(),
        float,
    )


def test_payoff_ratio_returns_float():
    bt = create_backtest()

    assert isinstance(
        bt.payoff_ratio(),
        float,
    )


def test_summary_returns_dict():
    bt = create_backtest()

    summary = bt.summary()

    assert isinstance(
        summary,
        dict,
    )


def test_summary_contains_all_metrics():
    bt = create_backtest()

    summary = bt.summary()

    expected_keys = {
        "cagr",
        "sharpe_ratio",
        "sortino_ratio",
        "calmar_ratio",
        "max_drawdown",
        "drawdown_duration",
        "profit_factor",
        "expectancy",
        "win_rate",
        "average_win",
        "average_loss",
        "payoff_ratio",
    }

    assert set(summary.keys()) == expected_keys


def test_to_dataframe_returns_dataframe():
    bt = create_backtest()

    df = bt.to_dataframe()

    assert isinstance(
        df,
        pd.DataFrame,
    )


def test_to_dataframe_columns():
    bt = create_backtest()

    df = bt.to_dataframe()

    assert list(df.columns) == [
        "Metric",
        "Value",
    ]


def test_to_dataframe_row_count():
    bt = create_backtest()

    df = bt.to_dataframe()

    assert len(df) == len(bt.summary())


def test_to_json_returns_string():
    bt = create_backtest()

    result = bt.to_json()

    assert isinstance(
        result,
        str,
    )


def test_to_json_is_valid_json():
    bt = create_backtest()

    result = bt.to_json()

    data = json.loads(result)

    assert isinstance(
        data,
        dict,
    )


def test_to_json_contains_metrics():
    bt = create_backtest()

    data = json.loads(bt.to_json())

    assert "sharpe_ratio" in data
    assert "profit_factor" in data


def test_to_csv_creates_file(tmp_path: Path):
    bt = create_backtest()

    filename = tmp_path / "summary.csv"

    bt.to_csv(
        str(filename),
    )

    assert filename.exists()


def test_to_csv_contains_expected_columns(tmp_path: Path):
    bt = create_backtest()

    filename = tmp_path / "summary.csv"

    bt.to_csv(
        str(filename),
    )

    df = pd.read_csv(filename)

    assert list(df.columns) == [
        "Metric",
        "Value",
    ]
