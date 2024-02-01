#!/usr/bin/python

import yfinance as yf
import pandas as pd
import numpy as np

# read data into pandas from .xls getData.py generated for us
# This is to keep from repeatedly hitting yfinance for downloads since we are looking at monthly data.

index_data = pd.read_excel("testData.xls", index_col=0, sheet_name='indexData')

price_data = pd.read_excel("testData.xls", index_col=0, sheet_name='priceData')


index_data_sofi = np.log(index_data.Close / index_data.Close.shift(1))
index_data_sofi = index_data_sofi.to_frame()
index_data_sofi.columns = ['indexsofi']
index_data_sofi = index_data_sofi.bfill()


print(index_data)


# df['return'] = np.log(df.price / df.price.shift(1))    real sofi calculation