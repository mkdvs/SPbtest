#!/usr/bin/python

import pandas as pd
import yfinance as yf


stock_data = pd.read_excel('stock_data_notranspose-2024-02-03.xlsx', index_col='Date', sheet_name='priceData')
# yfinance shows first day of month but it is last price of the month so we shift it 1
stock_data = stock_data.shift(1)
stock_data = stock_data.dropna()
stock_data = stock_data.bfill()
stock_data = stock_data.ffill()
# Calculate daily returns (pctchange)
return_df = stock_data.pct_change()
return_df = return_df.dropna()


# only caluating one colum for entire df?  We don't need to .prod(() until very end data os already monthly
#mnthly_ret = (return_df + 1).prod()
#mnthly_ret = mnthly_ret.to_frame()

profits = [] # keep track of profits
in_position = False # keep track of whether holding this stock or not



for index, row in return_df.iterrows():
    if not in_position and row.A > .10:
        buyprice = row.A
        #in_position = True
        print(buyprice)



