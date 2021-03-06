import ast
import pickle

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from datetime import datetime
import yfinance as yf

with open ('outfile', 'rb') as fp:
    list_of_tickers = pickle.load(fp)

tickerz = []
for i in list_of_tickers:
    new_dict = {}
    new_dict['label'] = i
    new_dict['value'] = i
    tickerz.append(new_dict)

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])
server = app.server
app.layout = html.Div([
    dcc.Markdown(''' --- '''),
    html.H1('Stock Analyzer Dashboard'),
    dcc.Markdown(''' --- '''),
    dcc.Tabs(id='tabs',
        value='tab_chart',
        children=[
        dcc.Tab(label='Chart',
            value='tab_chart',
            children=[
            html.Div(style={'border-left': '3px solid grey',
        					'marginTop': 25,
                            'height': '95%',
                            'position': 'absolute',
                            'left': '24.5%',
                            'top': '15%'}),
            html.Div([
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.H3('Enter a Stock Symbol:',
                                style={'paddingRight':'30px'}),
                            dcc.Dropdown(
                                id='my_ticker_symbol',
                                options=tickerz,
                                value='TSLA',
                            ),
                            html.Br(),
                            html.H3('Select Date Range:'),
                            dcc.DatePickerRange(
                                id='my_date_picker',
                                min_date_allowed = datetime(1950, 1, 1),
                                max_date_allowed = datetime.today(),
                                start_date = datetime(2018, 1, 1),
                                end_date = datetime.today()
                            ),
                            html.Br(),
                            html.Br(),
                            html.H3('Add Indicators'),
                            dcc.RadioItems(
                                id='ma_button',
                                options=[{'label': i, 'value': i} for i in ['None','SMA','EMA']],
                                value='None',
                                labelStyle={'display': 'inline-block'}
                                ),
                            dcc.Slider(
                                id='ma_slider',
                                min=1,
                                max=50,
                                value=10,
                                marks={**{str(1):str(1)},**{str(year): str(year) for year in range(5,51,5)}},
                                step=None
                                ),
                            html.Button(id='submit-button',
                                n_clicks=0,
                                children='Submit',
                                style={'fontSize':24,'marginLeft':'40%'}
                                )
                            ], style={'display':'inline-block', 'verticalAlign':'top','width':'3'}
                        )
                    ),
                    dbc.Col(
                        html.Div([
                            dcc.Loading(
                                id="loading-1",
                                type="default",
                                children=dcc.Graph(
                                    id='inter_chart',
                                    figure={
                                        'data': [
                                            {'x': [0], 'y': [0]}
                                        ]
                                    }
                                )
                            ),
                        dcc.Loading(
                            id="loading-2",
                            type="default",
                            children=html.Div(id='add_info')
                        ),
                        ]),width=9
                    )
                ])
            ])
            ]
        ),
        dcc.Tab(label='Comparison',
            value='tab_comp',
            children=[
            html.Div([html.H3('Enter Stock Symbols:', style={'paddingRight':'30px'}),
            dcc.Dropdown(
                id='comp_ticker_symbol',
                options=tickerz,
                value=['TSLA'],
                multi=True
            )], style={'display':'inline-block', 'verticalAlign':'top','width':'30%'}),
            html.Div([
                html.H3('Select start and end dates:'),
                dcc.DatePickerRange(
                    id='comp_date_picker',
                    min_date_allowed = datetime(1950, 1, 1),
                    max_date_allowed = datetime.today(),
                    start_date = datetime(2018, 1, 1),
                    end_date = datetime.today()
                )
            ], style={'display':'inline-block','paddingLeft':'30px'}),
            html.Div([
                html.Button(id='comp_submit-button',
                n_clicks=0,
                children='Submit',
                style={'fontSize':24,'marginLeft':'30px'}
                )
            ], style={'display':'inline-block'}
            ),
            dcc.Graph(
                id='comp_chart',
                figure={
                    'data': [
                        {'x': [1,2], 'y': [3,1]}
                    ]
                }
            )
            ]
        )
        ]
    )
    ],style={'marginLeft':'1%'}
)

@app.callback(
    Output('inter_chart', 'figure'),
    [Input('submit-button','n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date'),
    State('ma_button', 'value'),
    State('ma_slider', 'value')])
def update_graph(n_clicks,stock_ticker, start_date, end_date, but_value, sli_value):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    df = yf.Ticker(stock_ticker).history(period='max')
    df['date'] = df.index
    df = df.reset_index(drop=True)
    df = df[(df['date'] >= start) & (df['date'] <= end)]

    traces.append({'x':df['date'], 'y': df['Close'], 'name':stock_ticker})
    if but_value == 'SMA':
        df['sma'] = df['Close'].rolling(window=sli_value).mean()
        traces.append({'x':df['date'], 'y': df['sma'], 'name':f'{sli_value} Day SMA'})
    if but_value == 'EMA':
        df['ema'] = df['Close'].ewm(span=sli_value,adjust=False).mean()
        traces.append({'x':df['date'], 'y': df['ema'], 'name':f'{sli_value} Day EMA'})
    # Change the output data
    fig = {
        'data': traces,
        'layout': {'title':stock_ticker}
    }
    return fig

@app.callback(
    Output('add_info', 'children'),
    [Input('submit-button','n_clicks')],
    [State('my_ticker_symbol', 'value')])
def set_display_children(n_clicks, ticker_symbol):
    try:
        stock_info = yf.Ticker(str(ticker_symbol)).info
        corp_name = stock_info['shortName']
        summary = stock_info['longBusinessSummary']
        sector = stock_info['sector']
        industry = stock_info ['industry']
        pe_ratio = round(stock_info['trailingPE'],2)
        yearly_high = round(stock_info['fiftyTwoWeekHigh'],2)
        yearly_low = round(stock_info['fiftyTwoWeekLow'],2)
        return html.Div([
            html.H3(f'Company Name: {corp_name}'),
            html.H5(f'Industry: {industry}'),
            html.H5(f'PE Ratio: {pe_ratio}'),
            html.Br(),
            html.H5(f'52 Week High: {yearly_high}'),
            html.H5(f'52 Week Low: {yearly_low}'),
            html.Br(),
            html.P(f'Company Summary: {summary}'),
            ])
    except:
        return html.Div([
            html.H3(f'Company Name: {ticker_symbol}'),
            html.H5(f'No other information available')
            ])


@app.callback(
    Output('comp_chart', 'figure'),
    [Input('comp_submit-button','n_clicks')],
    [State('comp_ticker_symbol', 'value'),
    State('comp_date_picker', 'start_date'),
    State('comp_date_picker', 'end_date')])
def update_comp_graph(n_clicks,stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    for tic in stock_ticker:
        df = yf.Ticker(tic).history(period='max')
        df['date'] = df.index
        df = df.reset_index(drop=True)
        df = df[(df['date'] >= start) & (df['date'] <= end)]

        traces.append({'x':df['date'], 'y': (df['Close']/df['Close'].iloc[0])-1, 'name':tic})

    # Change the output data
    fig = {
        'data': traces,
        'layout': {'yaxis':{'title':'Percentage Change(%)','tickformat':".2%"}}
        }
    return fig

if __name__ == '__main__':
    app.run_server()
