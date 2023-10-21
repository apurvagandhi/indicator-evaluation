
"""
Code implementing a TheoreticallyOptimalStrategy (details below). It should implement testPolicy(), which returns a trades data frame (see below).

Student Name: Apurva Gandhi
GT User ID: agandhi301
GT ID: 903862828
"""

import datetime as dt
from numpy import dtype
import pandas as pd
from util import get_data

def author():
    """
    : return: The GT username of the student
    : rtype: str
    """
    return "agandhi301"

def testPolicy(symbol="JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
    # Create a set of trades representing the best a strategy could possibly do during the in-sample period using JPM.
    # Read the symbol prices
    prices_df = get_data([symbol], pd.date_range(sd, ed)) 
    prices_df = prices_df[symbol]     
    # print(type(prices_df))
    # print(prices_df.index)
    # print(prices_df)    
    
    df_trades = pd.DataFrame(prices_df, index=prices_df.index)
    df_trades.drop(symbol, axis=1, inplace=True)
    df_trades["Order"] = None
    df_trades["Shares"] = 0
    df_trades["Symbol"] = symbol
    # print(df_trades)
    
    previous_order_shares = 0
    # for current_day in range(0,len(df_trades) - 1):
    counter = 0
    for date in df_trades.index:
        current_price = prices_df.iloc[counter]
        next_day_price = prices_df.iloc[counter + 1]
        if (counter < prices_df.shape[0] - 2):
            counter += 1
        # print("Current price is ", current_price, "Next day price is ", next_day_price)
        if current_price > next_day_price:
            # Current Price is higher than Next Day Price, indicating a price drop, so sell the stock.
            # print("selling and previous order share is ", previous_order_shares)
            df_trades.loc[date, "Order"] = "SELL"
            if previous_order_shares == 0:
                current_order_shares = -1000
            elif previous_order_shares == 1000:
                current_order_shares = -2000
            elif previous_order_shares == -1000: 
                current_order_shares = 0
        elif current_price < next_day_price:
            # Current Price is lower than Next Day Price, suggesting a price increase, so buy the stock.
            # print("buying")
            df_trades.loc[date, "Order"] = "BUY"
            if previous_order_shares == 0:
                current_order_shares = 1000
            elif previous_order_shares == -1000:
                current_order_shares = 2000
            elif previous_order_shares == 1000: 
                current_order_shares = 0
        else:
            # No significant price change, so do nothing.
            df_trades.loc[date, "Order"] = "NO TRADE"
            current_order_shares = 0
        
        df_trades.loc[date, "Shares"] = current_order_shares
        # print(df_trades.loc[date, symbol])
        previous_order_shares += current_order_shares
    # print(df_trades)
    return df_trades


def benchmark(symbol, sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009, 12, 31), sv=100000):
    """
    The performance of a portfolio starting with $100,000 cash, investing in 1000 shares of JPM, and holding that position. 
    """
    
    prices_df = get_data([symbol], pd.date_range(sd, ed)) 
    prices_df = prices_df[symbol]     

    
    df_trades = pd.DataFrame(prices_df, index=prices_df.index)
    df_trades.drop(symbol, axis=1, inplace=True)
    df_trades["Order"] = None
    df_trades["Shares"] = 0
    df_trades["Symbol"] = symbol

   
    benchmark_df = pd.DataFrame(prices_df, index=prices_df.index)
    benchmark_df.drop(symbol, axis=1, inplace=True)
    benchmark_df["Order"] = None
    benchmark_df["Shares"] = 0
    benchmark_df["Symbol"] = symbol
    benchmark_df.iloc[0] = ["BUY", 1000, symbol]
    return benchmark_df

def get_statistics(portfolio_values):
    daily_ret = portfolio_values.copy()
    daily_ret[1:] = (daily_ret[1:] / daily_ret[:-1].values) - 1
    daily_ret.loc[daily_ret.index[0]] = 0
    # return daily_rets

    cumulative_return = (portfolio_values[-1] / portfolio_values[0]) - 1
    average_daily_return = daily_ret[1:].mean()
    stdev_daily_return = daily_ret[1:].std()

    return cumulative_return, stdev_daily_return, average_daily_return