# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 15:58:21 2023

@author: abhinav.kumar
"""

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash
from helping_files.funtions import get_stock_data


app = Dash(__name__, 
           use_pages=True,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[
               {"name": "viewport", "content": "width=device-width, initial-scale=1"}
             ],
            suppress_callback_exceptions=True
           )
server = app.server

# df = get_stock_data('tcs.ns', '2023-01-01')
# data = df.to_json(orient='records', date_format='iso')

extacted_data = dcc.Store(id='store-data1', data = None, storage_type='session')

meta_dic = {'start_from':None, 'extracted_stock':None, 'holiday_data':None, 'country_selected':None}

meta_data = dcc.Store(id='store-data2', data=meta_dic, storage_type='session')

data_holiday = dcc.Store(id='store-data4', data=None, storage_type='session')


date_filter_data = dcc.Store(id='store-data3', data=None, storage_type='session')

date_upload = dcc.Store(id='store-data5', data=None, storage_type='session')


data5 = {'upload_stock_data':None}
upload_data = dcc.Store(id='store-data-upload', data=None, storage_type='session')


data6 = {'upload_stock_data':None}
upload_data_2 = dcc.Store(id='store-data-upload2', data=None, storage_type='session')


final_data = dcc.Store(id='store-data-final', data=None, storage_type='session')

path = {'which_path':None}
path_save = dcc.Store(id='store-data-path', data=None, storage_type='session')
app.layout = html.Div([
	dash.page_container, 
    extacted_data,
    meta_data,
    date_filter_data,
    data_holiday,
    upload_data,
    upload_data_2,
    path_save,
    date_upload,
    final_data

])

if __name__ == '__main__':
	app.run_server(debug=True, port=8051)
