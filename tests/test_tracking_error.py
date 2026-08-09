import pandas as pd
import pytest

from quanttools.portfolio import (
    tracking_error,
)


def test_tracking_error_returns_float():
    portfolio = pd.Series(
        [
            0.02,
            -0.01,
            0.03,
            0.01,
            -0.02,
        ]
    )

    benchmark = pd.Series(
        [
            0.01,
            -0.02,
            0.02,
            0.00,
            -0.01,
        ]
    )

    result = tracking_error(
        portfolio,
        benchmark,
    )

    assert isinstance(
        result,
        float,
    )


def test_empty_benchmark():
    portfolio = pd.Series(
        [
            0.01,
            0.02,
        ]
    )

    benchmark = pd.Series(dtype=float)

    with pytest.raises(ValueError):
        tracking_error(
            portfolio,
            benchmark,
        )


def test_invalid_portfolio():
    benchmark = pd.Series(
        [
            0.01,
            0.02,
        ]
    )

    with pytest.raises(TypeError):
        tracking_error(
            [
                0.01,
                0.02,
            ],
            benchmark,
        )


def test_invalid_benchmark():
    portfolio = pd.Series(
        [
            0.01,
            0.02,
        ]
    )

    with pytest.raises(TypeError):
        tracking_error(
            portfolio,
            [
                0.01,
                0.02,
            ],
        )


def test_length_mismatch():
    portfolio = pd.Series(
        [
            0.01,
            0.02,
            0.03,
        ]
    )

    benchmark = pd.Series(
        [
            0.01,
            0.02,
        ]
    )

    with pytest.raises(ValueError):
        tracking_error(
            portfolio,
            benchmark,
        )
