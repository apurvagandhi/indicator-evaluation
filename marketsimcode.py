""""""  		  	   		  		 		  		  		    	 		 		   		 		  
"""MC2-P1: Market simulator.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 		  		  		    	 		 		   		 		  
Atlanta, Georgia 30332  		  	   		  		 		  		  		    	 		 		   		 		  
All Rights Reserved  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Template code for CS 4646/7646  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 		  		  		    	 		 		   		 		  
works, including solutions to the projects assigned in this course. Students  		  	   		  		 		  		  		    	 		 		   		 		  
and other users of this template code are advised not to share it with others  		  	   		  		 		  		  		    	 		 		   		 		  
or to make it available on publicly viewable websites including repositories  		  	   		  		 		  		  		    	 		 		   		 		  
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 		  		  		    	 		 		   		 		  
or edited.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
We do grant permission to share solutions privately with non-students such  		  	   		  		 		  		  		    	 		 		   		 		  
as potential employers. However, sharing with other current or future  		  	   		  		 		  		  		    	 		 		   		 		  
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 		  		  		    	 		 		   		 		  
GT honor code violation.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
-----do not edit anything above this line---  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
Student Name: Apurva Gandhi  	   		  		 		  		  		    	 		 		   		 		  
GT User ID: agandhi301		  	   		  		 		  		  		    	 		 		   		 		  
GT ID: 903862828			  	   		  		 		  		  		    	 		 		   		 		  
"""  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
from matplotlib import pyplot as plt  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
import pandas as pd
from util import get_data, plot_data  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
def compute_portvals(trades, start_val=100000, commission=0, impact=0):  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    Computes the portfolio values.  		  	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		  
    :param orders_file: Path of the order file or the file object  		  	   		  		 		  		  		    	 		 		   		 		  
    :type orders_file: str or file object  		  	   		  		 		  		  		    	 		 		   		 		  
    :param start_val: The starting value of the portfolio  		  	   		  		 		  		  		    	 		 		   		 		  
    :type start_val: int  		  	   		  		 		  		  		    	 		 		   		 		  
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		  		 		  		  		    	 		 		   		 		  
    :type commission: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		  		 		  		  		    	 		 		   		 		  
    :type impact: float  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: pandas.DataFrame  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   	
    ### Step 1 		 		  		  		    	 		 		   		 		    		 		  		  		    	 		 		   		 		  
    # read in the orders file
    orders_df = trades  
    # read in the dates for the orders 
    orders_df = orders_df.sort_index()
    start_date = orders_df.index[0]		  	   		  		 		  		  		    	 		 		   		 		  
    end_date = orders_df.index[-1] 
    dates = pd.date_range(start_date, end_date)	 
    # Get symbols for the orders		
    symbols = orders_df["Symbol"].unique()
    # Read in adjusted closing prices for given symbols, date range  	   		
    prices_df = get_data(symbols, dates)  
    prices_df = prices_df.sort_index()
    # Just the spy 		
    df_prices_SPY = prices_df['SPY']	  	
    # Remove spy	 		  		  		    	 		 		   		 		  
    prices_df = prices_df[symbols]  
     # Add cash column
    prices_df['Cash'] = 1.0  
    
    ### Step 2
    trades_df  = prices_df.copy()
    trades_df[symbols] = 0
    trades_df['Cash'] = 0
    
    ### Step 3
    for index, order_row in orders_df.iterrows():
        number_of_shares = int(order_row["Shares"])
        price_of_share = prices_df.loc[index][order_row["Symbol"]]
        if order_row['Order'] == 'SELL':
            trades_df.loc[index, order_row["Symbol"]] += number_of_shares * 1
            trades_df.loc[index, "Cash"] += number_of_shares * price_of_share * -1
        elif order_row['Order'] == 'BUY':
            trades_df.loc[index, order_row["Symbol"]] += number_of_shares * 1
            trades_df.loc[index, "Cash"] += number_of_shares * price_of_share * -1
        else:
            continue
    ### Step 4   
    holdings_df  = trades_df.copy()
    for count, (index, holdings_df_row) in enumerate(holdings_df.iterrows()):
        if count == 0:
            holdings_df.loc[index, "Cash"] +=  start_val
            prev_index = index
        else: 
            holdings_df.loc[index, :] +=  holdings_df.loc[prev_index, :]
            prev_index = index
    
    ### Step 5    
    values_df = holdings_df.copy()
    values_df = prices_df * holdings_df

    # Step 6
    portfolio_value = values_df.sum(axis=1)
    return portfolio_value  		  	   		  		 		  		  		    	 		 		   		 		  
  		
def author():  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    :return: The GT username of the student  		  	   		  		 		  		  		    	 		 		   		 		  
    :rtype: str  		  	   		  		 		  		  		    	 		 		   		 		  
    """  		  	   		  		 		  		  		    	 		 		   		 		  
    return "agandhi301"	   		  		 		  		  		    	 		 		   		 		  
  		  	   		  		 		  		  		    	 		 		   		 		