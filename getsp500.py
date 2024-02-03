#!/usr/bin/python

import yfinance as yf
import pandas

sp500Index_data = yf.download('^GSPC','2022-10-17', '2023-11-20', auto_adjust=True)

sp500Index_data.to_csv('gspc.csv')

