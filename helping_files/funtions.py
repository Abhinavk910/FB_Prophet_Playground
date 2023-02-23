# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 19:23:30 2023

@author: abhinav.kumar
"""
import holidays
from datetime import date, timedelta
import plotly.express as px
import pandas as pd
import yfinance as yf
import base64
import io
from dash import html, dash_table, dcc

colors = """#FCA311
#14213D
#000000
#66CCCC
#99CCFF"""
colors = colors.split("\n")

def get_holi(country_code, start_from_year):
    
    end_year = date.today().year
    
    holidays_dic = holidays.CountryHoliday(country_code, years=start_from_year)
    for year in range(start_from_year, end_year):
        holidays_dic.update(holidays.CountryHoliday(country_code, years=year+1))
    
    data = pd.Series(holidays_dic).to_frame().reset_index()
    data.columns=['date', 'event']
    data.sort_values(['event', 'date'], inplace=True)
    data['lower_window'] = 0
    data['upper_window'] = 0
    
    return data.to_dict(orient='records')


def get_stock_data(stock, start_date):
    end_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    data = yf.download([stock], start=start_date, end=end_date)[['Close']]
    df = pd.date_range(start_date, end_date).to_frame()
    df=df.join(data)
    # df['Close'] = df.Close.interpolate(method='time')
    df['Close'] = df.Close.fillna(method = 'ffill')
    df['Close'] = df.Close.fillna(method = 'bfill')
    df.reset_index(drop=True, inplace=True)
    df.columns = ['ds', stock]
    return df



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    print(decoded)
    try:
        if 'csv' in filename:
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file2.'
        ])
    # return [df]
    return [df, [html.Div([
        html.Div([
            html.Div([
                html.H4('First 3 rows'),
                dash_table.DataTable(
                    data=df.iloc[:3].to_dict('records'),
                    columns=[{'name': i, 'id': i} for i in df.columns]
                ),
            ], className='div-container')
        ], className='col-sm-12 col-md-6'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Div([
                                html.P('Select Date Column'),
                            ], className='col-sm-12 col-md-4'),
                            html.Div([
                                dcc.Dropdown(id='date-col',
                                    options=[{'label': i, 'value': i} for i in df.columns],
                                )
                            ], className='col-sm-12 col-md-8')
                        ], className='row')
                    ], className='col-sm-12'),
                    html.Hr(),
                    html.Div([
                        html.Div([
                            html.Div([
                                html.P('Select Data Column'),
                            ], className='col-sm-12 col-md-4'),
                            html.Div([
                                dcc.Dropdown(id='data-col',
                                    options=[{'label': i, 'value': i} for i in df.columns],
                                )
                            ], className='col-sm-12 col-md-8')
                        ], className='row')
                    ], className='col-sm-12')
                ], className='row')
            ], className='div-container')
        ], className='col-sm-12 col-md-6')
    ], className='row g-0')]]



def plot_upload(df):
    try:
        fig = px.line(df, x='ds', y='y', line_shape='spline')
    except:
        fig = px.line(df, x='ds', y='y', line_shape='linear')
    fig.update_xaxes(rangeslider_visible=False,
                     showline=True,
                     title=None,
                     linecolor=colors[2],
                     linewidth=3,
                     showgrid=False,
                     layer='above traces',
                     showticklabels=True,
                     ticks="outside",
                    tickwidth=1.5,
                    tickcolor=colors[2],
                    ticklen=10,
                tickmode='auto',
                tickfont=dict(size=10),
                        rangeselector=dict(
                        buttons=list([
                            dict(count=1, label="1m", step="month", stepmode="backward"),
                            dict(count=6, label="6m", step="month", stepmode="backward"),
                            dict(count=1, label="1y", step="year", stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    )
    fig.update_yaxes(
                title=None,
                showline = False,
                showgrid=False,
                fixedrange=True,
                zeroline = False,
                nticks=5,
                ticks="inside",
                tickcolor='black',
                ticklen=5,
                tickwidth=1,
                tickmode='auto',
                tickfont=dict(size=10)
            )
    fig.update_traces(mode="lines", hovertemplate=None)
    fig.update_traces(line_color=colors[0], line_width=2)
    fig.update_layout(hovermode="x")
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=0.02,
        xanchor="right",
        x=1
    ))
    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0, pad = 0),
        plot_bgcolor = '#FFFFFF',
        paper_bgcolor = '#FFFFFF'
    )
    return fig