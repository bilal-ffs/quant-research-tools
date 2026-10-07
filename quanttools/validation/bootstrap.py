"""Bootstrap robustness analysis of periodic simple returns, not cash trade P&L."""

from dataclasses import dataclass

import numpy as np
import pandas as pd

from quanttools.statistics import sharpe_ratio
from quanttools.utils.validation import (
    validate_finite,
    validate_periods_per_year,
    validate_positive_integer,
    validate_returns,
)


@dataclass
class BootstrapResult:
    """Every simulation, finite-metric percentile summaries, and optional equity.

    ``metrics`` has one row per simulation. Undefined/nonfinite metrics are NaN;
    ``summary`` has lower/median/upper percentiles and valid_count per metric.
    ``paths`` is None unless requested, otherwise shape (simulations, horizon+1)
    with starting equity 1 at column 0. probability_valid_count is the number
    of finite ending equities used for probability_of_loss.
    """

    metrics: pd.DataFrame
    summary: pd.DataFrame
    probability_of_loss: float
    probability_valid_count: int
    paths: np.ndarray | None
    method: str
    horizon: int
    block_size: int
    confidence_level: float
    periods_per_year: float
    risk_free_rate: float


def iid_bootstrap(
    returns: pd.Series,
    *,
    n_simulations: int = 1000,
    horizon: int | None = None,
    confidence_level: float = 0.95,
    periods_per_year: float = 252,
    risk_free_rate: float = 0.0,
    random_state: int | None = None,
    return_paths: bool = False,
) -> BootstrapResult:
    """Resample individual observations with replacement.

    Defaults: 1000 simulations, horizon equal to cleaned sample length, central
    95% percentile interval, 252 periods/year, annual risk-free rate 0, no saved
    paths. An integer seed gives reproducible results using a local NumPy RNG.
    Missing observations are dropped; remaining returns must be finite and >=-1.
    These distributions are conditional on the historical sample, not forecasts.
    """
    return _bootstrap(
        returns,
        n_simulations=n_simulations,
        horizon=horizon,
        block_size=1,
        confidence_level=confidence_level,
        periods_per_year=periods_per_year,
        risk_free_rate=risk_free_rate,
        random_state=random_state,
        return_paths=return_paths,
        method="iid",
    )


def moving_block_bootstrap(
    returns: pd.Series,
    *,
    n_simulations: int = 1000,
    horizon: int | None = None,
    block_size: int = 5,
    confidence_level: float = 0.95,
    periods_per_year: float = 252,
    risk_free_rate: float = 0.0,
    random_state: int | None = None,
    return_paths: bool = False,
) -> BootstrapResult:
    """Sample overlapping, non-circular contiguous blocks with replacement.

    Each block starts uniformly in [0, sample_length-block_size]. Concatenate
    blocks and truncate the last block to the horizon. block_size defaults to 5
    and must fit the cleaned sample; other defaults match iid_bootstrap.
    Blocks preserve some local dependence within blocks, not across boundaries.
    Observation order is the supplied order, with missing observations removed.
    Simulated distributions are conditional on the historical sample, not forecasts.
    """
    return _bootstrap(
        returns,
        n_simulations=n_simulations,
        horizon=horizon,
        block_size=block_size,
        confidence_level=confidence_level,
        periods_per_year=periods_per_year,
        risk_free_rate=risk_free_rate,
        random_state=random_state,
        return_paths=return_paths,
        method="moving_block",
    )


def _bootstrap(
    returns,
    *,
    n_simulations,
    horizon,
    block_size,
    confidence_level,
    periods_per_year,
    risk_free_rate,
    random_state,
    return_paths,
    method,
):
    values = validate_returns(returns).to_numpy()
    validate_positive_integer(n_simulations, "n_simulations")
    horizon = len(values) if horizon is None else horizon
    validate_positive_integer(horizon, "horizon")
    validate_positive_integer(block_size, "block_size")
    if block_size > len(values):
        raise ValueError("block_size cannot exceed the cleaned sample length.")
    validate_finite(confidence_level, "confidence_level")
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1.")
    validate_periods_per_year(periods_per_year)
    validate_finite(risk_free_rate, "risk_free_rate")
    if random_state is not None:
        if isinstance(random_state, (bool, np.bool_)) or not isinstance(
            random_state, (int, np.integer)
        ):
            raise TypeError("random_state must be a nonnegative integer or None.")
        if random_state < 0:
            raise ValueError("random_state must be nonnegative.")
    if not isinstance(return_paths, bool):
        raise TypeError("return_paths must be a bool.")
    rng = np.random.default_rng(random_state)
    paths = np.empty((n_simulations, horizon + 1)) if return_paths else None
    metrics = np.full((n_simulations, 4), np.nan)
    endings = np.full(n_simulations, np.nan)
    offsets = np.arange(block_size)
    n_blocks = (horizon + block_size - 1) // block_size
    for simulation in range(n_simulations):
        starts = rng.integers(0, len(values) - block_size + 1, size=n_blocks)
        indices = (starts[:, None] + offsets).ravel()[:horizon]
        sample = values[indices]
        with np.errstate(over="ignore", invalid="ignore", divide="ignore"):
            equity = np.concatenate(([1.0], np.cumprod(1 + sample)))
            # Bankruptcy is absorbing, including after an earlier numerical overflow.
            bankrupt = np.flatnonzero(sample == -1)
            if bankrupt.size:
                equity[bankrupt[0] + 1 :] = 0.0
            endings[simulation] = equity[-1]
            metrics[simulation, 0] = equity[-1] - 1
            metrics[simulation, 1] = equity[-1] ** (periods_per_year / horizon) - 1
            if np.isfinite(equity).all():
                metrics[simulation, 2] = np.min(
                    equity / np.maximum.accumulate(equity) - 1
                )
            try:
                metrics[simulation, 3] = sharpe_ratio(
                    pd.Series(sample),
                    risk_free_rate=risk_free_rate,
                    periods_per_year=periods_per_year,
                )
            except ValueError:
                # One observation or zero variance: only Sharpe is undefined.
                pass
        if paths is not None:
            paths[simulation] = equity
    metrics[~np.isfinite(metrics)] = np.nan
    frame = pd.DataFrame(
        metrics,
        columns=[
            "total_return",
            "cagr",
            "max_drawdown",
            "sharpe_ratio",
        ],
    )
    frame.index.name = "simulation"
    tail = (1 - confidence_level) / 2
    summary = frame.quantile([tail, 0.5, 1 - tail]).T
    summary.columns = ["lower", "median", "upper"]
    summary["valid_count"] = frame.count()
    finite_endings = endings[np.isfinite(endings)]
    probability = float(np.mean(finite_endings < 1)) if finite_endings.size else np.nan
    return BootstrapResult(
        metrics=frame,
        summary=summary,
        probability_of_loss=probability,
        probability_valid_count=len(finite_endings),
        paths=paths,
        method=method,
        horizon=horizon,
        block_size=block_size,
        confidence_level=confidence_level,
        periods_per_year=periods_per_year,
        risk_free_rate=risk_free_rate,
    )
