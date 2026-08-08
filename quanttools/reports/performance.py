"""
quanttools.reports.performance
==============================

Functions for generating performance reports.
"""

from __future__ import annotations

import pandas as pd


def performance_report(
    returns: pd.Series,
    trade_results: pd.Series,
) -> str:
    """
    Generate a performance report.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    trade_results : pandas.Series
        Profit and loss values for completed trades.

    Returns
    -------
    str
        Formatted performance report.
    """
    raise NotImplementedError