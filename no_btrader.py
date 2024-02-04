#!/usr/bin/python

import pandas as pd
import yfinance as yf
import numpy as np


stock_data = pd.read_excel('stock_data_notranspose-2024-02-03.xlsx', index_col='Date', sheet_name='priceData')
# yfinance shows first day of month but it is last price of the month so we shift it 1
stock_data = stock_data.shift(1)
stock_data = stock_data.dropna()
stock_data = stock_data.bfill()
stock_data = stock_data.ffill()
stock_data = stock_data.astype(float)

print(stock_data.info())
# Calculate daily returns (pctchange)
return_df = stock_data.pct_change()
return_df = return_df.dropna()


# only caluating one colum for entire df?  We don't need to .prod(() until very end data os already monthly
#mnthly_ret = (return_df + 1).prod()
#mnthly_ret = mnthly_ret.to_frame()

profits = [] # keep track of profits
in_position = False # keep track of whether holding this stock or not

priceReturn_df = stock_data.join(return_df, lsuffix="_price", rsuffix="_sofi")

print(priceReturn_df)



#for index, row in priceReturn_df.iterrows():
   
'''
    if not in_position and row[A_sofi] > .14:
        buyprice = A_price
        in_position = True
        trailing_stop = buyprice * .90
    if in_position:
    
        if row.A_price * .90 >= trailing_stop:
            trailing_stop = A_price
        if row.A_price <= trailing_stop:
            sellprice = A_price
            profit = (sellprice-buyprice)/buyprice
            #print(f'Buy is: {buyprice}   | Sell is:  {sellprice}  Profit is: {profit}' ) 
            profits.append(profit)
            in_position = False
        
'''
print(profits)




