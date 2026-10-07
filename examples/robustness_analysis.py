"""Run from the repository root: python -m examples.robustness_analysis."""

import numpy as np
import pandas as pd

from quanttools import Backtest
from quanttools.statistics import drawdown_episodes, recovery_time
from quanttools.validation import iid_bootstrap


def main():
    # Synthetic monthly returns; no market downloads or trade execution.
    rng = np.random.default_rng(17)
    returns = pd.Series(
        rng.normal(0.008, 0.035, 60),
        index=pd.date_range("2020-01-01", periods=60, freq="MS"),
    )
    # An initial loss and exact equal-peak recovery: 0.8 * 1.25 = 1.0.
    returns.iloc[:2] = [-0.2, 0.25]
    # Cash P&L is separate and does not determine periodic compounding.
    trades = pd.Series([100.0, -60.0, 80.0, -30.0])
    bt = Backtest(returns, trades, periods_per_year=12, risk_free_rate=0.03)
    print(bt.report())
    print("Labeled drawdown episodes:")
    print(drawdown_episodes(returns).to_string(index=False))
    print("Deepest episode recovery count:", recovery_time(returns))
    print("Unrecovered example:", recovery_time(pd.Series([-0.2, 0.01])))

    options = dict(n_simulations=500, horizon=24, random_state=42)
    iid = iid_bootstrap(returns, periods_per_year=12, risk_free_rate=0.03, **options)
    repeated = bt.robustness(**options)
    pd.testing.assert_frame_equal(iid.metrics, repeated.metrics)
    blocks = bt.robustness(method="moving_block", block_size=3, **options)
    for name, result in [("IID", iid), ("Moving blocks", blocks)]:
        print(f"\n{name} percentile summaries:")
        print(result.summary)
        print(f"Probability ending below 1: {result.probability_of_loss:.2%}")
        print("Valid ending-equity count:", result.probability_valid_count)
    print("\nThese distributions are conditional on the sample, not forecasts.")


if __name__ == "__main__":
    main()
