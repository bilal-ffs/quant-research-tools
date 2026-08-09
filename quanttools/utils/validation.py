"""
quanttools.utils.validation
===========================

Shared validation utilities.
"""

from __future__ import annotations

import pandas as pd


def validate_returns(
    returns: pd.Series,
) -> pd.Series:
    """
    Validate a return series.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    Returns
    -------
    pandas.Series
        Return series with missing values removed.

    Raises
    ------
    TypeError
        If returns is not a pandas Series.

    ValueError
        If returns is empty or contains only missing values.
    """

    if not isinstance(returns, pd.Series):
        raise TypeError("returns must be a pandas Series.")

    if returns.empty:
        raise ValueError("returns cannot be empty.")

    returns = returns.dropna()

    if returns.empty:
        raise ValueError("returns contains only missing values.")

    return returns


def validate_return_pair(
    portfolio_returns: pd.Series,
    benchmark_returns: pd.Series,
) -> tuple[pd.Series, pd.Series]:
    """
    Validate two return series.

    Parameters
    ----------
    portfolio_returns : pandas.Series
        Portfolio periodic returns.

    benchmark_returns : pandas.Series
        Benchmark periodic returns.

    Returns
    -------
    tuple[pandas.Series, pandas.Series]
        Validated return series with missing values removed.

    Raises
    ------
    TypeError
        If either input is not a pandas Series.

    ValueError
        If either series is empty.

    ValueError
        If the series have different lengths.
    """

    portfolio_returns = validate_returns(
        portfolio_returns,
    )

    benchmark_returns = validate_returns(
        benchmark_returns,
    )

    if len(portfolio_returns) != len(benchmark_returns):
        raise ValueError("return series must have the same length.")

    return (
        portfolio_returns,
        benchmark_returns,
    )


def validate_trade_results(
    trade_results: pd.Series,
) -> pd.Series:
    """
    Validate a trade result series.

    Parameters
    ----------
    trade_results : pandas.Series
        Profit and loss values.

    Returns
    -------
    pandas.Series
        Clean trade result series.

    Raises
    ------
    TypeError
        If trade_results is not a pandas Series.

    ValueError
        If trade_results is empty or contains only missing values.
    """

    if not isinstance(
        trade_results,
        pd.Series,
    ):
        raise TypeError("trade_results must be a pandas Series.")

    if trade_results.empty:
        raise ValueError("trade_results cannot be empty.")

    trade_results = trade_results.dropna()

    if trade_results.empty:
        raise ValueError("trade_results contains only missing values.")

    return trade_results
