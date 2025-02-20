#!/usr/bin/env python
# coding: utf-8

import dash
import more_itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')


# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center'}),
    
    # Dropdown for statistics selection
    html.Label("Select Statistics:"),
    dcc.Dropdown(
        id='dropdown-statistics',
        options=[
            {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'},
            {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'}
        ],
        value='Recession Period Statistics',
        clearable=False
    ),

    # Dropdown for selecting a year
    html.Label("Select Year:"),
    dcc.Dropdown(
        id='select-year',
        options=[{'label': str(year), 'value': year} for year in data['Year'].unique()],
        value=data['Year'].min(),
        clearable=False
    ),

    # Output container
    html.Div(id='output-container')
])

# Callback function to update the dashboard
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'), 
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, selected_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        R_chart1 = dcc.Graph(
            figure=px.line(recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index(),
                           x='Year', y='Automobile_Sales',
                           title="Average Automobile Sales During Recession")
        )

        R_chart2 = dcc.Graph(
            figure=px.bar(recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index(),
                          x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Vehicles Sold by Type During Recession")
        )

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics' and selected_year:
        yearly_data = data[data['Year'] == selected_year]

        Y_chart1 = dcc.Graph(
            figure=px.line(yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index(),
                           x='Month', y='Automobile_Sales',
                           title="Total Monthly Automobile Sales in {}".format(selected_year))
        )

        Y_chart2 = dcc.Graph(
            figure=px.bar(yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index(),
                          x='Vehicle_Type', y='Automobile_Sales',
                          title="Average Vehicles Sold by Type in {}".format(selected_year))
        )

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex'})
        ]

    return html.Div()  # Return an empty div if no valid selection

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
