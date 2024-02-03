#!/usr/bin/python

import yfinance as yf
import pandas as pd
import numpy as np
import backtrader as bt
import backtrader.analyzers as btanalyzers
import matplotlib.pyplot as plt
import seaborn as sns
#plt.style.use('seaborn')


# read data into pandas from .xls getData.py generated for us
# This is to keep from repeatedly hitting yfinance for downloads since we are looking at monthly data and likley run may times during testing.
index_data = pd.read_excel("testData.xls", index_col=0, sheet_name='indexData')
price_data = pd.read_excel("testData.xls", index_col=0, sheet_name='priceData')
'''
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

# what is the percentage change from one month to the next of ratio_6mma?

ratio_change = ratio_6mma.bfill().pct_change().round(3)
ratio_change = ratio_change.bfill()


# drop first 5 rows as they will always be NaN due to rolling mean above.  This is our indicator for backtesting..I hope.
#ratio_6mma = ratio_6mma.iloc[5:]

# lets dump everyting to a spreadsheet to spot check numbers/calculations manually
#with pd.ExcelWriter('spotTest.xls', engine="openpyxl") as writer:
#    price_data.to_excel(writer, sheet_name="priceData")
#    index_data.to_excel(writer, sheet_name="indexData")
#    price_data_sofi.to_excel(writer, sheet_name="sofi")
#    index_data_sofi.to_excel(writer, sheet_name="indexSofi")
#    price_6mma.to_excel(writer, sheet_name="6mma")
#    index_6mma.to_excel(writer, sheet_name="index6mma")
#    ratio_6mma.to_excel(writer, sheet_name="ratio6mma")
#    ratio_change.to_excel(writer, sheet_name="ratiopctChange")
'''
class CustomData(bt.feeds.PandasData):

    lines = ('open', 'high', 'low', 'close', 'volume', 'openinterest')
    params = (
                ('datetime', -1),  # Use -1 for automatic detection or specify the column name if needed
                ('open', 'open'),
                ('high', 'high'),
                ('low', 'low'),
                ('close', 'close'),
                ('volume', 'volume'),
                ('openinterest', -1),
    )

class testStrategy(bt.Strategy):
    def __init__(self):
        pass
    def next(self):
        pass

class testclose(bt.Strategy):
    def __init__(self):
        pass
    def next(self):
        dataclose = self.datas[0].close[0]
        print(dataclose)

class testLog(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[1].close
    def log(self,txt):
        dt = self.datas[1].datetime.datetime()
        print(f'{dt}  |  {txt}')
    def next(self):
        x = self.dataclose[0]
        self.log(txt=x)

class smaStrategy(bt.Strategy):

    params = (
        ('fast_length',  5),
        ('slow_length', 25)
    )
    def __init__(self):

        self.crossovers = []

        for d in self.datas:
           
            ma_fast = bt.ind.SMA(d, period = self.params.fast_length)
            ma_slow = bt.ind.SMA(d, period = self.params.slow_length)

            self.crossovers.append(bt.ind.CrossOver(ma_fast, ma_slow))
            
    
    def next(self):
        for i, d in enumerate(self.datas):
            # Get the current value of the crossover indicator
            crossover_value = self.crossovers[i][0]
            
            if not self.getposition(d).size:
                #print(f'Crossover value for {d._name}: {crossover_value}')
                if self.crossovers[i] > 0:
                    print('Buy')
                    self.buy(data=d)
            elif self.crossovers[i] < 0:
                self.close(data=d)
        



cerebro = bt.Cerebro()



for ticker in price_data.columns:
    # Prepare the data for the current ticker
    stock_data = price_data[[ticker]].copy()
    stock_data.index = pd.to_datetime(stock_data.index)  # Ensure the index is datetime

    stock_data.rename(columns={ticker: 'close'}, inplace=True)
    stock_data['open'] = stock_data['high'] = stock_data['low'] = stock_data['close']
    stock_data['volume'] = 0

    # Convert the DataFrame to a format Backtrader can use
    #print(stock_data)
    data = CustomData(dataname=stock_data)
    
    cerebro.adddata(data, name=ticker)
    



cerebro.broker.set_cash(100000)
cerebro.addstrategy(smaStrategy)
cerebro.addsizer(bt.sizers.PercentSizer, percents=5)
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')


cerebro.run()
print(cerebro.broker.getvalue())

#cerebro.plot()











    




