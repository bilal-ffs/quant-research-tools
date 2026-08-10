"""
quanttools.risk.ulcer_index
===========================

Functions for calculating the Ulcer Index.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from quanttools.utils.validation import (
    validate_returns,
)


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

    returns = validate_returns(
        returns,
    )

    equity_curve = (1 + returns).cumprod()

    running_peak = equity_curve.cummax()

    drawdown = equity_curve / running_peak - 1

    squared_drawdowns = drawdown**2

    ulcer = np.sqrt(squared_drawdowns.mean())

    return float(
        ulcer,
    )
