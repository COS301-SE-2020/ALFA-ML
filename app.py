import dash.dependencies as dd
import dash_core_components as dcc
import dash_html_components as html
import dash 

from io import BytesIO

import pandas as pd
from wordcloud import WordCloud
import base64

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__) #, external_stylesheets=external_stylesheets)

dfm = pd.DataFrame({'word': ['apple', 'pear', 'orange'], 'freq': [1,3,9]})

app.layout = html.Div([
    html.Img(id="image_wc"),
])

def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(background_color='black', width=480, height=360)
    wc.fit_words(d)
    return wc.to_image()

@app.callback(dd.Output('image_wc', 'src'), [dd.Input('image_wc', 'id')])
def make_image(b):
    img = BytesIO()
    plot_wordcloud(data=dfm).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

if __name__ == '__main__':
    app.run_server(debug=True)