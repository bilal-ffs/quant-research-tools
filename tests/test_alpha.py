import pandas as pd
import pytest

from quanttools.portfolio import (
    alpha,
)


def test_alpha_returns_float():
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

    result = alpha(
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
        alpha(
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
        alpha(
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
        alpha(
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
        alpha(
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
        alpha(
            portfolio,
            benchmark,
        )
