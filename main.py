#!/usr/bin/env python3
# python main.py
# Created by: Matthew Wright, CPA, PSM, ACA - pythonfin@proton.me
# Version: 1.0.0
# I am publishing this under an MIT license

# standard imports

# third party imports
import pandas as pd

# local application imports
from basic.quantitative_basic import QuantitativeBeta


if __name__ == '__main__':

    # set initial program parameters
    tickers_list = ["SCGLY", "BNPQY", "RNLSY", "LRLCY", "SBGSY", "VEOEY"]
    calculations = QuantitativeBeta(tickers_list)

    index = "^GSPC"
    start_date = '2020-01-01'
    date_range = pd.date_range('2021-01-31', periods=24, freq='M')

    # load core data values
    calculations.load_data(index=index, start=start_date, end=date_range[-1], interval='1d')

    # perform calculations
    calculations.prepare_beta_calculations(index=index, date_range=date_range, start=start_date)

    # output results
    calculations.plot_betas()
