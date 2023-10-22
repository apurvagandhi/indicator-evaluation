import datetime as dt

from matplotlib import dates, ticker
import numpy as np
from util import get_data
import matplotlib.pyplot as plt
import pandas as pd
'''
Code implementing your indicators as functions that operate on DataFrames. There is no defined API for indicators.py, 
but when it runs, the main method should generate the charts that will illustrate your indicators in the report.

Student Name: Apurva Gandhi
GT User ID: agandhi301
GT ID: 903862828
'''
# Helper Function
def calculate_rolling_mean(values, window_size):
    return values.rolling(window_size).mean()

# Helper Function
def calculate_rolling_std(values, window_size):
    return values.rolling(window_size).std()

# Indicator 1 - Simple Moving Average
def calculate_simple_moving_average(prices, window_size = 10):
    simple_moving_average = calculate_rolling_mean(prices, window_size)
    return simple_moving_average

# Indicator 2 - Bollinger band
def calculate_bollinger_bands(values, window_size=10, num_std_dev=2):
    rolling_mean = calculate_rolling_mean(values, window_size)
    rolling_std = calculate_rolling_std(values, window_size)
    upper_band = rolling_mean + rolling_std * num_std_dev
    lower_band = rolling_mean - rolling_std * num_std_dev
    return upper_band, lower_band

#Indicator 3 - Momentum 
def calculate_momentum(values, window_size = 10):
    return (values / values.shift(window_size)) - 1
    
# Indicator 4 - Commodity Channel Index - CCI 
def calculate_commodity_channel_index(values, window_size=10):
    rolling_mean = calculate_rolling_mean(values, window_size)
    rolling_std = calculate_rolling_std(values, window_size)
    scaling_factor = 2 / rolling_std
    return (values - rolling_mean) / (scaling_factor * rolling_std)

# Indicator 5 - Moving Average Convergence Divergence (MACD)
def calculate_moving_average_convergence_divergence(values, short_period = 12, long_period = 26, signal_period = 9):    
    # Calculate the short-term EMA
    short_ema = values.ewm(ignore_na=False, span=short_period, adjust=True).mean()
    # Calculate the long-term EMA
    long_ema = values.ewm(ignore_na=False, span=long_period, adjust=True).mean()
    # Calculate the MACD line
    macd_line = short_ema - long_ema
    # Calculate the signal line (9-period EMA of MACD)
    signal_line = macd_line.ewm(ignore_na=False, span=signal_period, adjust=True).mean()
    return macd_line, signal_line
    
def test_code():
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    symbol = "JPM"
    prices_df = get_data([symbol], pd.date_range(start_date, end_date))[symbol]
    normalized_prices_df = prices_df/prices_df[0]
    
    # Indicator 1 Graph
    sma1 = calculate_rolling_mean(normalized_prices_df, 20)
    sma2 = calculate_rolling_mean(normalized_prices_df, 100)
    fig = plt.figure(figsize=(10, 6))
    plt.title("Simple Moving average")
    plt.ylabel("Normalized Price")
    plt.xlabel("Date")
    plt.plot(normalized_prices_df, label="JPM Prices", color="blue", lw=0.8)
    plt.plot(sma1, label="window size 20", color="purple", lw=0.8)
    plt.plot(sma2, label="window size 100", color="red", lw=0.8) 
    plt.grid(which='both', axis='both')
    plt.tick_params(axis='x', which='major', labelsize=10)
    fig.autofmt_xdate()
    plt.legend(loc="best", frameon=True)
    plt.savefig("sma.png")
    plt.clf()
    
    # Indicator 2 Graph
    upper_band, lower_band = calculate_bollinger_bands(normalized_prices_df,20)
    bollinger_band_percentage = (normalized_prices_df - lower_band) / (upper_band - lower_band)
    fig = plt.figure(figsize=(10, 5))
    plt.title("Bollinger Bands")
    plt.xticks(rotation=20)
    plt.ylabel("Normalized Values")
    plt.xlabel("Date")
    plt.plot(normalized_prices_df, label="prices", color="blue", lw=0.8)
    plt.plot(upper_band, label="Bollinger Band Upper Band", color="purple", lw=0.8)
    plt.plot(lower_band, label="Bollinger Band Lower Band", color="red", lw=0.8)
    plt.grid(which='both', axis='both', linestyle="--")
    plt.tick_params(axis='x', which='major', labelsize=10)
    fig.autofmt_xdate()
    plt.legend(loc="best", frameon=True)
    plt.savefig("bollinger.png")
    plt.clf()
    
    fig = plt.figure(figsize=(10, 5))
    plt.title("Bollinger Bands Percentage")
    plt.xticks(rotation=20)
    plt.ylabel("Percentage")
    plt.xlabel("Date")
    plt.plot(bollinger_band_percentage, label="bollinger band percentage", color="purple", lw=0.8)
    plt.grid(which='both', axis='both', linestyle="--")
    plt.tick_params(axis='x', which='major', labelsize=10)
    fig.autofmt_xdate()
    plt.legend(loc="best", frameon=True)
    plt.savefig("bollinger_2.png")
    plt.clf()
    
    # Indicator 3 Graph
    momentum = calculate_momentum(normalized_prices_df, 20)
    fig = plt.figure(figsize=(10, 6))
    plt.title("Momentum")
    plt.ylabel("Momentum")
    plt.xlabel("Date")
    plt.plot(normalized_prices_df, label="JPM Prices", color="blue", lw=0.8)
    # left, right = plt.xlim()
    # plt.xticks(np.arange(left, right, 60), rotation=10)
    plt.plot(momentum, label="Momentum", color="purple", lw=0.8)
    plt.grid(which='both', axis='both', linestyle="--")
    plt.tick_params(axis='x', which='major', labelsize=10)
    plt.axhline(y=0, color="red", lw=0.5)
    plt.legend(loc="best", frameon=True)
    fig.autofmt_xdate()
    plt.savefig("momentum.png")
    plt.clf()
    
    # Indicator 4 Graph
    cci = calculate_commodity_channel_index(normalized_prices_df)
    fig = plt.figure(figsize=(10, 6))
    plt.title("Commodity Channel Index")
    plt.ylabel("CCI")
    plt.xlabel("Date")
    plt.plot(cci, label="CCI", color="purple", lw=0.8)
    plt.plot(normalized_prices_df, label="JPM Prices", color="blue", lw=0.8)
    plt.grid(which='both', axis='both', linestyle="--")
    plt.tick_params(axis='x', which='major', labelsize=10)
    plt.axhline(y=0, color="red", lw=0.5)
    plt.legend(loc="best", frameon=True)
    fig.autofmt_xdate()
    plt.savefig("cci.png")
    plt.clf()
    
    # Indicator 5 Graphs
    macd_line, signal_line = calculate_moving_average_convergence_divergence(normalized_prices_df)
    fig = plt.figure(figsize=(10, 6))
    plt.suptitle("Moving Average Convergence Divergence")
    ax1 = plt.subplot(211)
    plt.grid(which='both', axis='both', linestyle="--")
    plt.tick_params(axis='x', which='major', labelsize=10)
    plt.ylabel("MACD")
    plt.xlabel("Date")
    ax1.plot(macd_line, label="MACD", color="purple", lw=0.8)
    ax1.plot(signal_line, label="Signal Line", color="blue", lw=0.8)
    plt.legend(loc="best", frameon=True)
    
    short_ema = normalized_prices_df.ewm(ignore_na=False, span=12, adjust=True).mean()
    long_ema = normalized_prices_df.ewm(ignore_na=False, span=26, adjust=True).mean()
    ax2 = plt.subplot(212)
    plt.ylabel("EMA")
    plt.xlabel("Date")
    plt.tick_params(axis='x', which='major', labelsize=10)
    plt.grid(which='both', axis='both', linestyle="--")
    plt.plot(normalized_prices_df, label="JPM Prices", color="blue", lw=0.8)
    ax2.plot(short_ema, label="Short EMA", color="purple", lw=0.8)
    ax2.plot(long_ema, label="Long EMA", color="orange", lw=0.8)
    plt.legend(loc="best", frameon=True)
    fig.autofmt_xdate()
    plt.savefig("macd.png")
    plt.clf()
    

if __name__ == "__main__":
    pd.set_option('display.max_rows', None)  # Display all rows
    pd.set_option('display.max_columns', None)  # Display all columns
    test_code()
