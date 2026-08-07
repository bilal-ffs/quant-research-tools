"""
quanttools.statistics.calmar
============================

Functions for calculating the Calmar Ratio.

References
----------
- Terry W. Young (1991)
"""

from __future__ import annotations

import pandas as pd

from quanttools.statistics.cagr import cagr
from quanttools.statistics.drawdown import max_drawdown

from quanttools.utils.validation import (
    validate_returns,
)


def calmar_ratio(
    returns: pd.Series,
    periods_per_year: int = 252,
) -> float:
    """
    Calculate the annualized Calmar Ratio.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    periods_per_year : int, default=252
        Number of return observations per year.

    Returns
    -------
    float
        Annualized Calmar Ratio.
    """
    # Step 1: Validate input

    returns = validate_returns(
        returns
    )
    # Step 2: Compute CAGR

    growth = cagr(
        returns,
        periods_per_year=periods_per_year,
    )
    # Step 3: Compute maximum drawdown

    drawdown = max_drawdown(
        returns
    )
    # Step 4: Validate drawdown

    if drawdown == 0:
        raise ValueError(
            "maximum drawdown is zero."
        )