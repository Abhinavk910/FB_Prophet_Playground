# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 16:10:26 2023

@author: abhinav.kumar
"""

from dash import html, dcc, Input, Output, State, dash_table
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from prophet import Prophet
import plotly.express as px
from datetime import date, timedelta, datetime
import plotly.graph_objects as go

from sklearn.metrics import mean_absolute_error, mean_squared_error
from math import sqrt


def get_mae(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    return round(mae, 2)

def get_mse(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    return round(mse, 2)

def get_rmse(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    rmse = sqrt(mse)
    return round(rmse, 2)
    
def get_mape(y_true, y_pred):
    mape = 100*((y_true - y_pred)/y_true).abs().mean()
    return round(mape, 2)

def get_mase(y_true, y_pred, y_train):
    mae_test = (y_true - y_pred).abs().mean()
    y_t = y_train
    y_t_1 = y_train.shift(-1)
    mae_train = (y_t - y_t_1).abs().mean()
    return round(mae_test/mae_train, 2)

dash.register_page(__name__)

colors = """#FCA311
#14213D
#000000
#66CCCC
#99CCFF"""
colors = colors.split("\n")

predict = html.Div([
    html.Div([
        html.H4('PlayGround!!', className='mx-3'),
    html.Hr(style={'margin':'0 2 2 2'}),
    html.Div([
        html.Div([
            html.Div([
            html.Span('Select Training Period'),
            dcc.DatePickerRange(
                id='date-range2',
                start_date_placeholder_text="Start Period",
                end_date_placeholder_text="End Period",
                # min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date.today(),
                style={'width':'100%', 'font-size':'12px'}
                # calendar_orientation='vertical',
            )
                ], className='div-container') 
        ], className='col-sm-12 col-md-4'),
        html.Div([
            html.Div([
            html.Span('Select Testing Period', id='select-span'),
            dcc.DatePickerSingle(
                id='date-range3',
                placeholder="Testing upto..",
                # min_date_allowed=date(1995, 8, 5),
                max_date_allowed=date.today(),
                style={'width':'100%'}
                # calendar_orientation='vertical',
            )
                ], className='div-container') 
        ], className='col-sm-12 col-md-4'),
        html.Div([
            html.Div([
            html.Span('Metrics'),
            dcc.Dropdown(
                id='mes-para',
                options=[
                    {'label': str(i), 'value': j} for (i, j) in {'Mean Absolute Error':'MAE',
                                                               'Mean Squared Error': 'MSE',
                                                               'Root Mean Squared Error':'RMSE',
                                                               'Mean Absolute Percentage Error':'MAPE',
                                                               'mean absolute scaled error':'MASE'
                                                               # 'Symmetric Mean Absolute Percentage Error':'SMAPE',
                                                               # 'Mean Directional Accuracy':'MDA'
                                                               }.items()
                ],
                value=['MAPE'],
                multi=True,
                clearable=False,
            )
            ], className='div-container')
        ], className='col-sm-12 col-md-4'),
        
    ], className='row', style={'margin':'auto'}),
    html.Hr(style={'margin':'0 2 2 2'}),
    html.Div([
        html.Div([
            html.Div([
            html.Span('n_changepoints'),
            dcc.Dropdown(
                id='id10',
                options=[
                    {'label': str(i), 'value': i} for i in [10,15, 20, 25,30, 35, 40, 45, 50]
                ],
                value=[25],
                multi=True,
                clearable=False,
            )
            ], className='div-container')
        ], className='col-sm-12 col-md-4'),
        html.Div([
            html.Div([
            html.Span('changepoint_prior_scale'),
            dcc.Dropdown(
                id='id1',
                options=[
                    {'label': str(i), 'value': i} for i in [0.01,0.03,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45, 0.5]
                ],
                value=[0.05],
                multi=True,
                clearable=False,
                
            )
                ], className='div-container') 
        ], className='col-sm-12 col-md-4'),
        html.Div([
            html.Div([
            html.Span('changepoint_range'),
            dcc.Dropdown(
                id='id5',
                options=[
                    {'label': str(i), 'value': i} for i in [0,0.1, 0.2, 0.3, 0.4,0.5, 0.6, 0.7, 0.8,0.9, 1]
                ],
                value=[0.8],
                multi=True,
                clearable=False,
            )
            ], className='div-container')
        ], className='col-sm-12 col-md-4'),
        html.Div([
            html.Div([
            html.Span('seasonality_prior_scale'),
            dcc.Dropdown(
                id='id2',
                options=[
                    {'label': str(i), 'value': i} for i in [0.01,1,5, 10]
                ],
                value=[10],
                multi=True,
                clearable=False,
            )
                ], className='div-container') 
        ], className='col-sm-12 col-md-4'),
        html.Div([
            html.Div([
            html.Span('holidays_prior_scale'),
            dcc.Dropdown(
                id='id3',
                options=[
                    {'label': str(i), 'value': i} for i in [0.01,1,5, 10]
                ],
                value=[10],
                multi=True,
                clearable=False,
            )
                ], className='div-container') 
        ], className='col-sm-12 col-md-4'),
        html.Div([
            html.Div([
            html.Span('seasonality_mode'),
            dcc.Dropdown(
                id='id4',
                options=[
                    {'label': str(i), 'value': i} for i in ['additive', 'multiplicative']
                ],
                value=['additive'],
                multi=True,
                clearable=False,
            )
            ], className='div-container')  
        ], className='col-sm-12 col-md-4'),
        # html.Div([
        #     html.Div([
        #     html.Span('growth'),
        #     dcc.Dropdown(
        #         id='id6',
        #         options=[
        #             {'label': str(i), 'value': i} for i in ['linear', 'logistic']
        #         ],
        #         value='linear'
        #     )
        #       ], className='div-container')  
        # ], className='col-sm-12 col-md-4'),
        
        html.Div([
            html.Div([
                html.Span('yearly_seasonality'),
                dcc.Dropdown(
                    id='id7',
                    options=[
                        {'label': str(i), 'value': i} for i in ['auto', True, False, 10, 20, 30, 40, 50]
                    ],
                    value=['auto'],
                    multi=True,
                    clearable=False,
                )
            ], className='div-container')
        ], className='col-sm-12 col-md-4  '),
        html.Div([
            html.Div([
            html.Span('weekly_seasonality'),
            dcc.Dropdown(
                id='id8',
                options=[
                    {'label': str(i), 'value': i} for i in ['auto', True, False, 10, 20, 30, 40, 50]
                ],
                value=['auto'],
                multi=True,
                clearable=False,
            )
            ], className='div-container')
        ], className='col-sm-12 col-md-4 '),
        html.Div([
            html.Div([
            html.Span('daily_seasonality'),
            dcc.Dropdown(
                id='id9',
                options=[
                    {'label': str(i), 'value': i} for i in ['auto', True, False, 10, 20, 30, 40, 50]
                ],
                value=['auto'],
                multi=True,
                clearable=False,
            )
            ], className='div-container')
        ], className='col-sm-12 col-md-4'),
        
    ], className='row', style={'margin':'auto'}),#this has also some padding 
    html.Hr(style={'margin':'0 2 2 2'}),
    html.Div([
        html.Div([
            html.Div([
                html.H2(id='value'),
                dcc.Loading(dcc.Graph(id='fig3')),
                html.Hr(style={'margin':'0 2 2 2'}),
                html.Div(id='result', className='p-sm-1 p-my-5')
            ], className='div-container')
        ], className='col-sm-12')
    ], className='row', style={'margin':'auto'}),
    html.Hr(style={'margin':'0 2 2 2'}),
    html.Div([
            html.A(dbc.Button('<--- Stock Data', id='get_feature', style={'width':'200px', 'margin':'10px'}), href='/upload'),
            html.A(dbc.Button('<--- Adding Features', id='get_forcast', style={'width':'200px', 'margin':'10px'}), href='/addholiday'),
            dbc.Button("Download xlsx", id="btn_xslx", style={'width':'200px', 'margin':'10px'}), dcc.Download(id="download_xslx")
        ], className='d-flex flex-wrap justify-content-center'),
    html.Hr(style={'margin':'0 2 2 2'}),
    html.Div([
        html.Div([
            html.P('Developed By')
            ]),
        html.Div([
            html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
            href = 'http://www.linkedin.com/in/abhinavk910', target="_blank", style={'color':'#FCA311'})
            ])
        ], className='div-container d-flex justify-content-around')
    
    ], style={ 'max-width':'1200px'} )
],className='min-vh-100 d-flex flex-column justify-content-center align-items-center mx-sm-0 mx-md-auto', style={ 'background-color':"#ECF9FF"})


# Define a layout for your page
layout = html.Div([
    predict,
], style={'background-color':"#ECF9FF",}, className='pt-sm-2 pt-md-3')



@dash.callback(
    [Output('date-range2', 'min_date_allowed'),
      Output('date-range2', 'start_date'),
      Output('date-range2', 'end_date'),
     Output('date-range3', 'date'),
     Output('id1', 'value'),
     Output('id2', 'value'),
     Output('id3', 'value'),
     Output('id4', 'value'),
     Output('id5', 'value'),
     # Input('id6', 'value'),
     Output('id7', 'value'),
     Output('id8', 'value'),
     Output('id9', 'value'),
     Output('id10', 'value')
     ],
    [
     Input('select-span', 'children')
     ],
    [
     State('store-data1', 'data'),
     State('store-data2', 'data'),
     State('store-data5', 'data'),
     State('store-data3', 'data')]
    )
def update_daterage(ninter, tab, stock, upload, data2):
    if tab == 'tab-10':
        start_date = upload['start_from']
    else:
        start_date = stock['start_from']
    try:
        return [start_date, data2['start_date'], data2['end_date'], data2['dt_t'],
                data2['id1'], data2['id2'], data2['id3'], data2['id4'], data2['id5'], data2['id7'],
                data2['id8'], data2['id9'], data2['id10']
                ]
    except:
        return [start_date,
                    start_date,
                    date.today() - timedelta(days=30),
                    date.today(),
                    0.05, 10, 10, 'additive', 0.8, 'auto', 'auto', 'auto', 25
                    ]

@dash.callback(
    Output('store-data3', 'data'),
    [Input('date-range2', 'start_date'),
    Input('date-range2', 'end_date'),
    Input('date-range3', 'date'),
    Input('id1', 'value'),
    Input('id2', 'value'),
    Input('id3', 'value'),
    Input('id4', 'value'),
    Input('id5', 'value'),
    # Input('id6', 'value'),
    Input('id7', 'value'),
    Input('id8', 'value'),
    Input('id9', 'value'),
    Input('id10', 'value')
    ]
    )
def update_store3(dt_s, dt_e, dt_t, id1, id2, id3, id4, id5, id7, id8, id9, id10):
    return {'start_date':dt_s, 'end_date':dt_e, 'dt_t':dt_t, 'id1':id1,'id2':id2, 
            'id3':id3,'id4':id4, 'id5':id5,'id7':id7, 'id8':id8,'id9':id9,'id10':id10 
            }

@dash.callback(
        [
            Output('id1', 'multi'),
            Output('id2', 'multi'),
            Output('id3', 'multi'),
            Output('id4', 'multi'),
            Output('id5', 'multi'),
            Output('id7', 'multi'),
            Output('id8', 'multi'),
            Output('id9', 'multi'),
            Output('id10', 'multi')
            ],
        Input('id1', 'value'),
        Input('id2', 'value'),
        Input('id3', 'value'),
        Input('id4', 'value'),
        Input('id5', 'value'),
        Input('id7', 'value'),
        Input('id8', 'value'),
        Input('id9', 'value'),
        Input('id10', 'value')
    )
def prevent_multi(id1, id2, id3, id4, id5, id7, id8, id9, id10):
    if not isinstance(id1, list):
        id1 = [id1]
    if not isinstance(id2, list):
        id2 = [id2]
    if not isinstance(id3, list):
        id3 = [id3]
    if not isinstance(id4, list):
        id4 = [id4]
    if not isinstance(id5, list):
        id5 = [id5]
    if not isinstance(id7, list):
        id7 = [id7]
    if not isinstance(id8, list):
        id8 = [id8]
    if not isinstance(id9, list):
        id9 = [id9]
    if not isinstance(id10, list):
        id10 = [id10]
        
    id_list = [len(id1), len(id2), len(id3), len(id4), len(id5), len(id7), len(id8), len(id9), len(id10)]
    result = [i>1 for i in  id_list]
    try:
        ind = result.index(True)
        return result
    except:
        return [True]*len(id_list)


@dash.callback(
    [Output('date-range3', 'min_date_allowed'),
     ],
     Input('date-range2', 'end_date'),
    )
def update_daterage2(data):
    return [
        datetime.strptime(data, "%Y-%m-%d") + timedelta(days=10)
            ]


@dash.callback(
    [
        Output('value', 'children'),
        Output('fig3', 'figure'),
        Output('store-data-final', 'data'),
        Output('result', 'children')
    ],
    [
        Input('id1', 'value'),
        Input('id2', 'value'),
        Input('id3', 'value'),
        Input('id4', 'value'),
        Input('id5', 'value'),
        # Input('id6', 'value'),
        Input('id7', 'value'),
        Input('id8', 'value'),
        Input('id9', 'value'),
        Input('id10', 'value'),
        Input('date-range2', 'start_date'),
        Input('date-range2', 'end_date'),
        Input('date-range3', 'date'),
        Input('mes-para', 'value')
    ],
    [
        State('store-data1', 'data'),
        State('store-data2', 'data'),
        State('store-data5', 'data'),
        State('store-data4', 'data'),
        
    ]
)
def get_update(id1, id2, id3, id4, id5, id7, id8, id9, id10, dr_s, dr_e, dr_t,mes_para,
               tab, stock, upload, holiday_meta_data):
    try:
        
        testing_interval = (datetime.strptime(dr_t, "%Y-%m-%d") - datetime.strptime(dr_e, "%Y-%m-%d")).days
        
        if not isinstance(id1, list):
            id1 = [id1]
        if not isinstance(id2, list):
            id2 = [id2]
        if not isinstance(id3, list):
            id3 = [id3]
        if not isinstance(id4, list):
            id4 = [id4]
        if not isinstance(id5, list):
            id5 = [id5]
        if not isinstance(id7, list):
            id7 = [id7]
        if not isinstance(id8, list):
            id8 = [id8]
        if not isinstance(id9, list):
            id9 = [id9]
        if not isinstance(id10, list):
            id10 = [id10]
            
        param_dic = {
                'changepoint_prior_scale': id1,
                'seasonality_prior_scale': id2,
                'holidays_prior_scale': id3,
                'seasonality_mode': id4,
                'changepoint_range': id5,
                # 'growth':growth,
                'yearly_seasonality': id7,
                'weekly_seasonality': id8,
                'daily_seasonality': id9,
                'n_changepoints': id10
            }
        
        index, name, times_it = 1,'dummy', 1
        for i, (j, k) in enumerate(param_dic.items()):
            if len(k)>1:
                index, name, times_it = i, j, len(k)
        
        
        total_params = []
        
        if times_it > 1:
            for time in range(times_it):
                param = {}
                for i, (j, k)in enumerate(param_dic.items()):
                    if i != index:
                        param[j] = k[0]
                    else:
                        param[j] = k[time]
                total_params.append(param)
        else:
            param = {}
            for j, k in param_dic.items():
                param[j] = k[0]
            
            total_params.append(param)
            
            
        if tab == 'tab-10':
            tdata = pd.read_json(upload['data'], orient='records')
            stock_name = upload['stock_name']
        else:
            tdata = pd.read_json(stock['data'], orient='records')
            stock_name = stock['stock_name']
        
        tdata = tdata.dropna()
        
        tdata.columns = ['ds', 'y']
        tdata['ds'] = pd.to_datetime(tdata.ds).dt.strftime('%Y-%m-%d')
        
        
        try:
            holiday_df = pd.DataFrame(holiday_meta_data['holiday_data'])
            holiday_df['date'] = pd.to_datetime(holiday_df.date)
            holiday_df.columns = ['ds', 'holiday', 'lower_window', 'upper_window']
            holiday_df.set_index('ds', drop=True, inplace=True)
            holiday_df = holiday_df.loc[dr_s:]
            holiday_df.reset_index(inplace=True)
            holiday_df['ds'] = holiday_df.ds.astype('string')
            holiday_df = holiday_df[['holiday', 'ds', 'lower_window', 'upper_window']]
            d = pd.merge(left=holiday_df, right=tdata, how='inner', left_on='ds', 
                        right_on='ds')[['ds', 'y', 'holiday']]
            d.dropna(inplace=True)
            holiday=True
        except:
            holiday=False
        
        
        data = tdata.set_index('ds', drop=True)
        # tdata.set_index('ds', inplace=True,drop=True)
        data = data.loc[dr_s:dr_e]
        data.reset_index(inplace=True)
        
        # test = tdata.set_index('ds', drop=True)
        # test = tdata.loc[dr_e:dr_t]
        # test.reset_index(inplace=True)
        y_train_final = pd.DataFrame([])
        if times_it>1:
            
            for i, params in enumerate(total_params):
                if holiday:
                    m = Prophet(**params, holidays=holiday_df).fit(data)
                else:
                    m = Prophet(**params).fit(data)
                future = m.make_future_dataframe(periods=testing_interval+30)
                y_train = m.predict(future)
                y_train = y_train.loc[:, ['ds', 'yhat']]    
                y_train['Type'] = str(param_dic[name][i])
                y_train.columns = ['ds', 'yhat', 'Type']
                y_train['ds'] = pd.to_datetime(y_train.ds).dt.strftime('%Y-%m-%d')
                y_train_final = pd.concat([y_train_final, y_train])
            
        else:
            params = total_params[0]
            if holiday:
                m = Prophet(**params, holidays=holiday_df).fit(data)
            else:
                m = Prophet(**params).fit(data)
            future = m.make_future_dataframe(periods=testing_interval+30)
            y_train_final = m.predict(future)
            y_train_upper_lower = y_train_final.loc[:, ['ds', 'yhat_lower', 'yhat_upper']]
            y_train_final = y_train_final.loc[:, ['ds', 'yhat']]
            y_train_final['Type'] = 'Prediction'
            y_train_final.columns = ['ds', 'yhat', 'Type']
            y_train_final['ds'] = pd.to_datetime(y_train_final.ds).dt.strftime('%Y-%m-%d')
        
        data2 = tdata.set_index('ds', drop=True)
        data2 = data2.loc[dr_s:dr_t]
        data2.reset_index(inplace=True)
        data2['Type'] = 'Actual'
        data2.columns = ['ds', 'yhat', 'Type']
        
        
        df = pd.concat([y_train_final, data2])
            
        colors = """#FCA311
        #14213D
        #000000
        #66CCCC
        #99CCFF"""
        colors = colors.split("\n")
        df['yhat'] = df.yhat.astype(int)
        if times_it>1:
            fig = px.line(df, x='ds', y='yhat', color='Type', line_shape='linear',
                          color_discrete_map={'Actual':colors[0]})
        else:
            fig = px.line(df, x='ds', y='yhat', color='Type', line_shape='linear',
                      color_discrete_map={'Prediction':colors[1], 'Actual':colors[0]})
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
        fig.update_layout(hovermode="x")
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=0.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(0,0,0,0)',
            title_text=''
        ))
        fig.add_vline(x=dr_e,
                  fillcolor="black", opacity=0.3,
                  layer="above", line_width=1,
                  line_color='rgba(0, 0, 0, 0.4)',
                  line_dash="dash")
        fig.add_vrect(x1=dr_e, x0=dr_t, line_width=0, fillcolor=colors[4], opacity=0.2)
        fig.update_layout(
            margin=dict(t=0, l=0, r=0, b=0, pad = 0),
            plot_bgcolor = '#FFFFFF',
            paper_bgcolor = '#FFFFFF'
        )
        if holiday:
            scatter_trace = go.Scatter(x=d.ds, y=d.y, mode="markers", text=d.holiday,
                                       marker=dict(color="red"),  showlegend=False,
                                       hovertemplate='<b>%{text}</b><br><extra></extra>'
                                      )
            fig.add_trace(scatter_trace)
            
        
        if times_it == 1:
           scatter_trace_upper =  go.Scatter(
                name='Upper Bound',
                x=y_train_upper_lower['ds'],
                y=y_train_upper_lower['yhat_upper'],
                mode='lines',
                marker=dict(color="#444"),
                line=dict(width=0),
                showlegend=False
                )
           fig.add_trace(scatter_trace_upper)
           scatter_trace_lower = go.Scatter(
                name='Lower Bound',
                x=y_train_upper_lower['ds'],
                y=y_train_upper_lower['yhat_lower'],
                marker=dict(color="#444"),
                line=dict(width=0),
                mode='lines',
                fillcolor='rgba(68, 68, 68, 0.3)',
                fill='tonexty',
                showlegend=False
                )
           fig.add_trace(scatter_trace_lower)
        
        
        df = pd.pivot_table(data=df, index='ds', values='yhat', columns='Type')
        df = df.loc[dr_e:dr_t]      
        df = df.dropna()
        
        test = 'Actual'
        y_true = df[test]
        list_of_col = list(df.columns)
        list_of_col.remove(test)
        preds = list_of_col
        
        result_data = {}
        
        if 'MAE' in mes_para:
            res = []
            for pred in preds:
                y_pred = df[pred]
                res.append(get_mae(y_true, y_pred))
            result_data['MAE'] = res
        if 'MSE' in mes_para:
            res = []
            for pred in preds:
                y_pred = df[pred]
                res.append(get_mse(y_true, y_pred))
            result_data['MSE'] = res
        if 'RMSE' in mes_para:
            res = []
            for pred in preds:
                y_pred = df[pred]
                res.append(get_rmse(y_true, y_pred))
            result_data['RMSE'] = res
        if 'MAPE' in mes_para:
            res = []
            for pred in preds:
                y_pred = df[pred]
                res.append(get_mape(y_true, y_pred))
            result_data['MAPE'] = res
        if 'MASE' in mes_para:
            res = []
            for pred in preds:
                y_pred = df[pred]
                res.append(get_mae(y_true, y_pred))
            result_data['MASE'] = res
            
        result = pd.DataFrame(result_data).T
        result.columns = preds
        result.reset_index(inplace=True)
        result = result.rename(columns={'index':'Metrics'})
        val = list(result.columns)
        tabled = html.Div([
            html.H4('Metrics'),
            dash_table.DataTable(
                data=result.to_dict('records'),
                columns=[{'name':i, 'id':i} for i in val],
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
                
            ),
        ], className='d-flex flex-column', style={'text-align':'center'})
        
        return [
            f'{stock_name}',
               fig, df.to_json(orient='records', date_format='iso'), tabled]
    
    except Exception as e:
        fig = go.Figure()
        fig.add_layout_image(dict(
        source="assets/image.jpg",
        x=0.2,
        y=0.1,
        )
        )
        fig.update_layout_images(dict(
                xref="paper",
                yref="paper",
                sizex=1,
                sizey=1,
                xanchor="left",
                yanchor="bottom"
        ))
        fig.update_layout(
            margin=dict(t=0, l=0, r=0, b=0, pad = 0),
            plot_bgcolor = '#FFFFFF',
            paper_bgcolor = '#FFFFFF',
            )
        fig.update_yaxes(
                    title=None,
                    showline = False,
                    showgrid=False,
                    zeroline = False,
                    tickmode='array',
                    tickvals=[]
                    )
        fig.update_xaxes(
                    title=None,
                    showline = False,
                    showgrid=False,
                    zeroline = False,
                    tickmode='array',
                    tickvals=[]
                    )
        return ['Error', fig, None, str(e)]


@dash.callback(Output("download_xslx", "data"), 
               [Input("btn_xslx", "n_clicks")],
               [State('store-data-final', 'data')],
               prevent_initial_call=True)
def generate_xlsx(n_nlicks, data):
        
    
    df = pd.read_json(data, orient='records')
    # df['ds'] = pd.to_datetime(df.ds).dt.strftime('%Y-%m-%d')
    df = df.pivot(index='ds', columns='Type', values='yhat')
    

    def to_xlsx(bytes_io):
        xslx_writer = pd.ExcelWriter(bytes_io, engine="xlsxwriter")  # requires the xlsxwriter package
        df.to_excel(xslx_writer, sheet_name="sheet1")
        xslx_writer.save()

    return dcc.send_bytes(to_xlsx, "prediction.xlsx")

