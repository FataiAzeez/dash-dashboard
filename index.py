# import neccessary libraries, modules and packages
from dash import html, dcc, Input, Output
from app import app
from pages import covid, search, about, login

# embedding the layout 
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# callback function to generate appropriate layout
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    """
    Renders the app with the appropriate layout based on the URL pathname.

    - Parameter: pathname: the URL pathname of the page to be displayed.

    - Output: The layout of the page corresponding to the URL pathname.
    """
    if pathname == '/':
        return login.login_layout
    if pathname == '/covid':
        return covid.covid_layout
    elif pathname == '/search':
       return search.search_layout
    elif pathname == '/about':
        return about.about_layout
    else:
        return login.login_layout

# run the app
if __name__ == '__main__':
    app.run()