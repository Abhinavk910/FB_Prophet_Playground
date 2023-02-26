# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 16:06:07 2023

@author: abhinav.kumar
"""
import dash
from dash import html, dcc, Output, Input, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
        html.Div([

        html.Div([
                html.H3(children='Welcome to FB Prophet Playground!!'),
                html.A(dbc.Button('Upload Data'), href='/upload'),
                ], className='div-container text-center p-5'),
        html.Div([
            html.Div([
                html.P('Developed By')
                ]),
            html.Div([
                html.A(html.P([html.Span("A"), "bhinav ",html.Span('K'), "umar"]),
                href = 'http://www.linkedin.com/in/abhinavk910', target="_blank", style={'color':'#FCA311'})
                ])
            ], className='div-container d-flex justify-content-around')
    ], className='w-auto')
    

], className='min-vh-100 d-flex flex-column justify-content-center align-items-center', 
             style={"background-color": "#ECF9FF"})
