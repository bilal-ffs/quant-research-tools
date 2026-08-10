"""
quanttools.risk.value_at_risk
=============================

Functions for calculating historical Value at Risk.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from quanttools.utils.validation import (
    validate_returns,
)


def value_at_risk(
    returns: pd.Series,
    confidence_level: float = 0.95,
) -> float:
    """
    Calculate historical Value at Risk (VaR).

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    confidence_level : float, default=0.95
        Confidence level.

    Returns
    -------
    float
        Historical Value at Risk expressed as a positive loss.
    """

    returns = validate_returns(
        returns,
    )

    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1.")

    percentile = (1 - confidence_level) * 100

    var = np.percentile(
        returns,
        percentile,
    )

    return float(-var)
