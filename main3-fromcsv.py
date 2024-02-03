#!/usr/bin/python

import yfinance as yf
import pandas as pd
import numpy as np
import backtrader as bt
import backtrader.analyzers as btanalyzers
import matplotlib.pyplot as plt
import seaborn as sns
#plt.style.use('seaborn')


# use these to calculate for indicator...i think.
index_data = pd.read_csv("gspc.csv", index_col=0)
price_data = pd.read_csv("A.csv", index_col=0)

class MaCrossStrategy(bt.Strategy):
 
    params = (
        ('fast_length', 5),
        ('slow_length', 25), 
        ('vix_level', 30)
    )
     
    def __init__(self):
        ma_fast = bt.ind.SMA(period = self.params.fast_length)
        ma_slow = bt.ind.SMA(period = self.params.slow_length)
         
        self.crossover = bt.ind.CrossOver(ma_fast, ma_slow)
        self.vix = self.data1.close
 
    def next(self):
        if not self.position:
            if self.crossover > 0 and self.vix < self.params.vix_level: 
                self.buy()
        elif self.crossover < 0: 
            self.close()

cerebro = bt.Cerebro()

GSPC = bt.feeds.YahooFinanceCSVData(
            dataname='gspc.csv',
            reverse = False
)

A = bt.feeds.YahooFinanceCSVData(
            dataname='A.csv',
            reverse = False
)
CSCO = bt.feeds.YahooFinanceCSVData(
            dataname='CSCO.csv',
            reverse = False
)

cerebro.adddata(A)

# if this is data1 (vix in example above), what if it is custom csv import of sp500 6mma instead of vix and we divide in strategy loop?
cerebro.adddata(GSPC)

cerebro.addstrategy(MaCrossStrategy, fast_length = 5, slow_length = 25, vix_level = 999)

cerebro.broker.setcash(100000.0)

cerebro.addanalyzer(btanalyzers.SharpeRatio, _name = "sharpe")
cerebro.addanalyzer(btanalyzers.Returns,     _name = "returns")

# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run over everything
back = cerebro.run()

cerebro.broker.getvalue()
 
back[0].analyzers.sharpe.get_analysis()['sharperatio']
back[0].analyzers.returns.get_analysis()['rnorm100']


# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())










    




