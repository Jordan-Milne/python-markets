import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime
import yfinance as yf

from get_all_tickers import get_tickers as gt
list_of_tickers = gt.get_tickers()


tickerz = []
for i in list_of_tickers:
    new_dict = {}
    new_dict['label'] = i
    new_dict['value'] = i
    tickerz.append(new_dict)


app = dash.Dash()

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([html.H3('Enter a stock symbol:', style={'paddingRight':'30px'}),
    dcc.Dropdown(
        id='my_ticker_symbol',
        options=tickerz,
        value=['GOLF'],
        multi=True
    )], style={'display':'inline-block', 'verticalAlign':'top','width':'30%'}),
    html.Div([
        html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed = datetime(1950, 1, 1),
            max_date_allowed = datetime.today(),
            start_date = datetime(2018, 1, 1),
            end_date = datetime.today()
        )
    ], style={'display':'inline-block'}),

    html.Div([
            html.Button(id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':24,'marginLeft':'30px'}

    )
    ],style={'display':'inline-block'}),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    ),
    dcc.Markdown(''' --- ''')
])
@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button','n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def update_graph(n_clicks,stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    for tic in stock_ticker:
        df = yf.Ticker(tic).history(period='max')
        df['date'] = df.index
        df = df.reset_index(drop=True)
        df = df[(df['date'] >= start) & (df['date'] <= end)]

        traces.append({'x':df.date, 'y': df.Close, 'name':tic})

    # Change the output data
    fig = {
        'data': traces,
        'layout': {'title':stock_ticker}
    }
    return fig

if __name__ == '__main__':
    app.run_server()
