import dash
import dash_core_components as dcc
import dash_html_components as html
# Add an import for Input/Output
from dash.dependencies import Input, Output

app = dash.Dash()

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.H3('Enter a stock symbol:'),
    dcc.Input(
# Add an ID to the input box
        id='my_ticker_symbol',
        value='TSLA'
    ),
    dcc.Graph(
# Add an ID to the graph
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ],
        }
    )
])
# Add a callback function
@app.callback(
    Output('my_graph', 'figure'),
    [Input('my_ticker_symbol', 'value')])
def update_graph(stock_ticker):
    fig = {
        'data': [
            {'x': [1,2], 'y': [3,1]}
        ],
        'layout': {'title':stock_ticker}
    }
    return fig

if __name__ == '__main__':
    app.run_server()
