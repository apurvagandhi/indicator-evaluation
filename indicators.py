import datetime as dt
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
def calculate_commodity_channel_index(values, window_size):
    rolling_mean = calculate_rolling_mean(values, window_size)
    rolling_std = calculate_rolling_std(values, window_size)
    scaling_factor = 2 / rolling_std
    return (values - rolling_mean) / (scaling_factor * rolling_std)

# Indicator 5 - Moving Average Convergence Divergence (MACD)
def calculate_moving_average_convergence_divergence(values, short_period = 12, long_period = 26,signal_period = 9):    
    # Calculate the short-term EMA
    short_ema = values.ewm(ignore_na=False, span=short_period, min_period = 0, adjust=True).mean()
    # Calculate the long-term EMA
    long_ema = values.ewm(ignore_na=False, span=long_period, adjust=True).mean()
    # Calculate the MACD line
    macd_line = short_ema - long_ema
    # Calculate the signal line (9-period EMA of MACD)
    signal_line = macd_line.ewm(ignore_na=False, span=signal_period, min_period = 0, adjust=True).mean()
    return macd_line, signal_line
    
def test_code():
    start_date = dt.datetime(2008, 1, 1)
    end_date = dt.datetime(2009, 12, 31)
    symbol = "JPM"
    prices_df = get_data([symbol], pd.date_range(start_date, end_date)) 
    prices_df = prices_df[symbol]  
    
if __name__ == "__main__":
    pd.set_option('display.max_rows', None)  # Display all rows
    pd.set_option('display.max_columns', None)  # Display all columns
    test_code()
