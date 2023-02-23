# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 11:55:34 2023

@author: abhinav.kumar
"""

from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from datetime import datetime, timedelta, date


upload_layout = html.Div([
        html.Div([
        html.Div([
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select Files')
                    ]),
                    style={
                        'height': '30px','lineHeight': '30px','borderWidth': '1px','borderStyle': 'dashed',
                        'borderRadius': '5px','textAlign': 'center','margin': '5px'
                    },
                    multiple=False
                ),
            ], className='div-container')
        ], className='col-sm-12')
    ], className='row', style={'margin':'auto'}),
    html.Div([
                 html.Div([
                     html.Div([
                         html.Div([
                             html.H4('First 3 rows'),
                             dash_table.DataTable(
                                 data=None,
                                 id='upload-datatable'
                             ),
                         ], className='')
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
                                                 options=[{'label': i, 'value': i} for i in ['dd']],#df.columns],
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
                                                 options=[{'label': i, 'value': i} for i in ['dd']],#df.columns],
                                             )
                                         ], className='col-sm-12 col-md-8')
                                     ], className='row')
                                 ], className='col-sm-12')
                             ], className='row')
                         ], className='m-4 p-3')
                     ], className='col-sm-12 col-md-6')
                 ], className='row g-0')
                 ], id='output-data-upload',className='div-container3', hidden=True),
    
    # html.Hr(style={'margin':'0 2 2 2'}),
    # html.Div([
    #         html.A(dbc.Button('Adding Features --->', id='get_feature', style={'width':'200px', 'margin':'10px'}), href='/addholiday'),
    #         html.A(dbc.Button('Forecasting --->', id='get_forcast', style={'width':'200px', 'margin':'10px'}), href='/predict'),
    #     ] id='hidden-div2', hidden=True),
    html.Div([
        html.Div([
            dbc.Button('Extract Data',id='get-upload-data', style={'width':'200px', 'margin':'10px'}),
        ], className='col-sm-12 d-flex justify-content-center flex-wrap')
    ], className='row ', style={'text-align':'center'}),
    dbc.Alert(
        "This is a danger alert!",
        id="alert-auto3",
        is_open=False,
        duration=4000,
        color="danger"
    ),
    ])


stock_layout = html.Div([
        html.Div([
          html.Div([
              html.H4('Select Stock')
          ], className='col-sm-12 col-md-6 text-center'),
          html.Div([
              dcc.Dropdown(
                  id='select-stock',
                  options=[
                      {'label':i, 'value':i} for i in ['RELIANCE.NS', 'Other']
                  ],
                  placeholder='',
                  multi=False,
                  clearable=False,
                  style={'text-align':'center', 'font-weight':'400', 'font-size':'1.2rem', }
              )
          ], className='col-sm-12 col-md-6')
        ], id='stock-dropdown', className='row mb-2', style={'min-width':'80%'}),
        html.Div([
              html.Div([
                  html.H4(['Type Stock Symbol from ',html.A('"YFinance"', href='https://finance.yahoo.com/',
                                                            target="_blank", style={'color':'black'}
                                                           )])
              ], className='col-sm-12 col-md-6 text-center'),
              html.Div([
                 dbc.Input(id='stock-input', style={'text-align':'center', 'font-weight':'400',
                                                    'font-size':'1.2rem', 'height':'37px'})
              ], className='col-sm-12 col-md-6')
            ], className='row', id='input-stock-row',hidden=True, style={'min-width':'80%'}),
        html.Hr(style={'margin':'0 2 2 2'}),
        html.P(id='print-here'),
        html.Div([
              html.Div([
                  html.H4(['Stock Data From '])
              ], className='col-sm-12 col-md-6 text-center'),
              html.Div([
                 dcc.DatePickerSingle(
                    id='date-range1',
                    min_date_allowed=date(1995, 8, 5),
                    max_date_allowed=date.today()- timedelta(days=90),
                    initial_visible_month=date.today() - timedelta(days=365),
                    date=date.today() - timedelta(days=365),
                    style={'width':'100%'}
                ),
              ], className='col-sm-12 col-md-6')
            ], className='row', style={'min-width':'80%'}),
        html.Hr(style={'margin':'0 2 2 2'}),
        html.Div([
            html.Div([
                dbc.Button('Extract Data',id='get-data', style={'width':'200px', 'margin':'10px'}),
            ], className='col-sm-12 d-flex justify-content-center flex-wrap')
        ], className='row ', style={'text-align':'center'}),
        dbc.Alert(
            "This is a danger alert!",
            id="alert-auto1",
            is_open=False,
            duration=4000,
            color="danger"
        ),
    ])
