import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H1('openssh layout goes here'),
    dcc.Link('Go home', href='/'),
])