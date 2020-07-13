import pandas as pd
import plotly.express as px
import yfinance as yf

# NASDAQ = yf.Ticker("^IXIC").history(period="max")
# NASDAQ['date'] = NASDAQ.index
# NASDAQ = NASDAQ.reset_index(drop=True)
#
# name = yf.Ticker(symbol)
# data = name.history(period="max")
# data['date'] = data.index
# data = data.reset_index(drop=True)

def chart(symbol, date_range):
    name = yf.Ticker(symbol)
    data = name.history(period=date_range)
    data['date'] = data.index
    data = data.reset_index(drop=True)


    fig = px.line(data, x='date', y='Close')
    fig.show()



chart('AMZN','2y')
