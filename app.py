# Import libraries
import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html
import dash 
import dash_bootstrap_components as dbc
import plotly.express as px
from io import BytesIO
import pandas as pd
from wordcloud import WordCloud
import base64
import plotly.graph_objects as go

# Global Constants
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# define the app 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# =========================================================================
# Import the dataset
# Data preparation will also take place here.
data = {
    'error_types': ['Fatal_Error', 'Notice_Error', 'Password_Auth_Failure', 'Warning', 'Parse_Error', 'Undefined'], 
    'frequency': [4, 8, 1, 14, 150, 3]
}

data1 = {
    'error_types': ['Fatal_Error', 'Notice_Error', 'Password_Auth_Failure', 'Warning', 'Parse_Error', 'Undefined'], 
    'frequency': [4, 8, 17, 14, 30, 21],
    'date': ['Sat Feb 19 01:02:23.406157 2018','Sun Mar 08 01:02:23.406157 2018','Thur Jun 07 01:02:23.406157 2018','Tue Jul 12 01:02:23.406157 2018', 'Fri Aug 04 01:02:23.406157 2018','Sat Sep 11 01:02:23.406157 2018'],
    'client': ['127.0.0.1:57668','127.0.0.1:57668','127.0.0.1:57668','127.0.0.1:57668','127.0.0.1:57668','127.0.0.1:57668']
}

dfm = pd.DataFrame(data)
dfm1 = pd.DataFrame(data1)

# =============================================================
# App attributes
colours = {
    'background': '#d3d3d3',
    'text': '#7FDBFF'
}

colors = ['lightslategray',] * 6
colors[1] = 'crimson'

# ===========================================================================
# Graphs, diagrams and other illustrations will be defined here
WORD_CLOUD = html.Img(
    id="image_wc"
)

TABLE = dbc.Table.from_dataframe(dfm1, striped=True, bordered=True, hover=True)

fig_bar_chart = go.Figure(data=[go.Bar(
    y=data['error_types'],
    x=data['frequency'],
    marker_color=colors, # marker color can be a single color value or an iterable
    orientation="h"
)])

fig_bar_chart.update_layout(title_text='Errors and Their Frequencies Bar Chart')


fig_pie_chart = go.Figure(data=[go.Pie(
	labels=data['error_types'], 
	values=data['frequency'], 
	hole=.3)
])

fig_pie_chart.update_layout(title_text='Errors and Their Frequencies Pie Chart')


# ==============================================================
# Custom components to be appended to app layout
NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="40px")),
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
    dbc.CardHeader("Word Cloud"),
    dbc.CardBody(
        [
            html.H5("Most Frequent Errors", className="card-title"),
            html.P(
                WORD_CLOUD,
            ),
        ]
    ),
]

# =============================================================
# app.layout describes what the app will look like
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
                figure=fig_bar_chart,
            ),
        ],
    ),

    html.Div(
        children=[
            dcc.Graph(
                figure=fig_pie_chart,
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
# =================================================================

# create the WordCloud
def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(background_color=colours['background'], width=480, height=360)
    wc.fit_words(d)
    return wc.to_image()

@app.callback(dd.Output('image_wc', 'src'), 
               [dd.Input('image_wc', 'id')])
def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=dfm).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

# ==============================================
# Run the program
if __name__ == '__main__':
    app.run_server(debug=True)