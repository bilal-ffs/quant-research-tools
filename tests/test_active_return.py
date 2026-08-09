import pandas as pd
import pytest

from quanttools.portfolio import (
    active_return,
)


def test_active_return_returns_float():
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

    result = active_return(
        portfolio,
        benchmark,
    )

    assert isinstance(
        result,
        float,
    )


def test_empty_portfolio():
    portfolio = pd.Series(dtype=float)

    benchmark = pd.Series(
        [
            0.01,
            0.02,
        ]
    )

    with pytest.raises(ValueError):
        active_return(
            portfolio,
            benchmark,
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
        active_return(
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
        active_return(
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
        active_return(
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
        active_return(
            portfolio,
            benchmark,
        )
