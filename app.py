# import neccessary libraries, modules and packages
import dash

# Create a Dash app with Bootstrap styling
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[
    'https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css'],
      meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

server = app.server
app.config.suppress_callback_exceptions = True