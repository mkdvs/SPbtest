#!/usr/bin/python
import pandas as pd
import matplotlib.pyplot as plt


df  = pd.read_csv('CSCO.csv')
df = df.rename(columns={"Adj Close": "AdjClose"})
df['price'] = df.AdjClose.shift(-1)
df['daily_return'] = df.AdjClose.pct_change()
df = df.dropna()

profits = []
in_position = False

for index, row in df.iterrows():
    if not in_position and row.daily_return > 0:
        buyprice = row.price
        in_position = True
        trailing_stop = buyprice * 0.98
    if in_position:
        if row.AdjClose * 0.98 >= trailing_stop:
            trailing_stop = row.AdjClose * 0.98
        if row.AdjClose <= trailing_stop:
            sellprice = row.price
            profit = (sellprice-buyprice)/buyprice
            profits.append(profit)
            in_position = False

ts = (pd.Series(profits) + 1).cumprod()
tr = (pd.Series(profits) + 1).prod()
print(tr)
ts.plot()

plt.show()


