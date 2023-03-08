# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 19:22:21 2023

@author: abhinav.kumar
"""
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from helping_files.country_code import country_data

dropdown = dcc.Dropdown(
                id='country_code',
                options=[
                    {'label': str(i), 'value': j} for i, j in zip(country_data['Country'], country_data['Code'])
                ],
                placeholder='Select Country',
                multi=False,
                clearable=False,
                value='IN',
                style={'text-align':'center', 'font-weight':'400', 'font-size':'1.2rem', }
            )

get_holi_button = dbc.Button('Get Holidays', id='get_holiday', n_clicks=0)

columns = [
    {'name': 'Date of Event', 'id': 'date', 'type': 'datetime', 'editable': True},
    {'name': 'Name', 'id': 'event', 'type':'text', 'editable':True},
    {'name':'Lower Window', 'id':'lower_window', 'type':'numeric', 'editable':True},
    {'name':'Upper Window', 'id':'upper_window', 'type':'numeric', 'editable':True}
    
]

table = dash_table.DataTable(
    id='editable-table',
    columns=columns,
    data=None,
    editable=True,
    row_deletable=True,
    style_cell={
        'textAlign': 'center',
        # 'overflowX': 'scroll',
        'whiteSpace': 'normal',
        'height': 'auto',
    },
    style_table={'overflowX': 'auto'},

    style_header={
        # 'backgroundColor': 'white',
        'fontWeight': 'bold'
    },

)

add_row = dbc.Button('Add Row', id='add-row-button',style={'width':'50px','font-size':'10px', 'margin':'1px', 'padding':'1px'}, n_clicks=0)

save_changes = dbc.Button('Save Changes', id='save-button', n_clicks=0)

alert = dbc.Alert(
    "This is a danger alert!",
    id="alert-auto2",
    is_open=False,
    duration=4000,
    color="info"
)

holiday_layout = html.Div([
    html.Div([
      html.Div([
          html.H4('Select Country')
      ], className='col-sm-12 col-md-4 text-center'),
      html.Div([
          dropdown
      ], className='col-sm-12 col-md-6')
    ], id='stock-dropdown', className='row mb-2', style={'min-width':'80%'}),
    html.Hr(style={'margin':'0 2 2 2'}),
    html.Div([
        html.Div([
            get_holi_button
        ], className='col-sm-12')
    ], className='row ', style={'text-align':'center'}),
    html.Hr(style={'margin':'0 2 2 2'}),
    html.Div([
        html.Div([
            table,
            html.Div([
                add_row
                ], id='div-add-row', hidden=False)

        ], className='col-md-12')
    ], className='row ', style={'text-align':'right'}),
    html.Hr(style={'margin':'0 2 2 2'}),
    html.Div([
            alert
        ]),
    html.Div([
        html.Div([
            save_changes,
        ], className='col-md-12', id='div-save', hidden=True)
    ], className='row ', style={'text-align':'center'}),


], className='my-3')



changepoin_layout = html.Div([
    dcc.Graph(id='graph-cp'),
    
    html.Div([
    # html.P('select changepoint from graph',id='check-cp'),
    dbc.Alert(
        "Saved",
        id="alert-auto-cp",
        is_open=False,
        duration=4000,
        color="info",
        className='mt-5'
    ),
    
    dash_table.DataTable(
                        data=None,
                        id='table-cp',
                        columns= [{'name': 'Changepoints', 'id': 'Changepoints', 'type': 'any', 'editable': True}],
                        editable=True,
                        row_deletable=True,
                        style_cell={
                            'textAlign': 'center',
                            'whiteSpace': 'normal',
                            'height': 'auto',
                        },
                        style_table={'overflowX': 'auto', 'min-width':'300px', 'margin-top':'30px'},
                        style_header={
                            'fontWeight': 'bold'
                        },
                        # style={}
                                 
                ),
    dbc.Button('Save', id='save_change-cp', className='m-3'),
    ], className='d-flex flex-column justify-content-center align-items-center'),
])
