import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from math import sqrt

from scipy.optimize import minimize
from sklearn import preprocessing


def optimize_portfolio(
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 1, 1),
    syms=["GOOG", "AAPL", "GLD", "XOM"],
    gen_plot=False,
):

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

    def calc_portfolio(allocs, prices):
        df = prices.copy()
        df = df.divide(df.iloc[0], axis=1)
        df *= allocs
        df = df.sum(axis=1)
        return df

    def calc_sharpe_ratio(allocs, prices):
        # Creating portfolio
        df = calc_portfolio(allocs, prices)
        # Daily returns
        dr = (df[1:] / df[:-1].values) - 1

        # Average daily return
        adr = dr.mean()

        # STD daily returns
        sddr = dr.std()

        return sqrt(252) * (adr / sddr)

    allocs = np.ones(shape=len(prices.columns))
    allocs /= allocs.sum()

    cons = {"type": "eq", "fun": lambda x: 1 - sum(x)}
    bnds = tuple((0, 1) for x in allocs)

    min_result = minimize(
        lambda x: -1 * calc_sharpe_ratio(x, prices),
        allocs,
        method="SLSQP",
        bounds=bnds,
        constraints=cons,
    )
    min_allocs = min_result.x

    cr, adr, sddr, sr = [0.25, 0.001, 0.0005, 2.1]  # add code here to compute stats

    port_val = calc_portfolio(min_allocs, prices)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=["Portfolio", "SPY"], axis=1)
        df_temp["SPY"] = df_temp["SPY"].divide(df_temp["SPY"][0])

        df_temp.plot()
        plt.show()

    return min_allocs, cr, adr, sddr, sr


def test_code():
    start_date = dt.datetime(2009, 1, 1)
    end_date = dt.datetime(2010, 1, 1)
    symbols = ["GOOG", "AAPL", "GLD", "XOM", "IBM"]

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True
    )

    # Print statistics
    print("Start Date:", start_date)
    print("End Date:", end_date)
    print("Symbols:", symbols)
    print("Allocations:", allocations)
    print("Sharpe Ratio:", sr)
    print("Volatility (stdev of daily returns):", sddr)
    print("Average Daily Return:", adr)
    print("Cumulative Return:", cr)


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()

