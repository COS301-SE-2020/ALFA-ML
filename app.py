import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html
import dash 

from io import BytesIO

import pandas as pd
from wordcloud import WordCloud
import base64

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__) #, external_stylesheets=external_stylesheets)

# ==============================================
# Import the dataset or define the dataset to be used programmtically
# Data preparation will also take place here.
dfm = pd.DataFrame({'word': ['PHP Fatal Error', 'PHP Notice', 'Password Auth Failure'], 'freq': [1,3,9]})

# ==============================================
# Graphs, diagrams and other illustrations will be defined here


# ==============================================
# Metadata and attributes
colours = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# ==============================================
# Create visualisation layout
app.layout = html.Div(style={'backgroundColor': 'red'}, children=[
    html.H1(
        "ALFA-ML WordCloud Prototype",
        style={
            'textAlign': 'center',
            'color': colours['text']
        }
    ),

    html.Img(
        id="image_wc"
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