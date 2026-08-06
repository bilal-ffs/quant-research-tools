"""
quanttools.statistics.max_drawdown
=================================

Functions for calculating drawdown-related performance metrics.

Description
-----------
Provides utilities to calculate:

- Maximum Drawdown
- Drawdown Series

References
----------
- Magdon-Ismail & Atiya (2004)
- Empyrical (Quantopian)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

def max_drawdown(
    returns: pd.Series,
) -> float:
  """
Calculate the maximum drawdown of a return series.

Parameters
----------
returns : pandas.Series
    Periodic returns expressed as decimal values.
    Example:
    0.01 = +1%
   -0.02 = -2%

Returns
-------
float
    Maximum drawdown expressed as a negative decimal.

Raises
------
TypeError
    If returns is not a pandas Series.

ValueError
    If the series is empty.

Examples
--------
>>> max_drawdown(returns)
-0.1432
"""
