#!/usr/bin/env python3
# python quantitative_basic.py
# Created by: Matthew Wright, CPA, PSM, ACA - pythonfin@proton.me
# Version: 1.0
# I am publishing this under an MIT license

# standard imports
from typing import Tuple, Any
from datetime import datetime

# third party imports
import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt

# local application imports


class QuantitativeCalcs:
    """
    Base class

    Parameters
    ----------
    self.yf_data : tuple
        Tuple[pd.DataFrame] containing the yf.download stock ticker data of time index
    self.tickers : list
        stock ticker symbols to be used in the calculations
        example: tickers = ["SCGLY", "BNPQY", "RNLSY", "LRLCY", "SBGSY", "VEOEY"]
    """

    def __init__(self, tickers):
        self.yf_data = tuple()
        self.tickers = tickers

    def load_data(self, index: str, **kwargs: Any):
        """
        Important to only dl and load the data as needed to maximize efficiency

        Retrieves historical data for the tickers and ^GSPC in a single call
        yf.download relies on a string of tickers separated by space ie/ 'SCGLY PFE'

        Args:
            :param index: comparative index to be used for beta calculations
            :type index: "str"

            :param kwargs: Optional arguments to be passed to the yf.download function.

            :Keyword Arguments:
                start (str): The start date in YYYY-MM-DD format.
                end (str): The end date in YYYY-MM-DD format.
                group_by (str): specifies how to group the downloaded data
                    (e.g. "ticker" for ticker symbol grouping, "column" to group by data column)
                interval = '1d' : The time interval period to be used in beta calculations
                    Valid intervals: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
                auto_adjust (bool): automatically adjust the calculations (default is True)
                prepost (bool): include pre-market and after-hours trading data (default is False)
                threads (int) specifying the number of threads to use for the download (default is 1)

        Returns:
            None: This just loads the df data into self.yf_data

        Raises:
            ValueError: If ticker isn't found, or if there is error with the data retrieval

        Example:
            >>> self.load_data("^GSPC", start='2020-01-01', end='2020-12-31', interval='1d')
        """
        try:
            stock_str = " ".join(self.tickers)

            data: Tuple[pd.DataFrame] = yf.download(stock_str + " " + index, **kwargs, group_by='ticker')

            # Check if the data isn't empty
            if data.empty:
                raise ValueError("yf.download didn't complete correctly for the ticker list")

            # Check if index data is available
            if index not in data:
                raise KeyError(f"Data for the {index} wasn't loaded")

            self.yf_data = data

        except (KeyError, ValueError) as e:
            print("Error:", e)
            return None

        except Exception as e:
            print("Unknown error:", e)
            return None


class QuantitativeBeta(QuantitativeCalcs):
    """ Commence with the basic quantitative analysis questions """
    def __init__(self, tickers):
        super().__init__(tickers)
        self.betas = []

    def prepare_beta_calculations(self, index: str, date_range: pd.DatetimeIndex, start: str):
        """
        complete all the beta calculation preparations

        Args:
            :param index: comparative index to be used for beta calculations
            :type index: "str"

            :param start: start date for this segment of beta calculations
            :type start: "str"

            :param date_range: Pandas df of the entirety of the date time index to be iterated over
            :type date_range: "pd.DatetimeIndex"

        Returns:
            dict: The beta values for the tickers, in two decimal places

        Raises:
            ValueError: If ticker isn't found, or if there is error with the data retrieval
            KeyError: If the ticker wasn't loaded within the yf.download
        """
        try:
            df_betas = []

            # Verify that the date range isn't empty
            if date_range.empty:
                raise ValueError("no date range - empty DateTimeIndex")

            for end_date in date_range:
                betas = self._calculate_beta(index=index, start=start, end=end_date)

                df = pd.DataFrame(betas, index=[end_date])
                df_betas.append(df)

                print(f'\ncurrent date is {end_date}')
                for ticker, beta_val in betas.items():
                    print(f'Ticker: {ticker} - with a beta of {beta_val}')

            self.betas = pd.concat(df_betas)

        except ValueError as e:
            print(f"Error: {e}")

        except Exception as e:
            print("Unknown error:", e)
            return None

    def _calculate_beta(self, index: str, start: str, end: str) -> dict[str, float] | None:
        """
        beta: measure of a stock's volatility in relation to the overall market (typical metric SP500)
        Calculate the beta for a given stock symbol

        Args:
            :param index: comparative index to be used for beta calculations
            :type index: "str"

            :param start: start date for this segment of beta calculations
            :type start: "str"

            :param end: end date for this segment of beta calculations
            :type end: "str"

        Returns:
            dict: The beta values for the tickers, in two decimal places

        Raises:
            ValueError: If ticker isn't found, or if there is error with the data retrieval
            KeyError: If the ticker wasn't loaded within the yf.download
        """

        try:
            betas_dict = {}

            # Use boolean mask with the pd.DataFrame.loc method to slice DataFrame by date range.
            # It's faster than .loc accessor as you avoid creating a df copy, rather done on original df

            mask = (self.yf_data.index >= start) & (self.yf_data.index <= end)
            df_yf_data = self.yf_data.loc[mask]

            # perform error checking
            if df_yf_data.empty:
                raise ValueError("yf.download didn't complete correctly for the ticker list")

            if index not in df_yf_data:
                raise KeyError(f"Data for the {index} wasn't loaded")

            # Calculate index returns using vectorized operations
            # ex EOD index[day + 1] value / EOD index [day] value - 1  gives  daily % return
            sp500_returns = df_yf_data[index]['Adj Close'] \
                .values[1:] / df_yf_data[index]['Adj Close'].values[:-1] - 1

            for ticker in self.tickers:
                if ticker not in df_yf_data:
                    raise KeyError(f"data for {ticker} wasn't loaded")

                # Calculate daily returns using vectorized operations
                stock_returns = df_yf_data[ticker]['Adj Close'] \
                    .values[1:] / df_yf_data[ticker]['Adj Close'].values[:-1] - 1

                # Verify sufficient return data to perform the beta calculations
                if len(stock_returns) < 2 or len(sp500_returns) < 2:
                    raise ValueError(f"Cannot calculate beta for {ticker} - lacking sufficient data")

                # Calculate the stock's beta
                # beta = covariance (stock's return relative to market) / variance (of the market's return)
                beta = np.cov(stock_returns, sp500_returns)[0, 1] / np.var(sp500_returns)

                betas_dict[ticker] = round(beta, 2)

            return betas_dict

        except (KeyError, ValueError) as e:
            print("Error:", e)
            return None

        except Exception as e:
            print("Unknown error:", e)
            return None

    def plot_betas(self):
        """
        Utilizing the current beta values, creates an output chart of betas using matplotlib
        and will plot the values from the self.tickers
        """

        try:
            # Check that df is a valid DataFrame
            if not isinstance(self.betas, pd.DataFrame):
                print("Error: calculate_beta.betas isn't a DataFrame")
                return None

            plt.plot(self.betas.index, self.betas)

            plt.title('Stock Beta over time')
            plt.xlabel('Date')
            plt.ylabel('Beta')

            plt.legend(self.tickers, loc='lower left')

            # Create a datetime stamp in the format "YYYY-MM-DD_HH-MM-SS" and save .png of beta results
            now = datetime.now()
            datetime_stamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            save_str = 'output/beta_' + datetime_stamp + '.png'

            plt.savefig(save_str)

        except Exception as e:
            print(f'Error: {e}')
            return None
