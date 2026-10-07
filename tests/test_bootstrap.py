"""Independent bootstrap calculations, sampling boundaries and reproducibility."""

import numpy as np
import pandas as pd
import pytest

from quanttools import Backtest
from quanttools.validation import BootstrapResult, iid_bootstrap, moving_block_bootstrap


@pytest.mark.parametrize("bootstrap", [iid_bootstrap, moving_block_bootstrap])
def test_reproducibility_and_global_rng_unchanged(bootstrap):
    returns = pd.Series([-0.1, 0.02, 0.01, -0.03, 0.04, 0.06])
    before = np.random.get_state()
    first = bootstrap(returns, n_simulations=12, random_state=123, return_paths=True)
    second = bootstrap(returns, n_simulations=12, random_state=123, return_paths=True)
    after = np.random.get_state()
    pd.testing.assert_frame_equal(first.metrics, second.metrics)
    pd.testing.assert_frame_equal(first.summary, second.summary)
    np.testing.assert_array_equal(first.paths, second.paths)
    assert first.probability_of_loss == second.probability_of_loss
    assert before[0] == after[0]
    np.testing.assert_array_equal(before[1], after[1])
    assert before[2:] == after[2:]


def test_iid_outputs_against_independent_calculation():
    historical = np.array([-0.2, 0.1, 0.03])
    n, horizon, seed = 9, 5, 8
    result = iid_bootstrap(
        pd.Series(historical),
        n_simulations=n,
        horizon=horizon,
        confidence_level=0.8,
        periods_per_year=12,
        risk_free_rate=0.06,
        random_state=seed,
        return_paths=True,
    )
    rng = np.random.default_rng(seed)
    expected = []
    equity_paths = []
    for _ in range(n):
        samples = historical[rng.integers(0, 3, size=horizon)]
        equity = [1.0]
        for value in samples:
            equity.append(equity[-1] * (1 + value))
        peak = 1.0
        worst = 0.0
        for value in equity:
            peak = max(peak, value)
            worst = min(worst, value / peak - 1)
        expected.append(
            [
                equity[-1] - 1,
                equity[-1] ** (12 / horizon) - 1,
                worst,
                (
                    (samples.mean() - 0.06 / 12) / samples.std(ddof=1) * np.sqrt(12)
                    if np.ptp(samples) > 0
                    else np.nan
                ),
            ]
        )
        equity_paths.append(equity)
    np.testing.assert_allclose(result.metrics, expected)
    np.testing.assert_allclose(result.paths, equity_paths)
    np.testing.assert_allclose(
        result.summary[["lower", "median", "upper"]],
        np.nanquantile(expected, [0.1, 0.5, 0.9], axis=0).T,
    )
    np.testing.assert_array_equal(
        result.summary.valid_count, np.isfinite(expected).sum(axis=0)
    )
    assert result.probability_of_loss == np.mean(np.array(equity_paths)[:, -1] < 1)
    assert result.probability_valid_count == n


def test_block_sampling_non_circular_boundaries_and_truncation():
    historical = np.array([-0.12, -0.08, -0.01, 0.03, 0.09])
    n, block, horizon, seed = 6, 3, 7, 42
    result = moving_block_bootstrap(
        pd.Series(historical),
        n_simulations=n,
        block_size=block,
        horizon=horizon,
        random_state=seed,
        return_paths=True,
    )
    rng = np.random.default_rng(seed)
    for path in result.paths:
        starts = rng.integers(0, len(historical) - block + 1, size=3)
        expected = np.concatenate([historical[s : s + block] for s in starts])[:horizon]
        recovered_samples = path[1:] / path[:-1] - 1
        np.testing.assert_allclose(recovered_samples, expected, atol=1e-15)
    assert result.paths.shape == (n, horizon + 1)
    assert (result.paths[:, 0] == 1).all()


def test_full_sample_block_and_block_size_one():
    returns = pd.Series([-0.2, 0.25, 0.1])
    full = moving_block_bootstrap(
        returns,
        n_simulations=2,
        block_size=3,
        horizon=5,
        return_paths=True,
    )
    expected = np.cumprod([1, 0.8, 1.25, 1.1, 0.8, 1.25])
    np.testing.assert_allclose(full.paths, np.tile(expected, (2, 1)))
    iid = iid_bootstrap(returns, n_simulations=5, random_state=4)
    blocks = moving_block_bootstrap(
        returns, n_simulations=5, block_size=1, random_state=4
    )
    pd.testing.assert_frame_equal(iid.metrics, blocks.metrics)


@pytest.mark.parametrize("bootstrap", [iid_bootstrap, moving_block_bootstrap])
def test_undefined_sharpe_keeps_entire_path_and_valid_counts(bootstrap):
    result = bootstrap(pd.Series([-0.1] * 5), n_simulations=4, random_state=1)
    assert result.paths is None
    assert len(result.metrics) == 4
    assert result.metrics.sharpe_ratio.isna().all()
    assert result.summary.loc["sharpe_ratio", "valid_count"] == 0
    assert result.summary.loc["sharpe_ratio", ["lower", "median", "upper"]].isna().all()
    assert result.summary.loc["cagr", "valid_count"] == 4
    assert result.probability_of_loss == 1
    assert result.metrics.max_drawdown.tolist() == pytest.approx([0.9**5 - 1] * 4)


def test_one_observation_and_bankruptcy():
    result = iid_bootstrap(
        pd.Series([-1.0]),
        n_simulations=3,
        horizon=4,
        return_paths=True,
        random_state=1,
    )
    np.testing.assert_array_equal(result.paths, np.tile([1, 0, 0, 0, 0], (3, 1)))
    assert (result.metrics[["total_return", "cagr", "max_drawdown"]] == -1).all().all()
    assert result.metrics.sharpe_ratio.isna().all()
    assert result.probability_of_loss == 1
    short = iid_bootstrap(pd.Series([-0.1, 0.2]), n_simulations=3, horizon=1)
    assert short.metrics.sharpe_ratio.isna().all()
    assert short.summary.loc["total_return", "valid_count"] == 3


def test_overflow_keeps_paths_and_reports_valid_probability_denominator():
    result = iid_bootstrap(pd.Series([1e200]), n_simulations=2, horizon=2)
    assert len(result.metrics) == 2
    assert result.metrics.isna().all().all()
    assert result.summary.valid_count.sum() == 0
    assert result.probability_valid_count == 0
    assert np.isnan(result.probability_of_loss)


def test_partial_undefined_counts_and_loss_probability_includes_constant_paths():
    result = iid_bootstrap(
        pd.Series([-0.5, 0.5]),
        n_simulations=50,
        horizon=2,
        random_state=2,
    )
    valid = result.metrics.sharpe_ratio.notna().sum()
    assert 0 < valid < 50
    assert result.summary.loc["sharpe_ratio", "valid_count"] == valid
    assert result.summary.loc["total_return", "valid_count"] == 50
    assert result.probability_of_loss == (result.metrics.total_return < 0).mean()


@pytest.mark.parametrize(
    "options",
    [
        {"n_simulations": 0},
        {"n_simulations": 1.5},
        {"n_simulations": True},
        {"horizon": 0},
        {"horizon": 2.5},
        {"horizon": False},
        {"confidence_level": 0},
        {"confidence_level": 1},
        {"confidence_level": np.nan},
        {"confidence_level": np.inf},
        {"periods_per_year": 0},
        {"periods_per_year": np.nan},
        {"risk_free_rate": np.inf},
        {"random_state": -1},
        {"random_state": 1.5},
        {"random_state": True},
        {"return_paths": "yes"},
    ],
)
@pytest.mark.parametrize("bootstrap", [iid_bootstrap, moving_block_bootstrap])
def test_bootstrap_parameter_validation(bootstrap, options):
    with pytest.raises((ValueError, TypeError)):
        bootstrap(pd.Series([0.01, -0.02, 0.03, -0.04, 0.05]), **options)


@pytest.mark.parametrize("block", [0, -1, 1.5, True, 6])
def test_block_size_validation(block):
    with pytest.raises((ValueError, TypeError)):
        moving_block_bootstrap(pd.Series([0.1] * 5), block_size=block)


@pytest.mark.parametrize(
    "returns",
    [
        pd.Series(dtype=float),
        pd.Series([np.nan]),
        pd.Series([np.inf]),
        pd.Series([-1.1]),
        pd.Series(["0.1"]),
        [0.1],
    ],
)
def test_bootstrap_input_validation(returns):
    with pytest.raises((ValueError, TypeError)):
        iid_bootstrap(returns)


def test_defaults_missing_values_and_optional_paths():
    returns = pd.Series([0.1, np.nan, -0.1, 0.03])
    result = iid_bootstrap(returns, random_state=0)
    assert isinstance(result, BootstrapResult)
    assert len(result.metrics) == 1000
    assert result.horizon == 3
    assert result.confidence_level == 0.95
    assert result.periods_per_year == 252
    assert result.risk_free_rate == 0
    assert result.paths is None
    stored = iid_bootstrap(returns.dropna(), random_state=0, return_paths=True)
    pd.testing.assert_frame_equal(result.metrics, stored.metrics)


@pytest.mark.parametrize("method", ["iid", "moving_block"])
def test_backtest_robustness_is_thin_configured_wrapper(method):
    returns = pd.Series([-0.1, 0.04, -0.02, 0.02, 0.08])
    bt = Backtest(
        returns, pd.Series([100, -200]), periods_per_year=12, risk_free_rate=0.03
    )
    options = dict(n_simulations=4, horizon=9, random_state=123, return_paths=True)
    actual = bt.robustness(method=method, **options)
    fn = iid_bootstrap if method == "iid" else moving_block_bootstrap
    expected = fn(returns, periods_per_year=12, risk_free_rate=0.03, **options)
    pd.testing.assert_frame_equal(actual.metrics, expected.metrics)
    np.testing.assert_array_equal(actual.paths, expected.paths)
    # The magnitude of cash P&L must never affect periodic-return robustness.
    other = Backtest(
        returns, pd.Series([100000, -0.5]), periods_per_year=12, risk_free_rate=0.03
    )
    pd.testing.assert_frame_equal(
        actual.metrics, other.robustness(method=method, **options).metrics
    )
    with pytest.raises(ValueError, match="method"):
        bt.robustness(method="unknown")


def test_summary_and_report_do_not_bootstrap(monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("bootstrap should remain opt-in")

    monkeypatch.setattr("quanttools.backtest.backtest.iid_bootstrap", fail)
    monkeypatch.setattr("quanttools.backtest.backtest.moving_block_bootstrap", fail)
    bt = Backtest(pd.Series([0.02, -0.03, -0.01, 0.05]), pd.Series([100, -200]))
    assert len(bt.summary()) == 12
    assert isinstance(bt.report(), str)


def test_equal_starting_capital_is_not_a_loss():
    result = moving_block_bootstrap(
        pd.Series([-0.2, 0.25]),
        block_size=2,
        horizon=2,
        n_simulations=3,
        random_state=1,
        return_paths=True,
    )
    np.testing.assert_array_equal(result.paths, np.tile([1, 0.8, 1], (3, 1)))
    assert result.probability_of_loss == 0
    assert result.probability_valid_count == 3
    assert result.metrics.total_return.tolist() == [0] * 3
    assert result.metrics.cagr.tolist() == [0] * 3
    assert result.metrics.max_drawdown.tolist() == pytest.approx([-0.2] * 3)


def test_block_bankruptcy_remains_zero_after_positive_returns():
    result = moving_block_bootstrap(
        pd.Series([-1, 0.5, 0.1]),
        block_size=3,
        horizon=3,
        n_simulations=2,
        return_paths=True,
    )
    np.testing.assert_array_equal(result.paths, np.tile([1, 0, 0, 0], (2, 1)))
    assert result.metrics.max_drawdown.tolist() == [-1, -1]
    assert result.metrics.sharpe_ratio.notna().all()
