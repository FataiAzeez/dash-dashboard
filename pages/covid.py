# import neccessary libraries, modules and packages
from dash import html, dcc, callback, Input, Output
import pandas as pd

# Import the COVID-19 data
main_df = pd.read_csv("https://github.com/FataiAzeez/dash-dashboard/blob/4519b0d1a11355d15473f6caf0165c495a53fce5/pages/covid_data.csv", 
                      engine='python', error_bad_lines=False)

#convert date column to DateTime format
#main_df['date'] = pd.to_datetime(main_df['date'])

# Create a copy of the main dataframe 
new_df = main_df.copy()

# creating list of cases
case_list = new_df[['newCasesBySpecimenDate-0_4', 'newCasesBySpecimenDate-0_59',
                     'newCasesBySpecimenDate-10_14', 'newCasesBySpecimenDate-15_19',
                     'newCasesBySpecimenDate-20_24', 'newCasesBySpecimenDate-25_29',
                     'newCasesBySpecimenDate-30_34', 'newCasesBySpecimenDate-35_39',
                     'newCasesBySpecimenDate-40_44', 'newCasesBySpecimenDate-45_49',
                     'newCasesBySpecimenDate-50_54', 'newCasesBySpecimenDate-55_59',
                     'newCasesBySpecimenDate-5_9', 'newCasesBySpecimenDate-60+',
                     'newCasesBySpecimenDate-60_64', 'newCasesBySpecimenDate-65_69',
                     'newCasesBySpecimenDate-70_74', 'newCasesBySpecimenDate-75_79',
                     'newCasesBySpecimenDate-80_84', 'newCasesBySpecimenDate-85_89',
                     'newCasesBySpecimenDate-90+']]

# Define the layout of the Covid page
covid_layout = html.Div(className='container-fluid', children=[
    #start of top navigation
    html.Div(className='row', children=[
        # start of Nav bar column
        html.Div(className='col-md-12', children=[
            html.Nav(className='navbar navbar-expand-lg navbar-dark bg-dark', children=[
                html.Div(className='mr-5', children=[
                    html.A(className='navbar-brand', children='COVID-19 Dashboard'),
                ]),
                
                html.Button(className='navbar-toggler', type='button', 
                            **{'data-toggle': 'collapse', 'data-target':'#navbarNav'}, children=[
                    html.Span(className='navbar-toggler-icon')
                ]),
                
                html.Div(id="navbarNav", className='collapse navbar-collapse mx-auto',  children=[
                    html.Div(className='mx-auto', children=[
                        html.Ul(className='navbar-nav mr-auto justify-content-center', children=[
                            html.Li(className='nav-item', children=html.A(className='nav-link bg-light',                                                                     
                                                                          children='Covid-19 Dashboard', 
                                                                          href='/covid', style={'color': 'black'})),
                            html.Li(className='nav-item', children=html.A(className='nav-link', 
                                                                          children='Stop and Search Dashboard', 
                                                                          href='/search', style={'color': 'white'})),
                            html.Li(className='nav-item', children=html.A(className='nav-link', 
                                                                          children='About Project', href='/about', 
                                                                          style={'color': 'white'})),
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
    
    # Start of side filter
    html.Div(className='row', children=[
        html.Div(className='col-md-3 mt-5', children=[
            html.Div(className='row', children=[
                # Start of Date picker 
                html.Div(className='col-md-12 mb-3', children=[
                    html.Div(className='card form-group', children=[
                        html.Div(className='card-body', children=[
                            html.Label('Select a Date'),
                                dcc.DatePickerRange(
                                id='date-picker',
                                end_date_placeholder_text="End Period",
                                calendar_orientation='vertical',

                                min_date_allowed=new_df['date'].min(),
                                max_date_allowed=new_df['date'].max(),
                                initial_visible_month=new_df['date'].min(),
                                start_date=new_df['date'].min(),
                                end_date=new_df['date'].max(),
                                style={'fontSize': '1.5rem'}
                            )                            
                        ])
                    ])
                ]), # End of Date picker section
                # Start of Area dropdown box
                html.Div(className='col-md-12', children=[
                    html.Div(className='card', children=[
                        html.Div(className='card-body', children=[
                            html.Div(className='form-group', children=[
                                html.Label('Select an Area'),
                                dcc.Dropdown(
                                    id='area-select',
                                    options=[{'label': area, 'value': area} for area in new_df['areaName'].unique()],
                                    value='Hartlepool'
                                )
                            ]),
                            html.Div(id='total-cases-by-area')
                        ])
                    ])
                ]),# End of Area dropdown picker

                # Start of Age group sepecimen dropdown picker
                html.Div(className='col-md-12 mt-3', children=[
                    html.Div(className='card', children=[
                        html.Div(className='card-body', children=[
                            html.Div(className='form-group', children=[
                                html.Label('Select Case Type'),
                                dcc.Dropdown(
                                    id='case-select-daily',
                                    options=[{'label': area, 'value': area} for area in case_list],
                                    value='newCasesBySpecimenDate-0_59'
                                )
                            ]),
                            html.Div(id='total-daily-cases')
                        ])
                    ])
                ]) # End of Age group sepecimen dropdown picker
            ])
        ]), #End of side filter pane
        

        html.Div(className='col-md-9', children=[
            # Bar showing the daily distribution of cases by area
            html.Div(className='row', children=[
                html.Div(className='col-md-12', children=[
                    dcc.Graph(id='histogram-plot', figure={
                        'data': [{
                            'x': new_df['date'].unique(),
                            'y': new_df['newCasesBySpecimenDate-0_59'],
                            'type': 'bar'
                        }],
                        'layout': {
                            'title': 'Breakdown of daily infection rate in Hartlepool by Specimen'
                        }
                    })
                ])
            ]),

            # Bar graph showing the number of cases over time
            html.Div(className='row', children=[
                html.Div(className='col-md-12', children=[
                    dcc.Graph(id='line-plot', figure={
                        'data': [{
                            'x': new_df['date'].unique(),
                            'y': new_df["newCasesBySpecimenDate-0_59"].diff() * 100,
                            'type': 'bar'
                        }],
                        'layout': {
                            'title': 'Breakdown of percentage change of infection rate in Hartlepool by Specimen'
                        }
                    })
                ])
            ]),

            # Pie chart showing the distribution of cases by region
            html.Div(className='row', children=[
                html.Div(className='col-md-12', children=[
                    dcc.Graph(id='pie-chart', figure={
                        'data': [{
                            'labels': new_df['areaType'],                     
                            'values': new_df['newCasesBySpecimenDate-0_59'],
                            'type': 'pie'
                        }],
                        'layout': {
                            'title': 'Cases by Area'
                        }
                    })
                ])
            ])
        ])
    ])
    ])




# Callback to update the total cases by area
@callback(
    Output('total-cases-by-area', 'children'),
    [Input('area-select', 'value'),
    Input('case-select-daily', 'value')])
def update_total_cases_by_area(selected_area, selected_case):
    """
    Updates the total cases by area based on the selected area and case value.
     
    """
    total_cases = new_df[new_df['areaName'] == selected_area][selected_case].sum()
    return html.H2(f'Total Cases: {total_cases}')

# Callback to update the total daily cases
@callback(
    Output('total-daily-cases', 'children'),
    [Input('case-select-daily', 'value')])
def update_total_daily_cases(selected_case):
    """
    Updates the total daily cases based on the selected case value.
    """
    total_daily_cases = new_df[selected_case].values[1]
    return html.H2(f'Total Daily Cases: {total_daily_cases}')


# Callback to update the bar plot
@callback(
    Output('histogram-plot', 'figure'),
    [Input('area-select', 'value'),
     Input('case-select-daily', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')])
def update_histogram_plot(selected_area, selected_case, start_date, end_date):
    """
    This function updates the bar plot based on the selected area, case, and date range.
    Parameters:
    - selected_area (str): the selected area name
    - selected_case (str): the selected case column name
    - start_date (str): the start date of the date range
    - end_date (str): the end date of the date range

    Returns:
    - dict: a dictionary containing data and layout for the plot
    """
    # Filter dataframe by selected area and date range
    filtered_df = new_df[(new_df['areaName'] == selected_area) & 
                         (new_df['date'] >= start_date) &
                         (new_df['date'] <= end_date)]
    
    return {
        'data': [{
            'x': filtered_df['date'].unique(),
            'y': filtered_df[selected_case],
            'type': 'bar'
        }],
        'layout': {
            'title': f'Breakdown of daily infection rate in {selected_area} by selected Specimen age group'
        }
    }

# Callback to update the are name dropdown option
@callback(
    Output('area-select', 'option'),
    [Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')])
def update_area_name(start_date, end_date):
    """
    Update the area dropdown options based on the selected date range.
        Parameters:
        - start_date: start date of the date range (string)
        - end_date: end date of the date range (string)
        Returns:
        - options: list of dictionaries containing the 'label' and 'value' for each option in the dropdown menu
    """
    options=[{'label': area, 'value': area} for area in new_df[(new_df['date'] >= start_date) &
                                                               (new_df['date'] <= end_date)]['areaName'].unique()]
    return options


# Callback to update the bar plot with percentage change rate for the selected area 
@callback(
    Output('line-plot', 'figure'),
    [Input('area-select', 'value'),
     Input('case-select-daily', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')])
def update_line_plot(selected_area, selected_case, start_date, end_date):
    """
    Updates the bar plot with percentage change rate for the selected area and selected case within 
    the selected date range.

    Parameters:
    - selected_area (str): name of the selected area
    - selected_case (str): name of the selected case
    - start_date (str): start date of the date range
    - end_date (str): end date of the date range

    Returns:
    - figure (dict): figure for the line plot
    
    """
    filtered_df = new_df[(new_df['areaName'] == selected_area) & 
                         (new_df['date'] >= start_date) &
                         (new_df['date'] <= end_date)]
    return {
        'data': [{
            'x': filtered_df['date'],
            'y': filtered_df[selected_case].diff()*100,
            'type': 'bar'
        }],
        'layout': {
            'title': f'Breakdown of percentage change rate in {selected_area} by selected Specimen age group'
        }
    }

# Callback to update the pie chart
@callback(
    Output('pie-chart', 'figure'),
    [Input('area-select', 'value'),
     Input('case-select', 'value')])
def update_pie_chart(selected_area, selected_case):
    """
    Updates the pie chart figure based on the selected area and case

    Parameters:
    - selected_area: string value representing the selected area
    - selected_case: string value representing the selected case

    Returns:
    - figure object containing the data and layout of the pie chart
    """
    filtered_df = new_df[new_df['areaName'] == selected_area]
    return {
        'data': [{
            'labels': filtered_df['areaName'],
            'values': filtered_df[selected_case],
            'type': 'pie'
        }],
        'layout': {
            'title': f'{selected_case} by Area'
        }
    }
