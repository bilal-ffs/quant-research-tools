"""Shared validation for real numeric observations and configuration."""

from numbers import Integral, Real

import numpy as np
import pandas as pd
from pandas.api.types import is_bool_dtype, is_complex_dtype, is_numeric_dtype


def validate_finite(value: float, name: str) -> None:
    """Require a finite real scalar (booleans are not configuration values)."""
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")
    if not np.isfinite(value):
        raise ValueError(f"{name} must be finite.")


def validate_periods_per_year(periods_per_year: float) -> None:
    """Require a finite positive observation frequency."""
    validate_finite(periods_per_year, "periods_per_year")
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be greater than zero.")


def validate_positive_integer(value: int, name: str) -> None:
    """Require a positive integer count."""
    if isinstance(value, (bool, np.bool_)) or not isinstance(value, Integral):
        raise TypeError(f"{name} must be an integer.")
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def _numeric_series(series: pd.Series, name: str) -> pd.Series:
    if not isinstance(series, pd.Series):
        raise TypeError(f"{name} must be a pandas Series.")
    clean = series.dropna()
    if clean.empty:
        raise ValueError(f"{name} cannot be empty or contain only missing values.")
    if (
        not is_numeric_dtype(clean.dtype)
        or is_bool_dtype(clean.dtype)
        or is_complex_dtype(clean.dtype)
    ):
        raise TypeError(f"{name} must contain real numeric values.")
    clean = clean.astype(float)
    if not np.isfinite(clean.to_numpy()).all():
        raise ValueError(f"{name} must contain finite values.")
    return clean


def validate_returns(returns: pd.Series) -> pd.Series:
    """Drop missing observations; reject nonfinite values and returns below -1.

    A return of -1 is bankruptcy: compounded equity remains zero thereafter.
    Labels and order of retained observations are preserved.
    """
    clean = _numeric_series(returns, "returns")
    if (clean < -1).any():
        raise ValueError("simple returns cannot be below -100%.")
    return clean


def validate_return_pair(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> tuple[pd.Series, pd.Series]:
    """Require matching unique labels; align to portfolio order, drop NA pairs.

    Different label sets (even with equal lengths) and duplicate labels raise.
    Validate each input before pairwise deletion so infinities cannot be hidden.
    """
    portfolio = validate_returns(portfolio_returns)
    benchmark = validate_returns(benchmark_returns)
    if not portfolio_returns.index.is_unique or not benchmark_returns.index.is_unique:
        raise ValueError("paired return indices must be unique.")
    if (
        len(portfolio_returns) != len(benchmark_returns)
        or not portfolio_returns.index.isin(benchmark_returns.index).all()
    ):
        raise ValueError("paired returns must have matching index labels.")
    labels = portfolio.index[portfolio.index.isin(benchmark.index)]
    if labels.empty:
        raise ValueError("no complete paired observations remain.")
    return portfolio.loc[labels], benchmark.reindex(labels)


def validate_trade_results(trade_results: pd.Series) -> pd.Series:
    """Drop missing cash P&L; require finite numeric values without return bounds."""
    return _numeric_series(trade_results, "trade_results")


def compounded_equity(returns: pd.Series) -> pd.Series:
    """Compound validated returns from 1, rejecting numerical overflow.

    Zero equity is absorbing. No recapitalization is assumed after bankruptcy.
    """
    with np.errstate(over="ignore", invalid="ignore"):
        equity = (1 + returns).cumprod()
    bankrupt = np.flatnonzero(returns.to_numpy() == -1)
    if bankrupt.size:
        equity.iloc[bankrupt[0] :] = 0.0
    if not np.isfinite(equity.to_numpy()).all():
        raise ValueError("compounded equity exceeds finite numeric range.")
    return equity
