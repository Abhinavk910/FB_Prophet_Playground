# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 18:59:28 2023

@author: abhinav.kumar
"""

from dash import html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
import pandas as pd
# from prophet import Prophet
import plotly.express as px
from datetime import date, timedelta, datetime
from helping_files.adding_holiday_layout import holiday_layout
from dash.exceptions import PreventUpdate
from helping_files.funtions import get_holi

dash.register_page(__name__)


layout = html.Div(children=[
    html.Div([
        dbc.Tabs([
            dbc.Tab(label="Adding Holiday", tab_id="tab-1"),
            # dbc.Tab(label="New Features(WIP)", tab_id="tab-2"),
            ],
            id="tabs", active_tab="tab-1",
        ),
        html.Div(id="content"),
        html.Hr(style={'margin':'0 2 2 2'}),
        html.Div([
                html.A(dbc.Button('<--- Stock Data', id='get_feature', style={'width':'200px', 'margin':'10px'}), href='/upload'),
                html.A(dbc.Button('Forecasting --->', id='get_forcast', style={'width':'200px', 'margin':'10px'}), href='/predict'),
            ], className='d-flex flex-wrap justify-content-center'),
    ], className='div-container p-sm-1 p-md-3', style={'min-width':'80%', 'max-width':'95%','min-height':'90%'})
], className='min-vh-100 d-flex flex-column justify-content-center align-items-center', 
             style={"background-color": "#ECF9FF"})





@dash.callback(Output("content", "children"), [Input("tabs", "active_tab")])
def switch_tab(at):
    if at == "tab-1":
        return holiday_layout
    elif at == "tab-2":
        return html.H1('WIP')
    return html.P("This shouldn't ever be displayed...")


@dash.callback(
    [Output('store-data4', 'data'),
     Output('alert-auto2', 'is_open'), Output('alert-auto2', 'children')
     # ,Output('for-refresh2', 'children')
     ],
    Input('save-button', 'n_clicks'),
    State('editable-table', 'data'),
    State('country_code', 'value'),
    State('store-data4', 'data'),
    prevent_initial_callback=True
)
def update_table_data(n_clicks, data, value, meta_data):
    
    if n_clicks:
        meta_data={}
        meta_data['holiday_data'] = data
        meta_data['country_selected'] = value
        return [meta_data, True, 'Saved'
                # , str(data)
                ]
    else:
        raise PreventUpdate


@dash.callback(
    [Output('editable-table', 'data'),Output('country_code', 'value')
     # ,Output('for-refresh', 'children')
     ],
    Input('add-row-button', 'n_clicks'),
    Input('get_holiday', 'n_clicks'),
    State('editable-table', 'data'),
    State('editable-table', 'columns'),
    State('store-data4', 'data'),
    State('country_code', 'value'),
    State('store-data1', 'data'),
    State('store-data2', 'data'),
    State('store-data5', 'data'),
)
def load_table_data(n_clicks, n_clicks2, rows, columns, table_data, country_code, tab, stock, upload):
    triggered_by = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if n_clicks2 == 0 and n_clicks==0:
        return [table_data['holiday_data'], table_data['country_selected']
                # , str(table_data['holiday_data'])
                ]
    else:
        if triggered_by == 'add-row-button':
            # Create a new row with empty values for each column
            new_row = {col['id']: '' for col in columns}
            # Add the new row to the existing data
            rows.append(new_row)
            return [rows, country_code
                    # , str(rows)
                    ]
        else:
            if tab == 'tab-10':
                data = get_holi(country_code, int(upload['start_from'].split('-')[0]))
            else:
                data = get_holi(country_code, int(stock['start_from'].split('-')[0]))
            return [data,country_code
                    # , str(data)
                    ]


@dash.callback(
        Output('div-save', 'hidden'),
        Output('div-add-row', 'hidden'),
        Input('get_holiday', 'n_clicks'),
        State('store-data4', 'data'),
        prevent_initial_callback=True
    )
def div_hidden(nclick, data):
    if nclick:
        return [False, False]
    elif data:
        return [False, False]
    else:
        raise PreventUpdate
    