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
from datetime import datetime

# Global Constants
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# define the app 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# =========================================================================
# Import the dataset

# Read file
file = open("preprocessing/error.txt", "r")
contents = ""
for i in range(5000):
    contents += str(file.readline())

# Data Wrangling
# split contents of file with respect to newline to make strings 
lines = contents.split('\n') # list of log entries

date_time_list = []
severity_level_list = []
dirty_list = []
for line in lines:
    pieces = line.split(" ")
    if len(pieces) > 11: # some lines are less than the minimum required length
	    date_time_list.append(" ".join([pieces[dt] for dt in range(5)]))
	    severity_level_list.append(pieces[5])
	    dirty_list.append(" ".join([pieces[e] for e in range(6,len(pieces),1)]))

# clean the error messages
error_msg_list = []
error_msg = ""
for dirty in dirty_list:
    dirty_pieces = dirty.split(" ")
    error_msg = ""
    for dirt_piece in dirty_pieces:
        if not any(char.isdigit() for char in dirt_piece):
            if not any(not char.isalnum() for char in dirt_piece):
                error_msg += dirt_piece + " "
    if error_msg:
        error_msg_list.append(error_msg.lower())

# clean and formate the dates
MONTH_MAP = {
    # map words to their digits representations
    "Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
    "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"
}
day_of_week_list = []
date_list = []
for date_time_str in date_time_list:
    date_time_str = date_time_str.replace('[','')
    date_time_str = date_time_str.replace(']','')
    date_time_pieces = date_time_str.split(" ")
    day_of_week_list.append(date_time_pieces[0])
    formatted_date_str = date_time_pieces[2] +"/"+ MONTH_MAP[date_time_pieces[1][:3]] +"/"+ date_time_pieces[4][2:]
    # convert date string to actual date object and append to date list
    date_list.append(datetime.strptime(formatted_date_str, '%d/%m/%y').date())

# create the dictionary of all the wrangled log file data
data = {
    "date_time": date_list,
    "day_of_the_week": day_of_week_list,
    "severity_level": severity_level_list,
    "error_messages": error_msg_list
}

# create the dataframe of all the data
df = pd.DataFrame(data)

# count how frequently each error messages occurs 
counts = df['error_messages'].value_counts()
unique_error_frequencies = {
    "unique_error_msgs": list(counts.index.values),
    "frequencies": counts.tolist()
}

"""
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
"""

# ===========================================================================
# Programs

# ===========================================================================
# Attributes
colours = {
    'background': '#000000',
    'text': '#7FDBFF'
}

colors = ['lightslategray',] * 6
colors[1] = 'crimson'

# ===========================================================================
# Graphs, diagrams and other illustrations will be defined here
WORD_CLOUD = html.Img(
    id="image_wc"
)

TABLE = dbc.Table.from_dataframe(
	df.head(10), 
	striped=True, 
	bordered=True, 
	hover=True
)

fig_bar_chart = go.Figure(data=[go.Bar(
    y=unique_error_frequencies['unique_error_msgs'],
    x=unique_error_frequencies['frequencies'],
    marker_color=colors, # marker color can be a single color value or an iterable
    orientation="h"
)])

fig_bar_chart.update_layout(title_text='Errors and Their Frequencies Bar Chart')


fig_pie_chart = go.Figure(data=[go.Pie(
	labels=unique_error_frequencies['unique_error_msgs'], 
	values=unique_error_frequencies['frequencies'], 
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
# ===============================================================================================================

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
    plot_wordcloud(data=pd.DataFrame(unique_error_frequencies)).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


# ================================================================================================================
# Run the program
if __name__ == '__main__':
    app.run_server(debug=True)