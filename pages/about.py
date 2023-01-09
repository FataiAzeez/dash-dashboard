# import neccessary libraries, modules and packages
from dash import html, dcc


# creating a layout for the about page content
about_layout = html.Div(className='container-fluid', children=[
    html.Div(className='row', children=[
        # start of Nav bar column
        html.Div(className='col-md-12', children=[
            html.Nav(className='navbar navbar-expand-lg navbar-dark bg-dark', children=[
                html.Div(className='mr-5', children=[
                    html.A(className='navbar-brand', children='About Project'),
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
                            html.Li(className='nav-item', children=html.A(className='nav-link', 
                                                                          children='Stop and Search Dashboard', 
                                                                          href='/search', style={'color': 'white'})),
                            html.Li(className='nav-item', children=html.A(className='nav-link bg-light', 
                                                                          children='About Project', 
                                                                          href='/about', style={'color': 'black'})),
                        ])
                    ]),
                    html.Div(children=[
                        html.Li(className='btn btn-secondary', id='logout', 
                                children=html.A(children='Log Out', href='/', style={'color': 'white'}))
                    ])
                ])
            ])
        ]) #end of Nav bar column
    ]),

    # About title
    html.H1(className='text-center mt-5', children='About Project'),
    html.Div(className='row my-5 justify-content-center', children=[
        # Start of about page content 
        html.Div(className='col-md-8 text-center', children=[
            dcc.Markdown('''

                The UK COVID-19 and Police Stop and Search Dashboards provide valuable insights into the COVID-19 pandemic and police stop and search practices in the UK. 
                
                **The COVID-19 Dashboard** allows users to drill down and filter data by date, town, and age group, providing a detailed view of daily infection rates and percentage change rates in selected cities. 

                **The Stop and Search Dashboard** displays stop and search statistics for Cleveland and Northumbria Police forces for the month of August 2021, including the total number of stop and searches conducted, total arrests made, and breakdowns by gender, age group, and ethnic group. 

                These dashboards were developed as part of a course module at Teesside University and offer a powerful tool for understanding and analyzing important issues facing the UK.

            ''')
        ])  # End of about page content
    ]),
    
     # Start of about page footer content
    html.Footer(className='footer mt-5', children=[
        html.Div(className='container', children=[
            html.Div(className='row align-items-end mt-5', children=[
                html.Div(className='col-md-12', children=[ html.Div(className='text-center', 
                     children=html.P(className='text-muted', 
                                     children='Project developed by Fatai Olaimde Azeez Copyright 2023'))
                ])
            ])
        ])
    ]) # End of about page footer content

])