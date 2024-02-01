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
price_data_sofi = np.log(price_data / price_data.shift(1))
price_data_sofi = price_data_sofi.bfill()

# now need 6 month moving average of index and each stock to begin building our indicator.

index_6mma = index_data_sofi.rolling(window=6).mean()
price_6mma = price_data_sofi.rolling(window=6).mean()

# Divide each column in price_6mma by the single column in index_6mma
# The division will automatically broadcast across the columns
ratio_6mma = price_6mma.divide(index_6mma['indexsofi'], axis=0)
# drop first 5 rows as they will always be NaN due to rolling mean above.  This is our indicator for backtesting..I hope.
ratio_6mma = ratio_6mma.iloc[5:]

# lets dump everyting to a spreadsheet to spot check numbers/calculations manually

with pd.ExcelWriter('spotTest.xls', engine="openpyxl") as writer:
    price_data.to_excel(writer, sheet_name="priceData")
    index_data.to_excel(writer, sheet_name="indexData")
    price_data_sofi.to_excel(writer, sheet_name="sofi")
    index_data_sofi.to_excel(writer, sheet_name="indexSofi")
    price_6mma.to_excel(writer, sheet_name="6mma")
    index_6mma.to_excel(writer, sheet_name="index6mma")
    ratio_6mma.to_excel(writer, sheet_name="ratio6mma")
    




