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

# This is to just create some trades to see if it is working
# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] < self.dataclose[-1]:
                    # current close less than previous close

                    if self.dataclose[-1] < self.dataclose[-2]:
                        # previous close less than the previous close

                        # BUY, BUY, BUY!!! (with default parameters)
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy()




class MaCrossStrategy(bt.Strategy):
 
    params = (
        ('fast_length', 5),
        ('slow_length', 25), 
        ('vix_level', 999)
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
            reverse = False,
            #timeframe = bt.TimeFrame.Months
)
CSCO = bt.feeds.YahooFinanceCSVData(
            dataname='CSCO.csv',
            reverse = False
)


# resampling replaces adddata
cerebro.resampledata(A, timeframe=bt.TimeFrame.Months)
#cerebro.adddata(A)


# if this is data1 (vix in example above), what if it is custom csv import of sp500 6mma instead of vix and we divide in strategy loop?
# https://quantnomad.com/using-multiple-datasets-in-backtraders-strategies/
#cerebro.adddata(GSPC)

#cerebro.addstrategy(MaCrossStrategy, fast_length = 5, slow_length = 25, vix_level = 999)
cerebro.addstrategy(TestStrategy)
cerebro.broker.setcash(100000.0)

#cerebro.addanalyzer(btanalyzers.SharpeRatio, _name = "sharpe")
#cerebro.addanalyzer(btanalyzers.Returns,     _name = "returns")

# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())




# Run over everything
cerebro.run()

cerebro.broker.getvalue()
 
#print(back[0].analyzers.sharpe.get_analysis()['sharperatio'])
#back[0].analyzers.returns.get_analysis()['rnorm100']


# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()








    




