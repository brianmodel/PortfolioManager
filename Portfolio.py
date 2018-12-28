from datetime import datetime
from enum import Enum
from math import sqrt
from dateutil import parser

import pandas as pd
from pandas_datareader import data
import numpy as np
import matplotlib.pyplot as plt


class Portfolio:
    def __init__(self, investment, tickers, allocs, buy_date):
        self.investment = investment
        self.buy_date = buy_date
        self.allocs = allocs

        self.data = self.load_data(tickers)
        self.sample_frequency = self.SampleFrequency.DAILY

        self.portfolio_value = self.calculate_portfolio_value()
        self.daily_returns = self.calculate_daily_returns()

    def calculate_portfolio_value(self):
        portfolio = self.data.copy()

        portfolio = portfolio[portfolio.index >= self.buy_date]

        portfolio = portfolio.divide(portfolio.iloc[0])
        portfolio = portfolio.multiply(self.allocs, axis=1)
        portfolio *= self.investment
        portfolio = portfolio.sum(axis=1)

        return portfolio

    def calculate_daily_returns(self):
        daily_ret = self.portfolio_value.copy()
        daily_ret[1:] = (daily_ret[1:] / daily_ret[:-1].values) - 1
        daily_ret.iloc[0] = 0
        return daily_ret

    def cumulitive_returns(self):
        return (self.portfolio_value[-1] / self.portfolio_value[0]) - 1

    def avg_daily_return(self):
        return self.daily_returns.mean()

    def risk(self):
        return self.daily_returns.std()

    def sharpe_ratio(self):
        avg = self.avg_daily_return()
        std = self.risk()
        ratio = sqrt(self.sample_frequency.value) * (avg / std)
        return ratio

    def bollinger_bands(self):
        mean = self.portfolio_value.rolling(window=20).mean()
        std = self.portfolio_value.rolling(window=20).std()
        self.portfolio_value.plot(label="Portfolio Value")
        mean.plot(label="Mean")
        (mean + 2*std).plot(label="Upper Band")
        (mean - 2*std).plot(label="Lower Band")

        plt.legend()
        plt.show()

    def daily_return_histogram(self):
        avg_daily = self.avg_daily_return()
        risk_std = self.risk()

        self.daily_returns.hist(bins=50)
        plt.axvline(avg_daily, linestyle="dashed", color="w")
        plt.axvline(risk_std, linestyle="dashed", color="r")
        plt.axvline(-risk_std, linestyle="dashed", color="r")

        plt.show()

    class SampleFrequency(Enum):
        DAILY = 252
        WEEKLY = 52
        ANNUALLY = 1

    def load_data(self, tickers):
        start = self.buy_date
        end = datetime.now().date()

        if isinstance(tickers, str):
            df = data.DataReader(tickers, "iex", start, end)
            df = df[["close"]]
            df.columns = [tickers]
            df.index.name = "Date"
            df.index = pd.to_datetime(df.index)

        elif isinstance(tickers, list):
            list_ = []
            for ticker in tickers:
                df = data.DataReader(ticker, "iex", start, end)
                df = df[["close"]]
                df.columns = [ticker]
                df.index.name = "Date"
                df.index = pd.to_datetime(df.index)
                df.columns = [ticker]

                list_.append(df)
            df = pd.concat(list_, axis=1)

        else:
            raise TypeError("Not a supported type")

        Portfolio.clean_data(df)
        return df

    @staticmethod
    def clean_data(df, fill=False):
        if fill:
            try:
                df.fillna(method="ffill", inplace=True)
                df.fillna(method="bfill", inplace=True)
            except TypeError:
                print("Must be a pandas dataframe")
        else:
            df.dropna(inplace=True)

        df.sort_index(axis=0, ascending=True, inplace=True)


if __name__ == "__main__":
    investment = 100
    tickers = ["AMZN", "AAPL"]
    allocs = [0.7, 0.3]
    portfolio = Portfolio(investment, tickers, allocs, "2015-10-13")

    print("Data: ")
    print(portfolio.data.head())
    print("")

    print("Portfolio Value: ")
    print(portfolio.portfolio_value.head())
    print(portfolio.portfolio_value.tail())
    print("")

    print("Daily return: ")
    print(portfolio.daily_returns.tail())
    print("")

    print("Cum return: ")
    print(portfolio.cumulitive_returns())
    print("")

    print("avg daily return: ")
    print(portfolio.avg_daily_return())
    print("")

    print("std daily return: ")
    print(portfolio.risk())
    print("")

    print("Sharpe ratio: ")
    print(portfolio.sharpe_ratio())
    print("")

    portfolio.daily_return_histogram()
    portfolio.bollinger_bands()
