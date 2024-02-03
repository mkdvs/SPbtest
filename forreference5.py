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
        stock_ma1 = bt.ind.SMA(self.dataclose, period=6)
        stock_ma2 = bt.ind.SMA(self.dataclose, period=6)
        # Use line delay notation (-x) to get a ref to the -1 point
        self.ma1_pct = stock_ma1 / stock_ma1(-1) -1  # same as (y2-y1)/y1 this is % change of 6mma of the stock
        #ma2_pct = stock_ma2 / stock_ma2(-1) - 1.0  # The ma2 percentage part




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
        #self.log('Close, %.2f' % self.dataclose[0])
        self.log(self.ma1_pct[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            
            if self.ma1_pct[0] < 0:
                # previous close less than the previous close

                # BUY, BUY, BUY!!! (with default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()
            else:

                # Already in the market ... we might sell
                if len(self) >= (self.bar_executed + 5):
                    # SELL, SELL, SELL!!! (with all possible default parameters)
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell()



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


# CANNOT RESAMPLE MONTHLY SINCE IT BUYS AT NEXT BAR WHICH WOULD BE 1 MONTH LATER
#cerebro.resampledata(A, timeframe=bt.TimeFrame.Months)

#cerebro.resampledata(GSPC, timeframe=bt.TimeFrame.Months)
cerebro.adddata(A)


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








    




