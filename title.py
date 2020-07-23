import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import yfinance as yf


app = dash.Dash()

app.layout = html.Div(children=[
html.H1('Hello Dash!'),
html.Div('Dash: Web Dashboards with python'),
dcc.Graph(id='example',
            figure={'data':[
            {'x':[1,2,3],'y':[4,1,2],'type':'bar','name':'SF'},
            {'x':[1,2,3],'y':[2,4,5],'type':'bar','name':'NYC'}
            ],
                    'layout':{
                    'title':'BAR PLOTS!'
                    }})
])

if __name__ == '__main__':
    app.run_server()







def chart(symbol, date_range):
    name = yf.Ticker(symbol)
    data = name.history(period=date_range)
    data['date'] = data.index
    data = data.reset_index(drop=True)


    fig = px.line(data, x='date', y='Close')
    fig.show()



chart('AMZN','2y')

def comparison(symbol,symbol2, date_range):
    name = yf.Ticker(symbol)
    data = name.history(period=date_range)
    data['date'] = data.index
    data = data.reset_index(drop=True)
    data['name'] = str(symbol)
    data['percent'] = (data['Close']/data['Close'].iloc[0])-1

    stock2 = yf.Ticker(str(symbol2)).history(period=date_range)
    stock2['date'] = stock2.index
    stock2 = stock2.reset_index(drop=True)
    stock2['name'] = str(symbol2)
    stock2['percent'] = (stock2['Close']/stock2['Close'].iloc[0])-1

    df = pd.concat([data,stock2])


    fig = px.scatter(df, x='date', y='percent', color='name')
    fig.update_xaxes(
        rangebreaks=[
            dict(bounds=["sat", "mon"]), #hide weekends
        ]
    )

    fig.show()


comparison('AMZN','AAPL', '1mo')
