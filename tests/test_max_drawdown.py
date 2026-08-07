import pandas as pd
import pytest

from quanttools.statistics.drawdown import max_drawdown


def test_max_drawdown_returns_correct_value():
    returns = pd.Series(
        [
            0.10,
            -0.20,
            0.05,
        ]
    )

    result = max_drawdown(returns)

    assert result == pytest.approx(-0.20)

def test_empty_series():
    returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        max_drawdown(returns)    

def test_invalid_input_type():
    with pytest.raises(TypeError):
        max_drawdown(
            [
                0.10,
                -0.20,
                0.05,
            ]
        )
def test_series_with_nan_values():
    returns = pd.Series(
        [
            0.10,
            None,
            -0.20,
            0.05,
        ]
    )

    result = max_drawdown(returns)

    assert isinstance(result, float)