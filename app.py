# Import libraries
import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html
import dash 
import dash_table as dt
import dash_bootstrap_components as dbc
import plotly.express as px
from io import BytesIO
import pandas as pd
from wordcloud import WordCloud
import base64

# define the app 
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Constants
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# ==============================================
# Import the dataset or define the dataset to be used programmtically
# Data preparation will also take place here.
data = {
    'error_types': ['Fatal_Error', 'Notice_Error', 'Password_Auth_Failure', 'Warning', 'Parse_Error', 'Undefined'], 
    'frequency': [4, 8, 17, 14, 30, 21]
}

dfm = pd.DataFrame(data)

# ==============================================
# Graphs, diagrams and other illustrations will be defined here
WORD_CLOUD = html.Img(
    id="image_wc"
)

TABLE = dbc.Table.from_dataframe(dfm, striped=True, bordered=True, hover=True)

DASH_TABLE = dt.DataTable(
    columns=[{"name": i, "id": i} for i in dfm.columns],
    data=dfm.to_dict('records'),
    style_cell={'textAlign': 'left'},
    
)

import plotly.graph_objects as go

colors = ['lightslategray',] * 6
colors[1] = 'crimson'

fig = go.Figure(data=[go.Bar(
    x=data['error_types'],
    y=data['frequency'],
    marker_color=colors # marker color can be a single color value or an iterable
)])
fig.update_layout(title_text='Errors and Their Frequencies')

# ==============================================
# Metadata and attributes
colours = {
    'background': '#d3d3d3',
    'text': '#7FDBFF'
}

# ==============================================
# Create visualisation layout and components
NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(
                        dbc.NavbarBrand("ALFA Data Science Dashboard", className="ml-2")
                    ),
                ],
                align="center",
                no_gutters=True,
            ),
        )
    ],
    color="dark",
    dark=True,
    sticky="top",
)

card_content = [
    dbc.CardHeader("World Cloud"),
    dbc.CardBody(
        [
            html.H5("Most Frequent Errors", className="card-title"),
            html.P(
                WORD_CLOUD,
            ),
        ]
    ),
]
app.layout = html.Div(children=[
    NAVBAR,

    html.Div(
        style={'width': '80%', 'margin': 'auto', 'margin-top': '50px'}, 
        children=[
            TABLE,
        ],
    ),

    html.Div(
        children=[
            dcc.Graph(
                figure=fig,
            ),
        ],
    ),

    html.Div(
        style={'margin': '150px 150px'},
        children= [
            dbc.Card(card_content, color='success', outline=True)
        ]
    ),
])

def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    #print(d)
    wc = WordCloud(background_color=colours['background'], width=480, height=360)
    wc.fit_words(d)
    return wc.to_image()

@app.callback(dd.Output('image_wc', 'src'), [dd.Input('image_wc', 'id')])
def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=dfm).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

# ==============================================
# Run the program
if __name__ == '__main__':
    app.run_server(debug=True)