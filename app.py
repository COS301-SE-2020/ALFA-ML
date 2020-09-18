# Import libraries
import os
from dash.dependencies import Input, Output
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
import nltk
from nltk.tokenize import word_tokenize
import flask
import io

# define the app 
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

server = app.server

# ===========================================================================
# Attributes
colours = {
    'background': '#000000',
    'text': '#FFFFFF',
    'main-theme': '#7851A9'
}

colors = ['violet','purple', colours['main-theme']] * 6

# ================================================================================================
# Custom components to be appended to app layout
NAVBAR = dbc.Navbar(
    children=[
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(
                        dbc.NavbarBrand("ALFA Data Science Dashboard", className="ml-2")
                    ),
                    dbc.Col(
                    	dbc.Button(
                    		html.A(
					        	"Home",
					        	href="https://alfa-automated-log-analyzer.firebaseapp.com/",
			        		),
                    	),
			        	width='auto'
                    )
                ],
                no_gutters=True,
                align='center',
            ),
        ),
    ],
    color="dark",
    dark=True,
    sticky="top",
)

BADGES = html.Span(
    [
        dbc.Badge("Data Science", pill=True, color="primary", className="mr-1"),
        dbc.Badge("Machine Learning", pill=True, color="secondary", className="mr-1"),
        dbc.Badge("Visualisations", pill=True, color="success", className="mr-1"),
        dbc.Badge("Artificial Intelligence", pill=True, color="warning", className="mr-1"),
        dbc.Badge("PyraSpace (Pty) Ltd ", pill=True, color="danger", className="mr-1"),
        dbc.Badge("Technology", pill=True, color="info", className="mr-1"),
        dbc.Badge("Project ALFA", pill=True, color="light", className="mr-1"),
        dbc.Badge("Dark Mode", pill=True, color="dark"),
    ]
)

"""
TABLE = dbc.Table.from_dataframe(
	df.head(5), 
	striped=True, 
	bordered=True, 
	hover=True,
	dark=True,
)
"""

# ===============================================================================================
# app.layout describes what the app will look like
# html.Title('ALFA | Dashboard')
app.layout = html.Div(children=[	
    NAVBAR,

    html.Div(
    	id='stats-facts',
    ),

	dbc.Jumbotron(
		[
			html.H1("ALFA Dashboard", className="display-3"),
			html.P(
			    "Made for the most productive, modern-day Data Scientist & Machine Learning Engineer.",
			    className="lead",
			),
			BADGES,
			html.Hr(className="my-2"),
			html.Div(
		    	style={'margin': 'auto'},
		    	children=[
		    		dcc.Upload(
				        id='upload-data',
				        children=html.Div([
		            		'Drag and Drop or ',
		            		html.A('Select Log Files to Visualise')
				        ]),
				        style={
				            'width': '98%',
				            'height': '60px',
				            'lineHeight': '60px',
				            'borderWidth': '1px',
				            'borderStyle': 'dashed',
				            'borderRadius': '5px',
				            'textAlign': 'center',
				            'margin': '10px'
		        		},
				        # Allow multiple files to be uploaded
				        multiple=True
					),
		    	]
		    ),
		]
	),

    html.Div(
    	id='data-table-output',
        style={'width': '80%', 'margin': 'auto', 'margin-top': '50px'}, 
    ),


    html.Div(
    	[
    		dbc.Row(
	            [
	                dbc.Col(html.Div(
						id='output-bar-chart',
					),),
	            ],
	            align="center",
        	),

        	dbc.Row(
        		[
	    			 dbc.Col(html.Div(
					    	id='output-pie-chart',
					    	#style={'margin': '8rem'},
				    	),),
	    			 dbc.Col(html.Div(
					    	id='output-pie-chart-2',
					    	#style={'margin': '8rem'},
				    	),),
        		],
        		align="center",
        	),

        	dbc.Row(
        		[
        			dbc.Col(
	                	html.Div(
					    	id='output-wordcloud',
					        children= [
					        	html.Div(
					        		style={'margin-left': '6rem', 'margin-right':'6rem'},
					        		children=[
						        		html.Img(
										    id="image_wc",
										    width='100%',
										    height='100%',
										),
					        		]
					        	)
					        ]
					    ),
	                ),
        		],
        		align="center",
        	),
    	]
    ),
    html.Footer(
		'All rights reserved. Made by PyraSpace 2020',
		style={'textAlign': 'center', 'margin-top': '4.5rem', 'color': colours['main-theme']}
	),
], 
	style={
		'overflow-x': 'hidden'
	},
) 

# =====================================================================================

# INTERACTIVENESS
def parse_contents(contents):
	#decoded = base64.b64decode(contents)

	#lines = decoded.split('\n')

	#print(contents)
	content_type, content_string = contents.split(',')

	decoded = base64.b64decode(content_string).decode("utf-8")
	
	lines = decoded.split('\n')[:500]

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
		error_msg = " ".join(error_msg.split(" ")[:5])
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
	global data 
	data = {
		"date": date_list,
		"day_of_the_week": day_of_week_list,
		"severity_level": severity_level_list,
		"error_messages": error_msg_list
	}

	return data

# Populating the data table
@app.callback(Output('data-table-output', 'children'),
              [Input('upload-data', 'contents')])
def update_output(contents):
	if contents is not None:
		the_data = parse_contents(contents[0])
		df = pd.DataFrame(the_data)
		children = [
			html.H3("Data Table"),
			dbc.Table.from_dataframe(
				df.head(5), 
				striped=True, 
				bordered=True, 
				hover=True,
				dark=True,
			),
		]
		return children

# Creating the bar chart
@app.callback(Output('output-bar-chart', 'children'),
			[Input('upload-data', 'contents')])
def create_bar_chart(contents):
	if contents is not None:
		# create the dataframe of all the data
		the_data = parse_contents(contents[0])
		df = pd.DataFrame(the_data)

		# count how frequently each error messages occurs 
		counts = df['error_messages'].value_counts()
		unique_error_frequencies = {
		    "unique_error_msgs": list(counts.index.values)[:8],
		    "frequencies": counts.tolist()[:8]
		}

		fig_bar_chart = go.Figure(data=[go.Bar(
		    y=unique_error_frequencies['unique_error_msgs'],
		    x=unique_error_frequencies['frequencies'],
		    marker_color=colors, # marker color can be a single color value or an iterable
		    orientation="h"
		)])

		fig_bar_chart.update_layout(
			plot_bgcolor=colours['background'],
			paper_bgcolor=colours['background'],
		   	font_color=colours['text'],
		   	xaxis=dict(
		   		title='Frequency',
		   		titlefont_size=16,
		   		tickfont_size=15,
		   	),
		   	yaxis=dict(
		        title='Error Messages',
		        titlefont_size=16,
		        tickfont_size=11,
		    ),
		)

		children = [
			dcc.Graph(
				style={'padding-left': '80px', 'padding-right': '80px'},  
				figure=fig_bar_chart
			)
		]

		return children

# creating pie chart 1
@app.callback(Output('output-pie-chart', 'children'),
			[Input('upload-data', 'contents')])
def create_pie_chart(contents):
	if contents is not None:
		# create the dataframe of all the data
		the_data = parse_contents(contents[0])
		df = pd.DataFrame(the_data)

		# count how frequently each error messages occurs 
		counts = df['error_messages'].value_counts()
		unique_error_frequencies = {
		    "unique_error_msgs": list(counts.index.values)[:8],
		    "frequencies": counts.tolist()[:8]
		}

		fig_pie_chart = go.Figure(data=[go.Pie(
			labels=unique_error_frequencies['unique_error_msgs'][:8], 
			values=unique_error_frequencies['frequencies'][:8], 
			hole=.3)
		])

		fig_pie_chart.update_layout(
			plot_bgcolor=colours['background'],
			paper_bgcolor=colours['background'],
			font_color=colours['text'],
		)

		children = [
			dbc.Row(
				[
					dbc.Col(dcc.Graph(figure=fig_pie_chart)),
				]
			)
		]

		return children

# creating pie chart 2
@app.callback(Output('output-pie-chart-2', 'children'),
			[Input('upload-data', 'contents')])
def create_pie_chart(contents):
	if contents is not None:
		# create the dataframe of all the data
		the_data = parse_contents(contents[0])
		df = pd.DataFrame(the_data)

		# count how frequently each error messages occurs 
		counts = df['severity_level'].value_counts()
		unique_severity_lvl_frequencies = {
		    "unique_severity_levels": list(counts.index.values)[:8],
		    "frequencies": counts.tolist()[:8]
		}

		fig_pie_chart = go.Figure(data=[go.Pie(
			labels=unique_severity_lvl_frequencies['unique_severity_levels'][:8], 
			values=unique_severity_lvl_frequencies['frequencies'][:8], 
			hole=.3)
		])

		fig_pie_chart.update_layout(
			plot_bgcolor=colours['background'],
			paper_bgcolor=colours['background'],
			font_color=colours['text'],
		)

		children = [
			dbc.Row(
				[
					dbc.Col(dcc.Graph(figure=fig_pie_chart)),
				]
			)
		]

		return children

# create numerical data
@app.callback(Output('stats-facts', 'children'),
			[Input('upload-data', 'contents')])
def retrieve_stats(contents):
	if contents is not None:
		# create the dataframe of all the data
		the_data = parse_contents(contents[0])
		df = pd.DataFrame(the_data)

		earliest_date = min(df['date'])
		latest_date = max(df['date'])
		error_counts = df['error_messages'].nunique()	
		day_most_occuring = df['day_of_the_week'].mode().tolist()[0]

		children = [
			dbc.CardGroup(
	    		[
	    			dbc.Card(
	    				dbc.CardBody(
	    					[
	    						html.H2(earliest_date, className="card-title"),
	    						html.P("Earliest Date in the Log File", className="card-text",),
	    					]
	    				),
	    				color='primary',
	    				inverse=True,
	    			),
	    			dbc.Card(
	    				dbc.CardBody(
	    					[
	    						html.H2(error_counts, className="card-title"),
	    						html.P("Error Types Detected", className="card-text",),
	    					]
	    				),
	    				color='warning',
	    				inverse=True,
	    			),
	    			dbc.Card(
	    				dbc.CardBody(
	    					[
	    						html.H2(day_most_occuring, className="card-title"),
	    						html.P("Day of the Week Most Errors Occur", className="card-text",),
	    					]
	    				),
	    				color='info',
	    				inverse=True,
	    			),
	    			dbc.Card(
	    				dbc.CardBody(
	    					[
	    						html.H2(latest_date, className="card-title"),
	    						html.P("Latest Date in the Log File", className="card-text",),
	    					]
	    				),
	    				color='light',
	    				inverse=True,
	    			),
	    		]
	    	)
		]

		return children

# ===============================================================================================================
# # create the WordCloud
def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(background_color=colours['background'], width=780, height=460)
    wc.fit_words(d)
    return wc.to_image()

@app.callback(Output('image_wc', 'src'), 
               [Input('upload-data', 'contents')])
def make_image(contents):
	if contents is not None:
		# create the dataframe of all the data
		the_data = parse_contents(contents[0])
		df = pd.DataFrame(the_data)

		# count how frequently each error messages occurs 
		counts = df['error_messages'].value_counts()
		unique_error_frequencies = {
			"unique_error_msgs": list(counts.index.values)[:8],
			"frequencies": counts.tolist()[:8]
		}
		img = BytesIO()
		plot_wordcloud(data=pd.DataFrame(unique_error_frequencies)).save(img, format='PNG')
		return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

# # ================================================================================================================
# Run the program
if __name__ == '__main__':
    app.run_server(debug=True)
