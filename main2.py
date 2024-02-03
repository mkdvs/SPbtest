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



class smaStrategy(bt.Strategy):

    params = (
        ('fast_length',  5),
        ('slow_length', 25)
    )
    def __init__(self):

        self.crossovers = []
        self.dataclose = self.datas[0].close

        for d in self.datas:
           
            ma_fast = bt.ind.SMA(d, period = self.params.fast_length)
            ma_slow = bt.ind.SMA(d, period = self.params.slow_length)

            self.crossovers.append(bt.ind.CrossOver(ma_fast, ma_slow))

    def log(self,txt,dt=None):
        dt = dt or self.datas[0].datetime.date(0)  
    
    def next(self):
        for i, d in enumerate(self.datas):
            # Get the current value of the crossover indicator
            crossover_value = self.crossovers[i][0]
            
            if not self.getposition(d).size:
                #print(f'Crossover value for {d._name}: {crossover_value}')
                self.log('close, %.2f' % self.dataclose[0])
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
    
    data = CustomData(dataname=stock_data)
    
    cerebro.adddata(data, name=ticker)
    



cerebro.broker.set_cash(100000)
cerebro.addstrategy(smaStrategy)
cerebro.addsizer(bt.sizers.PercentSizer, percents=5)
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')


cerebro.run()
print(cerebro.broker.getvalue())

#cerebro.plot()











    




