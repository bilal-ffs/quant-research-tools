"""
quanttools.risk.ulcer_index
===========================

Functions for calculating the Ulcer Index.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from quanttools.statistics.drawdown import drawdown_series


def ulcer_index(
    returns: pd.Series,
) -> float:
    """
    Calculate the Ulcer Index.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    Returns
    -------
    float
        Ulcer Index.
    """

    drawdown = drawdown_series(returns)

    squared_drawdowns = drawdown**2

    ulcer = np.sqrt(squared_drawdowns.mean())

    return float(
        ulcer,
    )
