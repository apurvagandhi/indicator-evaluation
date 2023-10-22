"""
This file should be considered the entry point to the project. The if “__name__” == “__main__”:
section of the code will call the testPolicy function in TheoreticallyOptimalStrategy, as well as your indicators and 
marketsimcode as needed, to generate the plots and statistics for your report (more details below).

Student Name: Apurva Gandhi
GT User ID: agandhi301
GT ID: 903862828
"""

import datetime as dt
from util import get_data
import matplotlib.pyplot as plt
import TheoreticallyOptimalStrategy as tos
import pandas as pd
from marketsimcode import compute_portvals
import indicators

def author():
    """
    : return: The GT username of the student
    : rtype: str
    """
    return "agandhi301"

def test_code():
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    start_value = 100000
    df_trades = tos.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
    # print(df_trades)
    trades_portfolio_value = compute_portvals(df_trades, 100000, 0.0, 0.0)
    cumulative_return, stdev_daily_return, average_daily_return = tos.get_statistics(trades_portfolio_value)
    trades_portfolio_value = trades_portfolio_value / trades_portfolio_value[0]
    print("trades cumulative_return", cumulative_return)
    print("trades tdev_daily_return" ,stdev_daily_return)
    print("trades average_daily_return", average_daily_return)
    # print(trades_portfolio_value)


    # print(trades_portfolio_value)
    df_benchmark = tos.benchmark(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
    benchMark_portfolio_value = compute_portvals(df_benchmark, 100000, 0, 0)
    cumulative_return, stdev_daily_return, average_daily_return = tos.get_statistics(benchMark_portfolio_value)
    benchMark_portfolio_value = benchMark_portfolio_value / benchMark_portfolio_value[0]
    print("\nbenchmark cumulative_return", cumulative_return)
    print("benchmark stdev_daily_return" ,stdev_daily_return)
    print("benchmark average_daily_return", average_daily_return)
    # print(benchMark_portfolio_value)
    
    plt.figure(figsize=(10, 5))
    plt.title("Benchmark vs. Theoretically Optimal Strategy")
    plt.xticks(rotation=20)
    plt.xlim(trades_portfolio_value.index.min(), trades_portfolio_value.index.max())
    plt.ylabel("Normalized Values")
    plt.plot(benchMark_portfolio_value, label="Benchmark", color="purple", lw=0.8)
    plt.plot(trades_portfolio_value, label="Theoretically Optimal Strategy", color="red", lw=0.8)
    plt.grid()
    plt.legend(loc="upper left")
    plt.savefig("figure1.png")
    plt.clf()


if __name__ == "__main__":
    pd.set_option('display.max_rows', None)  # Display all rows
    pd.set_option('display.max_columns', None)  # Display all columns
    test_code()
    indicators.test_code()
