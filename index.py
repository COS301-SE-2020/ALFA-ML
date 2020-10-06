import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import apache, openssh, landing

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(
        id='page-content',
    )
])


# Update the page
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apache':
        return apache.layout
    elif pathname == '/openssh':
        return openssh.layout
    else:
        return landing.layout


# ---------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
