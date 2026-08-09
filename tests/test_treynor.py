import pandas as pd
import pytest

from quanttools.portfolio import (
    treynor_ratio,
)


def test_treynor_returns_float():
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

    result = treynor_ratio(
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
        treynor_ratio(
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
        treynor_ratio(
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
        treynor_ratio(
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
        treynor_ratio(
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
        treynor_ratio(
            portfolio,
            benchmark,
        )


def test_zero_beta():
    portfolio = pd.Series(
        [
            0.01,
            0.01,
            0.01,
        ]
    )

    benchmark = pd.Series(
        [
            0.00,
            0.00,
            0.00,
        ]
    )

    with pytest.raises(ValueError):
        treynor_ratio(
            portfolio,
            benchmark,
        )
