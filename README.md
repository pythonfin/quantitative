<b> Quantitative calculations </b>

Author: Matthew Wright, CPA, PSM, ACA <br> 

<br> This software creates quantitative based calculations with time series results in a graphical output format

To run this program:

    #1) Get poetry operational for your environment
    pip install poetry
    python -m poetry lock --no-update
    python -m poetry install
    
    #2) Running program
    For index argument, current options are:
    S&P 500 Index: "^GSPC"
    Dow Jones Industrial Average: "^DJI"
    Nasdaq Composite: "^IXIC"
    Russell 2000 Index: "^RUT"
    MSCI Emerging Markets Index: "^EEM"
    CBOE Volatility Index (VIX): "^VIX"

    For tickers, create a list of any NYSE stocks

    start_date: YYYY-MM-DD format

    date_range = YYYY-MM-DD format of end of first period
    periods= # of periods of comparison
    freq = Valid frequency intervals: 
    [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

Example output of:

    tickers_list = ["UL", "HSBC", "AZN", "BP", "VOD", "BHP", "GSK"]
    index = "^GSPC"
    start_date = '2020-01-01'
    date_range = pd.date_range('2021-01-31', periods=24, freq='M')
