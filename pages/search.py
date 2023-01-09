# import neccessary libraries, modules and packages
from dash import html, dcc, callback, Input, Output
import pandas as pd
import requests


def merge_data(url1, url2):
    """ 
    This function merges data from two URLs into one dataframe.

    Parameters:
        url1 (str): The first URL to get data from.
        url2 (str): The second URL to get data from.

    Returns:
        pandas.DataFrame: A merged dataframe containing data from both URLs.

    """
    # Get data from the first URL
    df1_request = requests.get(url1)
    # Get data from the second URL
    df2_request = requests.get(url2)
    
    # Check if the request was successful
    if df1_request.status_code == requests.codes.ok:
        json_df1 = df1_request.json()
    else:
        print("Error getting data from {}".format(url1))
        return

    if df2_request.status_code == requests.codes.ok:
        json_df2 = df2_request.json()
    else:
        print("Error getting data from {}".format(url2))
        return

    # Normalize the json data
    df1 = pd.json_normalize(json_df1)
    df2 = pd.json_normalize(json_df2)

    # Add a new column to each dataframe
    df1["force_type"] = "Northumbria Police"
    df2["force_type"] = "Cleveland Police"

    # Concatenate the two dataframes and reset the index
    df3 = pd.concat([df1, df2], ignore_index=True)

    return df3


def clean_data(df):
    # Drop unnecessary columns
    df = df.drop(["operation", "operation_name", "location", "outcome_linked_to_object_of_search", 
                  "legislation", "removal_of_more_than_outer_clothing", "outcome_object.id", 
                  "location.latitude", "location.street.id", "location.longitude"], axis=1)
    
    # Drop rows with any NaN values
    df.dropna(inplace=True)
    
    return df

#url for the two dataframe
url1= 'https://data.police.uk/api/stops-force?force=northumbria&date=2021-08'
url2= 'https://data.police.uk/api/stops-force?force=cleveland&date=2021-08'

#calling the merged data
merged_df = merge_data(url1, url2)

#calling the cleaned dataframe
filterdf = clean_data(merged_df)

# Define the layout of the search page
search_layout = html.Div(className='container-fluid', children=[
    #top navigation
    html.Div(className='row', children=[
        
        # start of Nav bar column
        html.Div(className='col-md-12', children=[
            html.Nav(className='navbar navbar-expand-lg navbar-dark bg-dark', children=[
                html.Div(className='mr-5', children=[
                    html.A(className='navbar-brand', children='Stop & Search Dashboard'),
                ]),
                
                html.Button(className='navbar-toggler', children=[
                    html.Span(className='navbar-toggler-icon')
                ]),
                
                html.Div(className='collapse navbar-collapse mx-auto', children=[
                    html.Div(className='mx-auto', children=[
                        html.Ul(className='navbar-nav mr-auto justify-content-center', children=[
                            html.Li(className='nav-item', children=html.A(className='nav-link', 
                                                                          children='Covid-19 Dashboard', 
                                                                          href='/covid', style={'color': 'white'})),
                            html.Li(className='nav-item', children=html.A(className='nav-link bg-light', 
                                                                          children='Stop and Search Dashboard', 
                                                                          href='/search', style={'color': 'black'})),
                            html.Li(className='nav-item', children=html.A(className='nav-link', 
                                                                          children='About Project', 
                                                                          href='/about', style={'color': 'white'})),
                        ])
                    ]),
                    html.Div(children=[
                        html.Li(className='btn btn-secondary', id='logout', 
                                children=html.A(children='Log Out', href='/', style={'color': 'white'}))
                    ])
                ])
            ])
        ]) # End of Nav bar column
    ]),
    
    # Start of main body div
    html.Div(className='row', children=[
        # Start of side filter pane
        html.Div(className='col-md-3 mt-5', children=[
            html.Div(className='row', children=[        
                html.Div(className='col-md-12', children=[
                    html.Div(className='card', children=[
                        html.Div(className='card-body', children=[
                            html.Div(className='form-group', children=[
                                html.Label('Select an Area'),
                                dcc.Dropdown(
                                    id='force-select',
                                    options=[{'label': force_type, 'value': force_type} for force_type in filterdf['force_type'].unique()],
                                    value='Cleveland Police'
                                )
                            ])
                        ])
                    ])
                ])
            ])
        ]), # End of side filter pane
      
        
        html.Div(className='col-md-9', children=[
            # Start of top card display
            html.Div(className='row mt-5', children=[      
                # Total search card
                html.Div(className='col-md-4 center', children=[
                    html.Div(className='card text-center', children=[
                        html.Div(className='card-body', children=[
                            html.H5(className='card-title center', children='Total stop and search'),
                            html.Div(id='total-search'),
                            html.P(className='card-text', children='The Total stop and search conducted for the selected Police force in August, 2021')
                        ])
                    ])
                ]),
                # Total Arrest card
                html.Div(className='col-md-4 center', children=[
                    html.Div(className='card text-center', children=[
                        html.Div(className='card-body', children=[
                            html.H5(className='card-title', children='Total Arrest made'),
                            html.Div(id='total-arrest'),
                            html.P(className='card-text', children='The Total Arrest made for the selected Police force in August, 2021')
                        ])
                    ])
                ]),
                # Percentage of Arrest display card
                html.Div(className='col-md-4 center', children=[
                    html.Div(className='card text-center', children=[
                        html.Div(className='card-body', children=[
                            html.H5(className='card-title', children='% of Arrest'),
                            html.Div(id='percent-arrest'),
                            html.P(className='card-text', children='The % of arrest made by the selected Police force in August, 2021')
                        ])
                    ])
                ])
            ]), # End of top card display

            
            
            # Pie chart Displays
            html.Div(className='row mt-3', children=[
                # Pie chart showing the Total Search by gender
                html.Div(className='col-md-6', children=[
                    dcc.Graph(id='pie-chart-total', figure={
                        'data': [{
                            'labels': filterdf['gender'].value_counts().index.tolist(),                     
                            'values': filterdf['gender'].value_counts().tolist(),
                            'type': 'pie'
                        }],
                        'layout': {
                            'title': 'Total Stop and search case by gender'
                        }
                    })
                ]),
                # Pie chart showing the Total Arrest by gender
                html.Div(className='col-md-6', children=[
                    dcc.Graph(id='pie-chart-arrest', figure={
                        'data': [{
                            'labels': filterdf[filterdf['outcome'] == 'Arrest']['gender'].value_counts().index.tolist(),                     
                            'values': filterdf[filterdf['outcome'] == 'Arrest']['gender'].value_counts().tolist(),
                            'type': 'pie'
                        }],
                        'layout': {
                            'title': 'Total Arrest by gender'
                        }
                    })
                ])
            ]), #End of Pie chart Displays div

            
            # histogram showing the stop and search by age group distribution by selected force
            html.Div(className='row mt-2', children=[
                
                #total stop and search by age-group
                html.Div(className='col-md-6', children=[
                    dcc.Graph(id='search-histogram-plot', figure={
                        'data': [{
                            'x': filterdf['age_range'],
                            'type': 'histogram'
                        }],
                        'layout': {
                            'title': 'Stop and search case breakdown by Age group'
                        }
                    })
                ]),
                # Arrest by age group
                html.Div(className='col-md-6', children=[
                    dcc.Graph(id='arrest-histogram-plot', figure={
                        'data': [{
                            'x': filterdf[filterdf['outcome'] == 'Arrest']['age_range'],
                            'type': 'histogram'                        
                            }],
                        'layout': {
                            'title': 'Total Arrest case breakdown by Age group'
                        }
                    })
                ])
            ]),
            
            # histogram showing stop and search by ethinicity
            html.Div(className='row mb-3', children=[
                html.Div(className='col-md-12', children=[
                    dcc.Graph(id='ethinic-histogram-plot', figure={
                        'data': [{
                            'x': filterdf['officer_defined_ethnicity'],
                            'type': 'histogram'
                        }],
                        'layout': {
                            'title': 'Stop search case by Ethinicity'
                        }
                    })
                ])
            ])
        ])
    ]) # End of main body div
]) # End of layout



# Callback to update the total stop and search by selected police force
@callback(
    Output('total-search', 'children'),
    [Input('force-select', 'value')])
def update_total_search_by_force(selected_force = 'Cleveland Police'):
    """
    Updates the total number of stop and searches conducted by the selected police force.
        Parameters:
        - selected_force (str): The name of the police force to filter by.
        Returns:
        - A text element displaying the total number of stop and searches conducted by the selected police force.
    """
    total_cases = filterdf[filterdf['force_type'] == selected_force]['force_type'].shape[0]
    return html.H2(f'{total_cases}')

# Callback to update the total arrest by selected police force
@callback(
    Output('total-arrest', 'children'),
    [Input('force-select', 'value')])
def update_total_arrest(selected_force = 'Cleveland Police'):
    """
    Updates the total arrests made by the selected police force.

    """
    total_arrest = filterdf[(filterdf['force_type'] == selected_force) &
                           (filterdf['outcome'] == 'Arrest')].shape[0]
    return html.H2(f'{total_arrest}')

# Callback to update the arrest percentage case by selected police force
@callback(
    Output('percent-arrest', 'children'),
    [Input('force-select', 'value')])
def update_total_arrest_percent(selected_force = 'Cleveland Police'):
    """
    Updates the percentage of total cases that resulted in an arrest for the selected police force.
    Parameters:
        selected_force (str): The name of the selected police force.
    Returns:
        An HTML H2 element containing the percentage of total cases that resulted in an arrest for 
        the selected police force.
    """
    total_cases = filterdf[filterdf['force_type'] == selected_force]['force_type'].shape[0]
    total_arrest = filterdf[(filterdf['force_type'] == selected_force) & 
                            (filterdf['outcome'] == 'Arrest')].shape[0]
    total_arrest_percent = round(total_arrest / total_cases * 100, 2)
    return html.H2(f'{total_arrest_percent}%')


# Callback to update the histogram plot for stop and search by Age group
@callback(
    Output('search-histogram-plot', 'figure'),
    [Input('force-select', 'value')])
def update_histogram_plot(selected_force):
    """
    Updates the histogram plot showing the number of stop and search cases by age group for the selected police force.

    Parameters:
    - selected_force (str): The police force to filter the data by.

    Returns:
    - dict: A dictionary containing the data and layout for the plot.
    """
    filtered_df = filterdf[(filterdf['force_type'] == selected_force)]
    
    return {
        'data': [{
            'x': filtered_df['age_range'],
            'type': 'histogram'
        }],
        'layout': {
            'title': f'{selected_force} stop and search case breakdown by Age group'
        }
    }


# Callback to update the histogram plot for arrest by age group
@callback(
    Output('arrest-histogram-plot', 'figure'),
    [Input('force-select', 'value')])
def update_arrest_plot(selected_force):
    """
    Updates the histogram plot showing the breakdown of arrest cases by age group for the selected police force.

    Parameter:
    - selected_force (str): The name of the police force to filter the data by.

    Returns:
    - figure: A histogram plot showing the breakdown of arrest cases by age group for the selected police force.
    """
    filtered_df = filterdf[(filterdf['force_type'] == selected_force) &
                          (filterdf['outcome'] == 'Arrest')]
    return {
        'data': [{
            'x': filtered_df['age_range'],
            'type': 'histogram'
        }],
        'layout': {
            'title': f'{selected_force} Arrest case breakdown by Age group'
        }
    }

# Callback to update the histogram plot of stop and search case by ethinic group
@callback(
    Output('ethinic-histogram-plot', 'figure'),
    [Input('force-select', 'value')])
def update_ethinic_plot(selected_force):
    """
    Updates the histogram plot showing the breakdown of stop and search cases by ethnicity for the 
    selected police force.

    Parameters:
    - selected_force (str): The selected police force.

    Returns:
    - dict: A dictionary containing the data and layout for the histogram plot.
    """
    filtered_df = filterdf[(filterdf['force_type'] == selected_force)]
    return {
        'data': [{
            'x': filtered_df['officer_defined_ethnicity'],
            'type': 'histogram'
        }],
        'layout': {
            'title': f'{selected_force} Stop and search case breakdown by Ethinic group'
        }
    }

# Callback to update the arrest cases by gender pie chart
@callback(
    Output('pie-chart-arrest', 'figure'),
    [Input('force-select', 'value')])
def update_pie_chart_arrest(selected_force):
    """
    Updates the pie chart showing the number of arrest cases by gender for the selected police force.

    - Parameters: selected_force (str): The selected police force.

    - Returns: figure: A pie chart figure object with the updated data.
    """
    filtered_df = filterdf[(filterdf['force_type'] == selected_force) &
                           (filterdf['outcome'] == 'Arrest')]
    return {
        'data': [{
            'labels': filtered_df['gender'].value_counts().index.tolist(),                     
            'values': filtered_df['gender'].value_counts().tolist(),
            'type': 'pie'
        }],
        'layout': {
            'title': f'{selected_force} Arrest cases by Gender'
        }
    }

# Callback to update the total case by gender pie chart
@callback(
    Output('pie-chart-total', 'figure'),
    [Input('force-select', 'value')])
def update_pie_chart_arrest(selected_force):
    """
    Update the pie chart with total cases by gender for the selected police force.

    - Parameters: selected_force: (str) The selected police force to filter data.
    
    - Returns: A dictionary with data and layout for the pie chart.
    """
    filtered_df = filterdf[filterdf['force_type'] == selected_force]
    return {
        'data': [{
            'labels': filtered_df['gender'].value_counts().index.tolist(),                     
            'values': filtered_df['gender'].value_counts().tolist(),
            'type': 'pie'
        }],
        'layout': {
            'title': f'{selected_force} Total cases by Gender'
        }
    }
