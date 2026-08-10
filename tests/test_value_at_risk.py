import pandas as pd
import pytest

from quanttools.risk import (
    value_at_risk,
)


def test_value_at_risk_returns_float():
    returns = pd.Series(
        [
            0.01,
            -0.02,
            0.03,
            -0.01,
            0.02,
        ]
    )

    result = value_at_risk(
        returns,
    )

    assert isinstance(
        result,
        float,
    )


def test_empty_returns():
    returns = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        value_at_risk(
            returns,
        )


def test_invalid_input():
    with pytest.raises(TypeError):
        value_at_risk(
            [
                0.01,
                0.02,
            ],
        )


def test_nan_values():
    returns = pd.Series(
        [
            0.01,
            None,
            -0.02,
            0.03,
        ]
    )

    result = value_at_risk(
        returns,
    )

    assert isinstance(
        result,
        float,
    )


def test_invalid_confidence_level():
    returns = pd.Series(
        [
            0.01,
            -0.02,
            0.03,
        ]
    )

    with pytest.raises(ValueError):
        value_at_risk(
            returns,
            confidence_level=1.5,
        )


def test_invalid_negative_confidence_level():
    returns = pd.Series(
        [
            0.01,
            -0.02,
            0.03,
        ]
    )

    with pytest.raises(ValueError):
        value_at_risk(
            returns,
            confidence_level=-0.5,
        )
