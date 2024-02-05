#!/usr/bin/python
import yfinance as yf
import pandas as pd
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0].Symbol
tickers = tickers.to_list()
# change periods to dashes for yfinance
tickers = [item.replace(".", "-") for item in tickers]

price_df = yf.download(tickers,start='2010-01-01', end='2024-01-01')


def slice_df(symbol):
    sliced = price_df.copy()
    sliced = sliced[sliced.columns[sliced.columns.get_level_values(1) == symbol]]
    

    sliced.columns = sliced.columns.droplevel(1)
    sliced.loc[:,'price'] = sliced.Open.shift(-1)

    return sliced

def ma_calc(df,n,m):
    df['sma_1'] = df.Close.rolling(n).mean()
    df['sma_2'] = df.Close.rolling(m).mean()

def backtest(df,n,m):
    ma_calc(df,n,m)
    in_position = False
    profits = []

    for index, row in df.iterrows():
        
        if not in_position:
            if row.sma_1 > row.sma_2:
                buyprice = row.price
                in_position = True
        if in_position:
                if row.sma_1 < row.sma_2:
                    profit = (row.price - buyprice)/buyprice
                    profits.append(profit)
                    in_position = False

    gain = (pd.Series(profits) + 1).prod()   
    return gain         


#test = slice_df('MSFT')



results = []

for sym in tickers:
    subdf = slice_df(sym)
    gain = backtest(subdf, 50, 100)  # Call backtest once
    #print(f'Result for {sym}:  {gain}')
    results.append(gain)

# Convert 'results' to a pandas Series and calculate cumulative product
profits_series = pd.Series(results)
cumulative_product = profits_series.cumprod()

# Print the cumulative product
print(cumulative_product)



'''
for sym in tickers:
     subdf = slice_df(sym)
     #print(f'Result for {sym}:  {backtest(subdf,50,100)}')
     results.append(backtest(subdf,50,100))

profits = pd.DataFrame({'profit':results},index=tickers)

print(results.cumprod())
'''