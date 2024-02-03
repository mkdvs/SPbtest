#!/usr/bin/python

import yfinance as yf
import pandas as pd
import numpy as np
import backtrader as bt
import backtrader.analyzers as btanalyzers
import matplotlib.pyplot as plt
import seaborn as sns







class MaCrosstrategy(bt.Strategy):

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
            #print(f'Crossover value for {d._name}: {crossover_value}')
            if not self.getposition(d).size:
                
                
                if self.crossovers[i] > 0:
                    self.buy(data=d)
            elif self.crossovers[i] < 0:
              
                self.close(data=d)
        



cerebro = bt.Cerebro()

stocks = ['AAPL', 'MSFT', 'TSLA']
for s in stocks:
    data = bt.feeds.PandasData(dataname = yf.download(s,'2015-07-06', '2021-07-01', auto_adjust=True))
    cerebro.adddata(data, name=s)

  
    


cerebro.broker.set_cash(100000)
cerebro.addstrategy(MaCrosstrategy)
cerebro.addsizer(bt.sizers.PercentSizer, percents=10)
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(bt.analyzers.Returns, _name='myreturn')



cerebro.run()
print(cerebro.broker.get_value())





#thestrats = cerebro.run()
#thestrat = thestrats[0]

#print(thestrat.analyzers.myreturn.get_analysis())


#cerebro.plot()

