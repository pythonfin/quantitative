#!/usr/bin/env python3
# pytest test_quantitative_basic.py

# third party imports
import pytest
import pandas as pd
import typing

# local application and library specifics imports
from basic.quantitative_basic import QuantitativeBeta


# set up test inputs by setting up a parameter dictionary for values
@pytest.mark.parametrize("yfinance_params", [
    {
        "ticker": ["HSBC"],
        "start_date": '2020-01-01',
        "periods": 1,
        "frequency": 'M',
        "interval": '1d',
        "index": "^GSPC",
        "results": 39.14
    },
    {
        "ticker": ["BP"],
        "start_date": '2020-01-01',
        "periods": 1,
        "frequency": 'M',
        "interval": '1d',
        "index": "^GSPC",
        "results": 38.04
    },
])
def test_load_data(yfinance_params: dict):
    """
    Ensure that yfinance loads basic values properly
    :param yfinance_params: All parameters required to be input to run the test
    :type yfinance_params: 'list'

    :yfinance_params:
        ticker (list['str']): list of the ticker symbol
        start_date (str): The start date in YYYY-MM-DD format.
        periods (int): number of time periods to be utilized
        frequency (str): Time span of future calculations
        intervals (str): Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
        index (str): comparative index to be used for beta calculations
        results (float): value of the stock ticker on the first period day noted
    """
    # set initial program parameters
    calculations = QuantitativeBeta(yfinance_params['ticker'])

    date_range = pd.date_range(yfinance_params['start_date'],
                               periods=yfinance_params['periods'],
                               freq=yfinance_params['frequency'])

    # load core data values
    calculations.load_data(index=yfinance_params['index'],
                           start=yfinance_params['start_date'],
                           end=date_range[-1],
                           interval=yfinance_params['interval'])

    assert round(calculations.yf_data[yfinance_params['ticker'][0]]['Open']
                 .values[0], 2) == yfinance_params['results']
