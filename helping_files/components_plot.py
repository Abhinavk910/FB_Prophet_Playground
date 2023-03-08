# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 14:59:12 2023

@author: abhinav.kumar
"""

import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go

def plot_yearly(m, yearly_start=0, name='yearly'):
    days = (pd.date_range(start='2017-01-01', periods=365) +
            pd.Timedelta(days=yearly_start))
    df_y = seasonality_plot_df(m, days)
    seas = m.predict_seasonal_components(df_y)
    return go.Scatter(x=df_y['ds'].dt.to_pydatetime(), y=seas['yearly'], hoverinfo='skip', showlegend=False)

def plot_trend(m, fcst, name='trend'):
    return go.Scatter(x=fcst['ds'].dt.to_pydatetime(), y=fcst['trend'], hoverinfo='skip', showlegend=False)

def plot_holidays(m, fcst, name='trend'):
    return go.Scatter(x=fcst['ds'].dt.to_pydatetime(), y=fcst['holidays'], hoverinfo='skip',  showlegend=False)

def plot_weekly(m, name='trend'):
    days = (pd.date_range(start='2017-01-01', periods=7) +
                        pd.Timedelta(days=0))
    sea = m.predict_seasonal_components(seasonality_plot_df(m, days))
    return go.Scatter(x=days.day_name(), y=sea['weekly'], mode='lines', hoverinfo='skip',  showlegend=False)


def seasonality_plot_df(m, ds):
    df_dict = {'ds': ds, 'cap': 1., 'floor': 0.}
    for name in m.extra_regressors:
        df_dict[name] = 0.
    # Activate all conditional seasonality columns
    for props in m.seasonalities.values():
        if props['condition_name'] is not None:
            df_dict[props['condition_name']] = True
    df = pd.DataFrame(df_dict)
    df = m.setup_dataframe(df)
    return df




def get_component_plot(m2, forecast2):
    components = ['trend']
    if m2.train_holiday_names is not None and 'holidays' in forecast2:
        components.append('holidays')
    # Plot weekly seasonality, if present
    if 'weekly' in m2.seasonalities and 'weekly' in forecast2:
        components.append('weekly')
    # Yearly if present
    if 'yearly' in m2.seasonalities and 'yearly' in forecast2:
        components.append('yearly')
    # Other seasonalities
    components.extend([
        name for name in sorted(m2.seasonalities)
        if name in forecast2 and name not in ['weekly', 'yearly']
    ])

    fig = make_subplots(rows=len(components), cols=1,subplot_titles=(components))
    
    for i, component in enumerate(components):
        if component == 'trend':
            #trend
            fig.add_trace(plot_trend(m2, forecast2), row=i+1, col=1)
            fig.update_yaxes(
                row=i+1, col=1,
                fixedrange=True, showgrid=False,
                zeroline=False
            )
            fig.update_xaxes(
                row=i+1, col=1,
                fixedrange=True, showgrid=False,
                zeroline=False
            )
        elif component == 'yearly':
            fig.add_trace(plot_yearly(m2), row=i+1, col=1)
            fig.update_xaxes(
                row=i+1, col=1,
                tickmode='array',
                ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                tickvals=['2017-01-01', '2017-02-01', '2017-03-01', '2017-04-01', '2017-05-01', '2017-06-01', '2017-07-01',
                         '2017-08-01', '2017-09-01', '2017-10-01', '2017-11-01', '2017-12-01'],
                fixedrange=True, showgrid=False,
                zeroline=False
            )
            fig.update_yaxes(
                row=i+1, col=1,
                fixedrange=True, showgrid=False,
                zeroline=False
            )
        elif component == 'weekly':
            fig.add_trace(plot_weekly(m2), row=i+1, col=1)
            fig.update_yaxes(
                row=i+1, col=1,
                fixedrange=True, showgrid=False,
                zeroline=False
            )
            fig.update_xaxes(
                row=i+1, col=1,
                fixedrange=True, showgrid=False,
                zeroline=False
            )
        elif component == 'holidays':
            fig.add_trace(plot_holidays(m2, forecast2), row=i+1, col=1)
            fig.update_yaxes(
                row=i+1, col=1,
                fixedrange=True, showgrid=False,
                zeroline=False
            )
            fig.update_xaxes(
                row=i+1, col=1,
                fixedrange=True, showgrid=False,
                zeroline=False
            )

    fig.update_layout(height=1000, plot_bgcolor='rgba(0,0,0,0.03)',
                      title_text="Component Plots")
    return fig
