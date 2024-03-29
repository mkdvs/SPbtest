#!/usr/bin/python3
import yfinance
import requests
import bs4 as bs
import pandas as pd
import numpy as np


stock_data = []
my_index_data = []

#### Select 1 month prior to the month you want to begin.  This is to fix Yfdownload returning end of month price with first of month date.
start_date = "2019-12-01"
end_date = "2024-01-01"


# load sp500 index data into dataframe from yfinance
def get_index_data():
    index_ticker = '^GSPC'
    # yfinance date format is YYYY-MM-DD
    my_index_data = yfinance.download(index_ticker,start=start_date, end=end_date, interval="1mo",actions=False,rounding=True,auto_adjust=True)['Close']
    return my_index_data


# load sp500 tickers into a list
def get_wiki_tickers():
    # Download sp500 ticker symbols from Wikipedia and write to a list
    resp = requests.get('http://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'wikitable sortable'})
    
    sptickers = []

    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[0].text
        sptickers.append(ticker)
        sptickers = [s.replace('\n', '') for s in sptickers]
        sptickers = [s.replace(".", "-") for s in sptickers] # Yahoo Finance uses dashes instead of dots so we have to change it here

    return sptickers

# Function to replace values that are more than double or less than half of the previous value
def replace_large_jumps(series):
    for i in range(1, len(series)):
        if series.iloc[i] > 2 * series.iloc[i - 1] or series.iloc[i] < 0.5 * series.iloc[i - 1]:
            series.iloc[i] = series.iloc[i - 1]
    return series

index_values = get_index_data()
index_values = index_values.to_frame()

#causing problems with btrader
#index_values.index = index_values.index.strftime('%m-%d-%Y')


ticker = get_wiki_tickers()
# yfinance date format is YYYY-MM-DD
my_price_data = yfinance.download(ticker,start=start_date, end=end_date, interval="1mo",actions=False,rounding=True,auto_adjust=True)['Close']
# fill null values with the last known price
my_price_data.ffill(inplace=True)
# Backward fill to fill any remaining NaN values at the beginning of the data
my_price_data.bfill(inplace=True)
# reformat date of date index column
# causing problems with dtrader
#my_price_data.index = my_price_data.index.strftime('%m-%d-%Y')

# Fix price anomolies
my_price_data = my_price_data.apply(replace_large_jumps, axis=0)

# Fix dates - yf.download give price for last day of the month but date is first day of the month
index_values = index_values.shift(1)
my_price_data = my_price_data.shift(1)
# drop the first row since it is blank due to shift(1)
index_values = index_values.iloc[1:]
my_price_data = my_price_data.iloc[1:]


# Write our cleaned data to an excel file for main.py to use
filename = "testData.xls"

with pd.ExcelWriter(filename, engine="openpyxl") as writer:
    my_price_data.to_excel(writer, sheet_name="priceData")
    index_values.to_excel(writer, sheet_name="indexData")
  
