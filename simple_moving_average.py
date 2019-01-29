#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 15:26:06 2019

@author: maninder
"""


import pandas as pd
import numpy as np
from pandas_datareader import data

#download the price data from the first trading day in 2000, until today, for the S&P500 from Yahoo Finance
sp500 = data.DataReader('^GSPC', 'yahoo',start='1/1/2000')

# checking the format of the data
print (sp500)
sp500.head()

# plotting a graph of the closing prices to see how the S&P has performed over the period.
sp500['Close'].plot(grid=True,figsize=(8,5))


#creating a moving average and simultaneously append them to new columns in our existing sp500 DataFrame.
#Below code both creates the series and automatically adds them to our DataFrame
sp500['42d'] = np.round(sp500['Close'].rolling(window=42).mean(),2)
sp500['252d'] = np.round(sp500['Close'].rolling(window=252).mean(),2)

sp500.tail

#ploting the closing prices and moving averages together

sp500[['Close','42d','252d']].plot(grid=True,figsize=(8,5))

#devise a rule to generate our trading signals.
#1) Buy Signal (go long) – the 42d moving average is for the first time X points above the 252d tend.
#2) Park in Cash – no position.
#3) Sell Signal (go short) – the 42d moving average is for the first time X points below the 252d trend.

#add new column to sp500
sp500['42-252'] = sp500['42d'] - sp500['252d']
    
#formalise the signals by adding a further column which we will call Stance. We also set our signal threshold ‘X’ to 50 (this is somewhat arbitrary and can be optimised at some point)

X = 50
sp500['Stance'] = np.where(sp500['42-252'] > X, 1, 0)
sp500['Stance'] = np.where(sp500['42-252'] < X, -1, sp500['Stance'])
sp500['Stance'].value_counts()


sp500['Market Returns'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
sp500['Strategy'] = sp500['Market Returns'] * sp500['Stance'].shift(1)

	
sp500[['Market Returns','Strategy']].cumsum().plot(grid=True,figsize=(8,5))