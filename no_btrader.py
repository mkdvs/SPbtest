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


###########  HAVE TO GET PRICES FROM STOCK_DATA TO CALCULATE PROFIT.  WE ARE ITERATING OVER RETURNS!!
for index, row in return_df.iterrows():
    if not in_position and row.A > 0:
        buyprice = row.A
        in_position = True
        trailing_stop = buyprice * .90
    if in_position:
        if row.A * .90 >= trailing_stop:
            trailing_stop = row.A
        if row.A <= trailing_stop:
            sellprice = row.A
            print(sellprice)
            profit = (sellprice-buyprice)/buyprice    
            profits.append(profit)
            in_position = False

#print(profits)




