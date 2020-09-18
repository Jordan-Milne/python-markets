# python-markets <a href="url"><img src="https://static.thenounproject.com/png/2064110-200.png" align="right" height="78"></a>

### Work in Progress
Web app for analyzing stocks using python and dash! Check out what I have done so far at [**this link**](https://python-stock-analyzer.herokuapp.com/). *This is web-app is deployed on heroku so the server usually takes 30-60 seconds to turn on (disadvantage of free teir)*


## How It's Made:

**Dash is a productive Python framework for building web applications made by the creators of *plotly*. Written on top of Flask, Plotly.js, and React.js, Dash is ideal for building data visualization apps with highly custom user interfaces in pure Python. It's particularly suited for anyone who works with data in Python.**

1. Stock data is imported using the python package yfinance
2. Stock price data is handled in a DataFrame using pandas
3. The dash framework allows for in app 'callbacks' so the app can have inputs (stock ticker symbol) and outputs (updating graphs using stock data).
