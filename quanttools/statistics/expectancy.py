"""
quanttools.statistics.expectancy
================================

Functions for calculating trade expectancy.

References
----------
Van K. Tharp
"""

from __future__ import annotations

import pandas as pd


def expectancy(
    trade_results: pd.Series,
) -> float:
    """
    Calculate trade expectancy.

    Parameters
    ----------
    trade_results : pandas.Series
        Profit and loss values for completed trades.

    Returns
    -------
    float
        Expected profit or loss per trade.
    """
    raise NotImplementedError
