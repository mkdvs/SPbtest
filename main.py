#!/usr/bin/python

import yfinance as yf
import pandas as pd
import numpy as np

# read data into pandas from .xls getData.py generated for us
# This is to keep from repeatedly hitting yfinance for downloads since we are looking at monthly data and likley run may times during testing.
index_data = pd.read_excel("testData.xls", index_col=0, sheet_name='indexData')
price_data = pd.read_excel("testData.xls", index_col=0, sheet_name='priceData')

# calculate change in index prices
index_data_sofi = np.log(index_data / index_data.shift(1))
index_data_sofi.columns = ['indexsofi']
# backfill so the first month's change is zero instead of 0 to x difference.
index_data_sofi = index_data_sofi.bfill()

# calculate changes in stock prices (priceData sheet)
price_data_sofi = np.log(index_data / index_data.shift(1))
price_data_sofi = price_data_sofi.bfill()

print(index_data_sofi)



