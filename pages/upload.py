# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 16:14:13 2023

@author: abhinav.kumar
"""

from dash import html, dcc, Input, Output, State, dash_table
from dash.exceptions import PreventUpdate
import dash
import plotly.express as px
import dash_bootstrap_components as dbc
from datetime import date, timedelta
import pandas as pd
from helping_files.funtions import get_stock_data, parse_contents, plot_upload
# from helping_files.upload_layout import upload_layout, stock_layout

dash.register_page(__name__)


# df = get_stock_data('tcs.ns', '2023-01-01')
# data = df.to_json(orient='records', date_format='iso')



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
    dbc.Alert(
        "You have to upload .csv or .xlsx file. Please do check!!",
        id="alert-auto5",
        is_open=False,
        duration=4000,
        color="danger"
    ),
    
    html.Div([
                 html.Div([
                     html.Div([
                         html.Div([
                             html.H4('First 3 rows'),
                             dash_table.DataTable(
                                 data=None,
                                 id='upload-datatable',
                                 style_table={'overflowX': 'scroll', 'width': '90%'}
                                 
                             ),
                         ], className='', style={"width":'90%'})
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
    
        html.Div([
            html.Div([
                dbc.Button('UPLOAD Extract Data',id='get-upload-data', style={'width':'200px', 'margin':'10px'}),
                html.Div([
                        html.A(dbc.Button('Adding Features --->', id='get_feature', style={'width':'200px', 'margin':'10px'}), href='/addholiday'),
                        html.A(dbc.Button('Forecasting --->', id='get_forcast', style={'width':'200px', 'margin':'10px'}), href='/predict')
                    ], id='hidden-div2', hidden=True)
            ], className='col-sm-12 d-flex justify-content-center flex-wrap')
        ], className='row ', style={'text-align':'center'}),
        dbc.Alert(
            "This is a danger alert!",
            id="alert-auto3",
            is_open=False,
            duration=4000,
            color="danger"
        ),
        html.Hr(style={'margin':'0 2 2 2'}, id='graph-hr', hidden=True),
        html.Div([
            html.Div([
                    dcc.Loading(html.H2(id='stock-name')),
                    dcc.Loading(dcc.Graph(id='fig1'))
            ], className='col-sm-12')
    ], className='row', style={'margin':'auto'}, id='graph-row', hidden=True)
    # ], className='div-container p-sm-1 p-md-5', style={'min-width':'80%'})
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
                html.Div([
                        html.A(dbc.Button('Adding Features --->', style={'width':'200px', 'margin':'10px'}), href='/addholiday'),
                        html.A(dbc.Button('Forecasting --->', style={'width':'200px', 'margin':'10px'}), href='/predict')
                    ], id='hidden-div1', hidden=True)
            ], className='col-sm-12 d-flex justify-content-center flex-wrap')
        ], className='row ', style={'text-align':'center'}),
        dbc.Alert(
            "This is a danger alert!",
            id="alert-auto1",
            is_open=False,
            duration=4000,
            color="danger"
        ),
        html.Hr(style={'margin':'0 2 2 2'}, id='graph-hr2', hidden=True),
        html.Div([
            html.Div([
                    dcc.Loading(html.H2(id='stock-name2')),
                    dcc.Loading(dcc.Graph(id='fig2'))
            ], className='col-sm-12')
    ], className='row', style={'margin':'auto'}, id='graph-row2', hidden=True)
    ])


colors = """#FCA311
#14213D
#000000
#66CCCC
#99CCFF"""
colors = colors.split("\n")



layout = html.Div(children=[
    html.Div([
        # html.P(['yo'], id='check'),
        html.Div([
            dbc.Tabs([
                dbc.Tab(label="Upload Data", tab_id="tab-10"),
                dbc.Tab(label="Stock Data", tab_id="tab-20"),
                ],
                id="data-tab", active_tab="tab-10",persistence=True, persistence_type='session'
            ),
            html.Div(id="data-content", className='mt-2')
        ], className='p-sm-1 p-md-3'),
        html.Hr(style={'margin':'0 2 2 2'}),
        html.Div([
            html.Div([
                html.Div([
                        html.A(dbc.Button('Adding Features --->', style={'width':'200px', 'margin':'10px'}), href='/addholiday'),
                        html.A(dbc.Button('Forecasting --->',  style={'width':'200px', 'margin':'10px'}), href='/predict')
                    ], id='hidden-div', hidden=True)
            ], className='col-sm-12 justify-content-center flex-wrap')
        ], className='row ', style={'text-align':'center'}),
    ], className='div-container p-sm-1 p-md-5', style={'min-width':'80%', 'max-width':'95%', 'text-align':'center'})
], className='min-vh-100 d-flex flex-column justify-content-center align-items-center mx-md-auto  mx-sm-0',style={"background-color": "#ECF9FF"})

@dash.callback([Output("data-content", "children"), Output('store-data1', 'data')],
               [Input("data-tab", "active_tab")])
def switch_tab(at):
    if at == "tab-10":
        return [upload_layout,at]
    elif at == "tab-20":
        return [stock_layout, at]



# upload data
@dash.callback([Output('store-data-upload', 'data'), Output('output-data-upload', 'hidden'), Output('alert-auto5', 'is_open')],
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
                State('upload-data', 'last_modified')],prevent_initial_call=True
              )
def upload_data(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        try:
            df, _ = parse_contents(list_of_contents, list_of_names, list_of_dates)
            return [df.to_json(orient='records', date_format='iso'), False, False]
        except:
            return [None, True, True]
            
    else:
        raise PreventUpdate



#populating table and dropdown
@dash.callback(
        [Output('upload-datatable', 'data'),
        Output('upload-datatable', 'columns'),
        Output('date-col', 'options'),
        Output('data-col', 'options')
        ],
        Input('output-data-upload', 'hidden'),
        State('store-data-upload', 'data'),prevent_initial_call=True
    )
def populate_uploaded_data(inputit, datait):
    if not inputit:
        df = pd.read_json(datait, orient='records')
        val = [{'name': i, 'id': i} for i in df.columns]
        val2 = [{'label': i, 'value': i} for i in df.columns]
        return [df.iloc[:3].to_dict('records'), val, val2, val2]
    else:
        PreventUpdate

@dash.callback(
    [Output('store-data5', 'data'),
    Output('alert-auto3', 'is_open'), Output('alert-auto3', 'children'),
    Output('alert-auto3', 'color'),
    Output('fig1', 'figure'),
    Output('graph-row', 'hidden'), Output('graph-hr', 'hidden'),
    Output('hidden-div2', 'hidden')
    ],
    Input('get-upload-data', 'n_clicks'),
    State('store-data5', 'data'),
    State('store-data-upload', 'data'),
    State('data-col', 'value'),
    State('date-col', 'value'),
    State('store-data1', 'data'),
    prevent_initial_call=True 
    )
def show_input1(nclick, data_upload_final, upload_data, data_col, date_col, tab):
    # if tab_active == 'tab-10':
    if nclick:
        if data_col is None or date_col is None:
            val = 'Select Date and Data Columns'
            return [None, True, val, 'danger', None, True, True, True]
        elif data_col == date_col:
            val = 'Please select date and data saperates column'
            return [None, True, val, 'danger', None, True, True, True]
        else:
            val = 'Done'
            meta_data = {}
            df = pd.read_json(upload_data, orient='records')
            df = df.loc[:,[date_col, data_col]]
            df.columns = ['ds', 'y']
            if df.ds.astype('string').str.match('[a-zA-Z]+')[0]:
                return [None, True, "Date should not start with string, isn't it?", 'danger', None, True, True, True]
            elif any(pd.to_datetime(df.ds, errors='coerce').isna().tolist()):
                return [None, True, "Date have string in between or some error in parsing date", 'danger', None, True, True, True]  
            elif df.y.dtype not in ('int64', 'float64'):
                return [None, True, 'Problem with Data column. Must be integer.', 'danger', None, True, True, True]
            else:
                df['ds'] = pd.to_datetime(df.ds).dt.strftime('%Y-%m-%d')
                fig = plot_upload(df)
                meta_data['data'] = df.to_json(orient='records', date_format='iso')
                meta_data['stock_name'] = 'Uploaded Data'
                df = df.sort_values('ds').reset_index(drop=True)
                meta_data['start_from'] = str(df.loc[0, 'ds'])
                return [meta_data, 
                        True, val, 'info', fig, False, False, False]
    elif tab == 'tab-10' and data_upload_final is not None:
        df = pd.read_json(data_upload_final['data'], orient='records')
        fig = plot_upload(df)
        return [data_upload_final,False, "val",'info',fig, False, False, False,
                # ,str(meta_data)
                ]
        
    else:
        raise PreventUpdate
    # else:
    #     return [data_upload_final, False, '','',True ]






@dash.callback(
    [Output('input-stock-row', 'hidden'), Output('stock-dropdown', 'hidden')],
    [Input('select-stock', 'value')], prevent_initial_call=True
)
def show_input(val):
    if val == 'Other':
        return [False, True]
    else:
        return [True, False]
  


@dash.callback(
    [
     
      Output('store-data2', 'data'),
      Output('alert-auto1', 'is_open'), Output('alert-auto1', 'children'),
      Output('alert-auto1', 'color'),
      Output('fig2', 'figure'),
      Output('graph-row2', 'hidden'), Output('graph-hr2', 'hidden'),
      Output('hidden-div1', 'hidden'),
      Output('stock-name2', 'children')
    ],
    [Input('get-data', 'n_clicks')],
    [
        State('select-stock', 'value'),
        State('stock-input', 'value'),
        State('date-range1', 'date'),
        State('store-data2', 'data'),
        State('store-data1', 'data'),
    ], prevent_initial_call=True
)
def show_input2(nclick, drop_input, text_input, date, meta_data, tab
                ):
    # if active_tab == 'tab-20':
            
    val = 'no val'
    if nclick:
        if drop_input is not None:
            if drop_input == 'Other':
                if text_input is not None:
                    df = get_stock_data(text_input, date)
                    if not df.isna().iloc[0,1]:
                        val='Done'
                        meta_data['start_from'] = date
                        meta_data['extracted_stock'] = text_input
                        stock_name = str.capitalize(meta_data['extracted_stock'].split('.')[0])
                        meta_data['stock_name'] = stock_name
                        df.columns = ['ds', 'y']
                        meta_data['data'] = df.to_json(orient='records', date_format='iso')
                        fig = plot_upload(df)
                        return [meta_data,True, val,'info',fig, False, False, False, stock_name]
                    else:
                        val = 'Stock written is not matching. Please Review!!'
                        return [meta_data, True, val, 'danger',None, True, True,True, ''
                                # ,f'{nclick}, {drop_input}, {date}, {len(df)}, {df.iloc[0]}'
                                ]
                else:
                    val = 'Please write stock name in above text box'
                    return [meta_data, True, val, 'danger',None, True, True, True, ''
                            # ,f'{nclick},{drop_input}, {date}, input stock it should not be none'
                            ]
            else:
                val='Done'
                df = get_stock_data(drop_input, date)
                meta_data['start_from'] = date
                meta_data['extracted_stock'] = drop_input
                stock_name = str.capitalize(meta_data['extracted_stock'].split('.')[0])
                meta_data['stock_name'] = stock_name
                df.columns = ['ds', 'y']
                meta_data['data'] = df.to_json(orient='records', date_format='iso')
                fig = plot_upload(df)
                return [meta_data,True, val,'info',fig, False, False, False, stock_name
                        # ,str(meta_data)
                        ]
        else:
            val = 'Please selected stock from dropdown, if not there select other and proceed.'
            return [meta_data,True, val,'danger',None, True, True, True, ''
                    # ,f'select from dropdown'
                    ]

    elif meta_data['start_from'] is not None and tab=='tab-20':
            df = pd.read_json(meta_data['data'], orient='records')
            fig = plot_upload(df)
            return [meta_data,False, val,'info',fig, False, False, False, meta_data['stock_name']
                    # ,str(meta_data)
                    ]
    else:
        raise PreventUpdate


        
    
