# import neccessary libraries, modules and packages
from dash import html, dcc, callback, Input, Output, State

# Creating the login form
form = html.Div(className='form-signin', children=[
    html.H1(className='h3 my-3 font-weight-normal text-center', children='Please sign in'),
    html.Label(className='sr-only', htmlFor='inputEmail', children='Email address'),
    dcc.Input(className='form-control mb-4', type='email', id='inputEmail', placeholder='Email address'),
    html.Label(className='sr-only mb-4', htmlFor='inputPassword', children='Password'),
    dcc.Input(className='form-control', type='password', id='inputPassword', placeholder='Password'),
    html.Button(className='btn btn-lg btn-primary btn-block mt-5 mb-4', id='submit-button', type='submit', 
                children='Sign in', n_clicks=0)
])

# Adding the form to the layout
login_layout = html.Div(id="page-content", className='container-fluid', children=[
    html.Div(className='row align-items-center justify-content-center mt-5', children=[
        html.Div(className='col-md-8 center mt-5', children=[
            html.Div(className='card text-center', children=[
                 html.Div(className='card-body', children=[
                    html.H3(className='card-title', children='Covid-19 & Stop and Search Monitoring Dashboard'),
                    html.P(className='card-text', 
                            children='Please login with your credential to access the dashboard')
                ])
            ])
        ])
    ]),
    html.Div(className='row align-items-center justify-content-center mt-2', children=[
        html.Div(className='col-md-3 mt-5', style={'backgroundColor': '#eeeeee'}, children=form)
    ]),
    
    html.Div(className='row align-items-end mt-5', children=[
        html.Div(className='col-md-12', children=[
            html.Div(className='text-center', 
                     children=html.P(className='text-muted', 
                                     children='Project developed by Fatai Olaimde Azeez Copyright 2023'))
        ])
    ])
])

# login callback 
@callback(
    Output('url', 'pathname'),
    [Input('submit-button', 'n_clicks')],
    [State('inputEmail', 'value'),
     State('inputPassword', 'value')])
def authenticate(n_clicks, inputEmail, inputPassword):
    """
    This authenticates the user and redirects to the appropriate page based on their credentials.
    If the email and password are valid, the user is redirected to '/covid'.

    If the email and password are invalid, the user is redirected back to '/' the login page.
    """
    if n_clicks is not None:
        if inputEmail == 'test@example.com' and inputPassword == 'password':
            return '/covid'
        else:
            return '/'
