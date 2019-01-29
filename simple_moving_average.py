# Using  S&P500 data for the assignment. 

#importing required modules

import pandas as pd
import numpy as np
from pandas_datareader import data

#download the price data from the first trading day in 2000, until today, for the S&P500 from Yahoo Finance
equity = data.DataReader('^GSPC', 'yahoo',start='1/1/2000')

# checking the format of the data
print (equity)
equity.head()
equity.tail()

# plotting a graph of the closing prices to see S&P's performance over the period.
equity['Close'].plot(grid=True,figsize=(8,5))


#Creating two moving averages and simultaneously append them to new columns in our existing equity DataFrame.
#Below code both creates the series and automatically adds them to our DataFrame
equity['42d'] = np.round(equity['Close'].rolling(window=42).mean(),2)
equity['252d'] = np.round(equity['Close'].rolling(window=252).mean(),2)

#checking out the data from the bottom.
equity.tail

#ploting the closing prices and moving averages together

equity[['Close','42d','252d']].plot(grid=True,figsize=(8,5))

#Creating a rule to generate our trading signals.
#1) Buy Signal - the 42d moving average is for the first time X points above the 252d tend.
#2) Park in Cash – no position.
#3) Sell Signal (go short) – the 42d moving average is for the first time X points below the 252d trend.

#add new column to equity to find the difference 
equity['42-252'] = equity['42d'] - equity['252d']
    
#formalise the signals by adding a further column which we will call Postition. We also set our signal threshold ‘X’ to 50

X = 50
equity['Postition'] = np.where(equity['42-252'] > X, 1, 0)
equity['Postition'] = np.where(equity['42-252'] < X, -1, equity['Postition'])

# Below code will show that for the time period we have chosen to backtest, on 2077 trading dates the 42d moving average lies more than 50 points below the 252d moving average, and on 1865 the 42d moving average lies more than 50 points above the 252d moving average.
equity['Postition'].value_counts()


