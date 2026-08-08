"""
quanttools.reports.performance
==============================

Functions for generating performance reports.
"""

from __future__ import annotations

import pandas as pd

from quanttools.statistics import (
    average_loss,
    average_win,
    cagr,
    calmar_ratio,
    drawdown_duration,
    expectancy,
    max_drawdown,
    payoff_ratio,
    profit_factor,
    sharpe_ratio,
    sortino_ratio,
    win_rate,
)


def performance_report(
    returns: pd.Series,
    trade_results: pd.Series,
) -> str:
    """
    Generate a performance report.

    Parameters
    ----------
    returns : pandas.Series
        Periodic returns.

    trade_results : pandas.Series
        Profit and loss values for completed trades.

    Returns
    -------
    str
        Formatted performance report.
    """

    # Performance

    cagr_value = cagr(returns)

    sharpe = sharpe_ratio(returns)

    sortino = sortino_ratio(returns)

    calmar = calmar_ratio(returns)

    # Risk

    max_dd = max_drawdown(returns)

    dd_duration = drawdown_duration(returns)

    # Trade Analytics

    pf = profit_factor(trade_results)

    exp = expectancy(trade_results)

    wr = win_rate(trade_results)

    avg_win = average_win(trade_results)

    avg_loss = average_loss(trade_results)

    payoff = payoff_ratio(trade_results)

    return f"""
    ==================================================
            QuantTools Performance Report
    ==================================================

    Performance Metrics
    --------------------------------------------------
    CAGR                     {cagr_value:>10.2%}
    Sharpe Ratio             {sharpe:>10.2f}
    Sortino Ratio            {sortino:>10.2f}
    Calmar Ratio             {calmar:>10.2f}

    Risk Metrics
    --------------------------------------------------
    Maximum Drawdown         {max_dd:>10.2%}
    Drawdown Duration        {dd_duration:>10}

    Trade Analytics
    --------------------------------------------------
    Profit Factor            {pf:>10.2f}
    Expectancy               {exp:>10.2f}
    Win Rate                 {wr:>10.2%}
    Average Win              {avg_win:>10.2f}
    Average Loss             {avg_loss:>10.2f}
    Payoff Ratio             {payoff:>10.2f}

    ==================================================
    """
