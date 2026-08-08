def profit_factor(
    trade_results: pd.Series,
) -> float:
    """
    Calculate the Profit Factor.

    Parameters
    ----------
    trade_results : pandas.Series
        Profit and loss values for completed trades.

    Returns
    -------
    float
        Profit Factor.

    Raises
    ------
    TypeError
        If trade_results is not a pandas Series.

    ValueError
        If trade_results is empty.

    Examples
    --------
    >>> profit_factor(trade_results)
    1.85
    """

    # Step 1: Validate input

    if not isinstance(
        trade_results,
        pd.Series,
    ):
        raise TypeError(
            "trade_results must be a pandas Series."
        )

    if trade_results.empty:
        raise ValueError(
            "trade_results cannot be empty."
        )

    trade_results = trade_results.dropna()

    if trade_results.empty:
        raise ValueError(
            "trade_results contains only missing values."
        )

    # Step 2: Separate winning and losing trades

    winning_trades = trade_results[
        trade_results > 0
    ]

    losing_trades = trade_results[
        trade_results < 0
    ]

    # Step 3: Compute gross profit and gross loss

    gross_profit = winning_trades.sum()

    gross_loss = abs(
        losing_trades.sum()
    )

    # Step 4: Validate gross loss

    if gross_loss == 0:
        raise ValueError(
            "gross loss is zero."
        )

    # Step 5: Compute Profit Factor

    profit_factor = (
        gross_profit / gross_loss
    )

    return float(
        profit_factor
    )
