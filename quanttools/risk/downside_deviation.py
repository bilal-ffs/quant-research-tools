"""
quanttools.risk.downside_deviation
==================================

Functions for calculating downside deviation.
"""

from __future__ import annotations

import pandas as pd

from quanttools.utils.validation import (
    validate_returns,
)


def downside_deviation(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
) -> float:
    """
    Calculate downside deviation.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    risk_free_rate : float, default=0.0
        Risk-free rate expressed as a decimal.

    Returns
    -------
    float
        Downside deviation.
    """

    returns = validate_returns(
        returns,
    )

    excess_returns = returns - risk_free_rate

    downside_returns = excess_returns[excess_returns < 0]

    if downside_returns.empty:
        return 0.0

    downside_deviation_value = downside_returns.std(
        ddof=1,
    )

    return float(
        downside_deviation_value,
    )
