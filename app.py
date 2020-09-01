import pandas as pd
import plotly.express as px

import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------
# Import and clean data
df = pd.read_csv("intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

# ------------------------------------------
# App layout
# remember: what does inside your 'App Layout' is your dash components i.e dropdowns, graphs, checkboxes

app.layout = html.Div([

    html.H1(
        "Web Application Dashboards with Dash", 
        style={'text-align': 'center'}
    ),

    dcc.Dropdown(
        id='slct_year',
        options=[
            {'label': '2015', 'value': 2015},
            {'label': '2016', 'value': 2016},
            {'label': '2017', 'value': 2017},
            {'label': '2018', 'value': 2018}
        ],
        multi=False,
        value=2015,
        style={'width': '40%'}
    ),

    html.Div(
        id='output_container',
        children=[]
    ),

    html.Br(),

    dcc.Graph(
        id='my_bee_map',
        figure={}
    )
])

# -------------------------------------
# Connect the Plotly graphs with the Dash components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]   

)
# this is the function definition of the callback
# each parameter is connected to the number of inputs -> parameter always refers to the component_property
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    # return value 1
    container = "The year chosen by the user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff['Year'] == option_slctd]
    dff = dff[dff['Affected by'] == 'Varroa_mites']
    
    # Plotly Express
    # return value 2
    fig = px.choropleth(
        data_frame=dff,
        locationmode='USA-states',
        locations='state_code',
        scope='usa',
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )
    
    # return in the order of the outputs
    return container, fig



# -------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
