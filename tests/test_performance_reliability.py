"""Independent regression checks for corrected metrics and observation alignment."""

import numpy as np
import pandas as pd
import pytest

from quanttools import Backtest
from quanttools.portfolio import (
    active_return,
    alpha,
    beta,
    information_ratio,
    tracking_error,
    treynor_ratio,
)
from quanttools.reports import performance_report
from quanttools.risk import downside_deviation, ulcer_index, volatility
from quanttools.statistics import (
    cagr,
    calmar_ratio,
    drawdown_duration,
    drawdown_episodes,
    drawdown_series,
    expectancy,
    max_drawdown,
    recovery_time,
    sharpe_ratio,
    sortino_ratio,
)
from quanttools.utils.validation import validate_return_pair

PAIRED = [active_return, alpha, beta, information_ratio, tracking_error, treynor_ratio]
ANNUALIZED = [cagr, calmar_ratio, sharpe_ratio, sortino_ratio, volatility]


def test_initial_loss_and_downstream_metrics():
    labels = pd.date_range("2020-01-01", periods=2)
    returns = pd.Series([-0.10, 0.05], index=labels)
    dd = drawdown_series(returns)
    pd.testing.assert_index_equal(dd.index, labels)
    assert dd.tolist() == pytest.approx([-0.10, -0.055])
    assert max_drawdown(returns) == pytest.approx(-0.10)
    assert drawdown_duration(returns) == 2
    assert ulcer_index(returns) == pytest.approx(np.sqrt((0.1**2 + 0.055**2) / 2))
    assert calmar_ratio(returns, 2) == pytest.approx(-0.055 / 0.10)


def test_equal_peak_is_recovery_and_initial_peak_is_explicit():
    labels = pd.date_range("2020-01-01", periods=3)
    returns = pd.Series([-0.2, 0.25, -0.1], index=labels)
    episodes = drawdown_episodes(returns)
    first, second = episodes.iloc[0], episodes.iloc[1]
    assert pd.isna(first.peak)
    assert first.peak_position == -1
    assert first.trough == labels[0]
    assert first.recovery == labels[1]
    assert first.depth == pytest.approx(-0.2)
    assert first.underwater_duration == 1
    assert first.trough_to_recovery_duration == 1
    assert first.recovered
    assert second.peak == labels[1]
    assert not second.recovered
    assert pd.isna(second.recovery)
    assert pd.isna(second.trough_to_recovery_duration)
    assert recovery_time(returns) == 1
    assert drawdown_duration(returns) == 1


def test_recovery_durations_multiple_periods_and_over_peak():
    # Equity: 1, 2, 1, 0.5, 0.5, 1, 2.2.
    returns = pd.Series([1, -0.5, -0.5, 0, 1, 1.2], index=list("abcdef"))
    episode = drawdown_episodes(returns).iloc[0]
    assert episode.peak == "a"
    assert episode.trough == "c"  # first tied minimum
    assert episode.recovery == "f"
    assert episode.depth == -0.75
    assert episode.underwater_duration == 4
    assert episode.trough_to_recovery_duration == 3
    assert recovery_time(returns) == 3


def test_unrecovered_deepest_episode_has_no_completed_time():
    returns = pd.Series([-0.5, 0.2, 0.1])
    episode = drawdown_episodes(returns).iloc[0]
    assert not episode.recovered
    assert pd.isna(episode.recovery_position)
    assert pd.isna(episode.trough_to_recovery_duration)
    assert episode.underwater_duration == 3
    assert recovery_time(returns) is None


def test_no_drawdown_and_tied_depth_policy():
    assert drawdown_episodes(pd.Series([0, 0.1, 0])).empty
    assert recovery_time(pd.Series([0, 0.1, 0])) == 0
    assert recovery_time(pd.Series([-0.5, 1, -0.5])) == 1


@pytest.mark.parametrize("metric", PAIRED)
def test_paired_metrics_align_reordered_labels(metric):
    portfolio = pd.Series([0.04, -0.02, 0.06], index=list("abc"))
    benchmark = pd.Series([0.02, -0.03, 0.01], index=list("abc"))
    assert metric(portfolio, benchmark.iloc[::-1]) == pytest.approx(
        metric(portfolio, benchmark)
    )


@pytest.mark.parametrize("metric", PAIRED)
@pytest.mark.parametrize("labels", [list("bcd"), list("aaa"), list("abcd")])
def test_paired_metrics_reject_unrelated_or_duplicate_labels(metric, labels):
    portfolio = pd.Series([0.04, -0.02, 0.06], index=list("abc"))
    benchmark = pd.Series(np.arange(len(labels)) * 0.01, index=labels)
    with pytest.raises(ValueError, match="index|indices"):
        metric(portfolio, benchmark)


def test_missing_pairs_are_dropped_together():
    portfolio = pd.Series([0.04, np.nan, 0.06, -0.01], index=list("abcd"))
    benchmark = pd.Series([0.02, -0.03, np.nan, -0.02], index=list("abcd"))
    p, b = validate_return_pair(portfolio, benchmark.iloc[::-1])
    assert p.index.tolist() == b.index.tolist() == ["a", "d"]
    assert active_return(portfolio, benchmark) == pytest.approx(0.015)
    with pytest.raises(ValueError, match="complete paired"):
        validate_return_pair(pd.Series([0.1, np.nan]), pd.Series([np.nan, 0.1]))


def test_nonfinite_values_cannot_be_hidden_by_missing_partner():
    with pytest.raises(ValueError, match="finite"):
        active_return(pd.Series([np.inf, 0.1]), pd.Series([np.nan, 0.2]))


@pytest.mark.parametrize(
    "metric", [cagr, drawdown_series, sharpe_ratio, ulcer_index, volatility, expectancy]
)
@pytest.mark.parametrize("bad", [np.inf, -np.inf, "oops", 1j, True])
def test_numeric_validation(metric, bad):
    with pytest.raises((TypeError, ValueError)):
        metric(pd.Series([bad, bad]))


@pytest.mark.parametrize("metric", ANNUALIZED)
@pytest.mark.parametrize("bad", [0, -1, np.nan, np.inf, "252", True])
def test_annualization_validation(metric, bad):
    with pytest.raises((TypeError, ValueError)):
        metric(pd.Series([0.02, -0.03, -0.01]), periods_per_year=bad)


@pytest.mark.parametrize(
    "metric", [sharpe_ratio, sortino_ratio, downside_deviation, alpha, treynor_ratio]
)
def test_risk_free_rate_must_be_finite(metric):
    returns = pd.Series([0.02, -0.03, -0.01])
    args = (returns, returns) if metric in [alpha, treynor_ratio] else (returns,)
    with pytest.raises(ValueError, match="finite"):
        metric(*args, risk_free_rate=np.inf)


def test_bankruptcy_is_absorbing_but_return_statistics_use_all_observations():
    returns = pd.Series([-1.0, 0.5, 0.1])
    assert drawdown_series(returns).tolist() == [-1, -1, -1]
    assert max_drawdown(returns) == -1
    assert ulcer_index(returns) == 1
    assert cagr(returns, 12) == -1
    assert calmar_ratio(returns, 12) == -1
    assert recovery_time(returns) is None
    assert sharpe_ratio(returns, periods_per_year=12) == pytest.approx(
        returns.mean() / returns.std(ddof=1) * np.sqrt(12)
    )
    with pytest.raises(ValueError, match="undefined"):
        sharpe_ratio(pd.Series([-1, -1]))
    with pytest.raises(ValueError, match="zero"):
        calmar_ratio(pd.Series([0, 0]))


@pytest.mark.parametrize(
    "metric", [cagr, max_drawdown, ulcer_index, sharpe_ratio, sortino_ratio, volatility]
)
def test_below_bankruptcy_is_invalid_for_simple_returns(metric):
    with pytest.raises(ValueError, match="-100%"):
        metric(pd.Series([-1.01, 0.5]))
    # Currency trade losses are unrestricted by the simple-return lower bound.
    assert expectancy(pd.Series([-200.0, 100.0])) == -50


def test_missing_observations_preserve_retained_drawdown_labels():
    returns = pd.Series([-0.1, np.nan, 0.05], index=list("abc"))
    assert drawdown_series(returns).index.tolist() == ["a", "c"]
    assert drawdown_duration(returns) == 2


def test_backtest_and_report_propagate_configuration():
    returns = pd.Series([0.04, -0.03, 0.02, -0.01])
    trades = pd.Series([100, -200, 50])
    bt = Backtest(returns, trades, periods_per_year=12, risk_free_rate=0.06)
    summary = bt.summary()
    assert summary["cagr"] == pytest.approx(np.prod(1 + returns) ** 3 - 1)
    assert summary["sharpe_ratio"] == pytest.approx(
        (returns.mean() - 0.06 / 12) / returns.std(ddof=1) * np.sqrt(12)
    )
    assert summary["sortino_ratio"] == pytest.approx(sortino_ratio(returns, 0.06, 12))
    assert summary["calmar_ratio"] == pytest.approx(calmar_ratio(returns, 12))
    assert bt.report() == performance_report(
        returns, trades, periods_per_year=12, risk_free_rate=0.06
    )
    assert f'{summary["cagr"]:>10.2%}' in bt.report()
    assert f'{summary["sharpe_ratio"]:>10.2f}' in bt.report()


@pytest.mark.parametrize(
    "options", [{"periods_per_year": np.nan}, {"risk_free_rate": np.inf}]
)
def test_backtest_rejects_invalid_configuration(options):
    with pytest.raises(ValueError):
        Backtest(pd.Series([0.1, -0.2]), pd.Series([100, -200]), **options)


def test_compounding_overflow_is_explicit():
    with pytest.raises(ValueError, match="finite numeric range"):
        drawdown_series(pd.Series([1e200, 1e200]))


def test_episode_labels_preserve_large_integer_ids():
    labels = [2**60 + 1, 2**60 + 2, 2**60 + 3]
    episodes = drawdown_episodes(pd.Series([-0.2, 0.25, -0.1], index=labels))
    assert episodes.iloc[0].trough == labels[0]
    assert episodes.iloc[0].recovery == labels[1]
    assert episodes.iloc[1].peak == labels[1]


def test_constant_variance_is_undefined_despite_roundoff():
    returns = pd.Series([0.03] * 10)
    with pytest.raises(ValueError):
        sharpe_ratio(returns, risk_free_rate=0.02)
    with pytest.raises(ValueError):
        volatility(returns)
    assert downside_deviation(-returns) == 0
    with pytest.raises(ValueError):
        sortino_ratio(-returns)
