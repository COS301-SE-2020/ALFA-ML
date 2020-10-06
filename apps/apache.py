import urllib

from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import plotly.graph_objects as go
from datetime import datetime
import dash_table
import time

from app import app

colours = {
    'background': '#282828',
    'text': '#FFFFFF',
    'main-theme': '#7851A9'
}

colors = ['violet', 'purple', colours['main-theme']] * 6

layout = html.Div(
    style={
        'overflow-x': 'hidden',
        'margin-left': '2rem', 'margin-right': '2rem', 'margin-bottom': '4rem'
    },
    children=[
        html.Div(
            style={
                'margin': 'auto'
            },
            children=[
                dbc.Modal(
                    [
                        dbc.ModalHeader("Upload Log File to Visualise"),
                        dbc.ModalBody([
                            dbc.FormGroup(
                                [
                                    dbc.FormText("Add a report title to identify what the visualisation about.",
                                                 color='white'),
                                    dbc.Input(type="text", id="report-title", placeholder="Title goes here"),
                                ]
                            ),
                            html.Br(),
                            html.Div(id='show-filename'),
                            dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Log File to Visualise')
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
                                multiple=True,
                            ),
                            # dcc.Loading(
                            #     id="loading-1",
                            #     type="graph",
                            #     children=html.Div(id="loading-output-1"),
                            #     fullscreen=True, 
                            #     style={'background': 'black'}
                            # ),
                        ]),
                        dbc.ModalFooter([
                            dbc.Button(
                                "Home", id="modal-back", className="mr-auto", href='/'
                            ),
                            dbc.Button(
                                "Visualise", id="upload-centered", className="ml-auto", n_clicks=0, color='primary'
                            ),
                        ]),
                    ],
                    id="modal-centered",
                    centered=True,
                    is_open=True,
                    size='md'
                ),
            ]
        ),

        # Layout with Rows starts here
        dbc.Row(
            id="report-heading",
        ),

        html.Br(),

        dbc.Row(
            id='stats-facts',
        ),

        html.Br(),

        dbc.Row([
            dbc.Modal(
                [
                    dbc.ModalHeader("What did you discover?"),
                    dbc.ModalBody(dbc.Textarea(className="mb-3", placeholder="Write some notes", persistence=True)),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close-table-notepad-btn", className="ml-auto"
                        )
                    ),
                ],
                id="table-notepad",
                scrollable=True,
            ),
        ]),

        html.Br(),

        dash_table.DataTable(id='the-data-table'),

        html.Hr(className="my-6"),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Row([
                        dbc.Button("Make a Note", id='open-table-notepad-btn', color='info',
                                   style={'margin-left': '20px', 'display': 'none'}),
                    ]),
                    width='auto'
                ),

                dbc.Col(
                    dbc.Row([
                        dbc.Button(
                            [
                                html.A('Export to CSV File',
                                       id='export-csv-link',
                                       download="data-table.csv",
                                       href="",
                                       target="_blank",
                                       )
                            ],
                            id='export-table-btn',
                            color='dark',
                            style={'margin-left': '5px', 'display': 'none'},
                        ),
                    ]),
                    width='auto'
                )
            ]
        ),

        html.Br(),

        dbc.Row(
            id='data-table-output',
            justify='center',
            # style={'width': '80%'},
        ),

        html.Br(),

        html.Div(
            id='email-sent-confirm',
        ),

        html.Br(),
        dbc.Row([
            dbc.Modal(
                [
                    dbc.ModalHeader("What did you discover?"),
                    dbc.ModalBody(dbc.Textarea(className="mb-3", placeholder="Write some notes", persistence=True, id='bar-notes')),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close-bar-graph-notepad-btn", className="ml-auto"
                        )
                    ),
                ],
                id="bar-graph-notepad",
                scrollable=True,
            ),

            dbc.Modal(
                [
                    dbc.ModalHeader("Who's the Recipient?"),
                    dbc.ModalBody(dbc.Input(id="bar-email-recipient", placeholder="johndoe@gmail.com", type="email")),
                    dbc.ModalFooter(
                        dbc.Button("Send", id="close-bar-email", className="ml-auto")
                    ),
                ],
                id="bar-email-modal",
            ),
        ]),

        html.Br(),

        dbc.Row([
            dbc.Col(
                dbc.Row([
                    dbc.Button("Make a Note", id='open-bar-graph-notepad-btn', color='info',
                                style={'margin-left': '20px', 'display': 'none'}),
                ]),
                width='auto'
            ),

            # dbc.Col(
            #     [
            #         dbc.Row([
            #             dbc.Button(
            #                 [
            #                     "Share via Email",
            #                 ],
            #                 id='email-bar-btn',
            #                 color='info',
            #                 style={'margin-left': '20px', 'display': 'none'}
            #             ),
            #         ]),
            #     ],
            #     width='auto'
            # )

        ]),
        html.Br(),
        dbc.Row(
            align="center",
            children=[
                dbc.Col(
                    html.Div(id='output-bar-chart')
                ),
            ],
        ),

        html.Br(),

        html.Hr(className="my-6"),

        dbc.Row([
            dbc.Modal(
                [
                    dbc.ModalHeader("What did you discover?"),
                    dbc.ModalBody(dbc.Textarea(className="mb-3", placeholder="Write some notes", persistence=True, id='pie-notes')),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close-pie-charts-notepad-btn", className="ml-auto"
                        )
                    ),
                ],
                id="pie-charts-notepad",
                scrollable=True,
            ),
        ]),

        html.Br(),

        dbc.Row(
            dbc.Col(
                dbc.Row([
                    dbc.Button("Make a Note", id='open-pie-charts-notepad-btn', color='info',
                               style={'margin-left': '20px', 'display': 'none'}),
                ])
            )
        ),
        html.Br(),
        dbc.Row(
            align="center",
            children=[
                dbc.Col(html.Div(
                    id='output-pie-chart',
                    # style={'margin': '8rem'},
                ), ),
                dbc.Col(html.Div(
                    id='output-pie-chart-2',
                    # style={'margin': '8rem'},
                ), ),
            ],
        ),

        html.Br(),

        html.Hr(className="my-6"),

        dbc.Row([
            dbc.Modal(
                [
                    dbc.ModalHeader("What did you discover?"),
                    dbc.ModalBody(dbc.Textarea(className="mb-3", placeholder="Write some notes", persistence=True, id='line-notes')),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close-line-chart-notepad-btn", className="ml-auto"
                        )
                    ),
                ],
                id="line-chart-notepad",
                scrollable=True,
            ),
        ]),

        html.Br(),

        dbc.Row(
            dbc.Col(
                dbc.Row([
                    dbc.Button("Make a Note", id='open-line-chart-notepad-btn', color='info',
                               style={'margin-left': '20px', 'display': 'none'}),
                ])
            )
        ),
        html.Br(),
        dbc.Row(
            children=[
                dbc.Col(
                    html.Div(id='output-line-chart')
                ),
            ],
        ),
        html.Hr(className="my-6"),
    ],
)


# Helper functions and callback functions start here

# @app.callback(Output("loading-output-1", "children"), 
#             [Input("upload-data", "contents")],
#             [State('upload-data', 'loading_state')]
# )
# def input_triggers_spinner(contents, loading_state):
#     if contents is not None:
#         print(type(loading_state))
#         time.sleep(4)
#         return []
#     else:
#         return []

# @app.callback(
#     Output('email-sent-confirm', 'children'),
#     [Input('close-bar-email', 'n_clicks')],
#     [State('upload-data','contents'),
#      State('bar-email-recipient', 'value'),
#      State('bar-notes', 'value'),
#      State('pie-notes', 'value'),
#      State('line-notes', 'value'),
#      State('report-title', 'value')]
# )
# def email_bar(n, contents, recipient, notes_bar, notes_pie, notes_line, title):
#     if n is not None:
#         if n:
#             df = pd.DataFrame(parse_contents(contents[0]))
#             fig1 = create_bar_chart(df)[1]
#             fig2 = create_line_chart(df)[1]
#             fig3 = create_pie_chart_1(df)[1]
#             fig4 = create_pie_chart_2(df)[1]

#             image_bytes1 = fig1.to_image(format='png', width=800, height=550, scale=2)
#             image_bytes2 = fig2.to_image(format='png', width=800, height=550, scale=2)
#             image_bytes3 = fig3.to_image(format='png', width=800, height=550, scale=2)
#             image_bytes4 = fig4.to_image(format='png', width=800, height=550, scale=2)

#             image_bytes_list = [image_bytes1, image_bytes2, image_bytes3, image_bytes4]
#             notes_list = [notes_bar, notes_line, notes_pie, ""]

#             send_email(image_bytes_list, recipient, notes_list, "ALFA Dashboard-" + title)

#             # return dbc.Toast(
#             #     "This toast is placed in the top right",
#             #     id="positioned-toast",
#             #     header="Positioned toast",
#             #     is_open=False,
#             #     dismissable=True,
#             #     icon="danger",
#             #     # top: 66 positions the toast below the navbar
#             #     style={"position": "fixed", "top": 66, "right": 10, "width": 950},
#             # )
#             return dbc.Alert("Success! Email Sent!", color="success")


# def send_email(image_bytes_list, recipient_, notes_list, subject_):
#     me = "pyraspace301@gmail.com"
#     recipient = recipient_
#     subject = subject_

#     email_server_host = 'smtp.gmail.com'
#     port = 587
#     email_username = me
#     email_password = 'pyraspace2020!'

#     import smtplib
#     from email.mime.multipart import MIMEMultipart
#     from email.mime.text import MIMEText
#     from email.mime.image import MIMEImage
#     import os

#     msg = MIMEMultipart('alternative')
#     msg['From'] = me
#     msg['To'] = recipient
#     msg['Subject'] = subject

#     for i in range(4):
#         if notes_list[i] == "":
#             notes_list[i] = "ALFA Dashboard Graphs by PyraSpace"
#         msg.attach(MIMEText(notes_list[i]))
#         msg.attach(MIMEImage(image_bytes_list[i], name='alfa_dashboard_graph'))

#     server = smtplib.SMTP(email_server_host, port)
#     server.ehlo()
#     server.starttls()
#     server.login(email_username, email_password)
#     server.sendmail(me, recipient, msg.as_string())
#     server.close()

#     return None





@app.callback(
    Output('show-filename', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data','filename')]
)
def show_uploaded_filename(contents, filename):
    if contents is not None:
        children = [
            dbc.Badge(filename, color="danger", className="mr-1"), 
        ]
        return children
    else:
        return []


@app.callback(
    [Output('data-table-output', 'children'),
     Output('output-bar-chart', 'children'),
     Output('output-line-chart', 'children'),
     Output('output-pie-chart', 'children'),
     Output('output-pie-chart-2', 'children'),
     Output('stats-facts', 'children'),
     Output('report-heading', 'children'),
     Output('upload-centered', 'is_open'),
     Output('open-table-notepad-btn', 'style'),
     Output('open-bar-graph-notepad-btn', 'style'),
     Output('open-pie-charts-notepad-btn', 'style'),
     Output('open-line-chart-notepad-btn', 'style'),
     Output('export-table-btn', 'style')],
    [Input('upload-centered', 'n_clicks')],
    [State('upload-data', 'contents'),
     State('report-title', 'value'),
     State('upload-centered', 'is_open')]
)
def input(n_clicks, contents, report_title, is_open):
    global dash_title
    dash_title = report_title
    s_shown = {'margin-left': '20px', 'display': 'block'}
    s_hidden = {'margin-left': '20px', 'display': 'none'}
    if n_clicks >= 1:
        if is_open:
            state = False
        if contents is not None:
            df = pd.DataFrame(parse_contents(contents[0]))
            return (create_data_table(df), create_bar_chart(df)[0], create_line_chart(df)[0],
                    create_pie_chart_1(df)[0], create_pie_chart_2(df)[0], retrieve_stats(df),
                    create_report_title(report_title), False, s_shown, s_shown, s_shown, s_shown, 
                    {'margin-left': '5px', 'display': 'block'})

    return [], [], [], [], [], [], [], True, s_hidden, s_hidden, s_hidden, s_hidden, {'margin-left': '5px', 'display': "none"}

def create_report_title(title):
    return dbc.Col(
        dbc.Jumbotron(
            [
                html.H4(title, className="display-4"),
                html.Hr(className="my-2"),
                html.P(dbc.Button("Home", color="primary", href='/'), className="lead"),
            ],
        ),
        width=12
    )


def parse_contents(contents):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string).decode("utf-8")

    lines = decoded.split('\n')[:500]

    date_time_list = []
    severity_level_list = []
    dirty_list = []
    for line in lines:
        pieces = line.split(" ")
        if len(pieces) > 11:  # some lines are less than the minimum required length
            date_time_list.append(" ".join([pieces[dt] for dt in range(5)]))
            severity_level_list.append(pieces[5])
            dirty_list.append(" ".join([pieces[e] for e in range(6, len(pieces), 1)]))

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
        "Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06",
        "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"
    }
    day_of_week_list = []
    date_list = []
    for date_time_str in date_time_list:
        date_time_str = date_time_str.replace('[', '')
        date_time_str = date_time_str.replace(']', '')
        date_time_pieces = date_time_str.split(" ")
        day_of_week_list.append(date_time_pieces[0])
        formatted_date_str = date_time_pieces[2] + "/" + MONTH_MAP[date_time_pieces[1][:3]] + "/" + date_time_pieces[4][
                                                                                                    2:]
        # convert date string to actual date object and append to date list
        date_list.append(datetime.strptime(formatted_date_str, '%d/%m/%y').date())

    # create the dictionary of all the wrangled log file data
    data = {
        "date": date_list,
        "day_of_the_week": day_of_week_list,
        "severity_level": severity_level_list,
        "error_messages": error_msg_list
    }

    return data


def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# app.callback(
#     Output("bar-email-modal", "is_open"),
#     [
#         Input("email-bar-btn", "n_clicks"),
#         Input("close-bar-email", "n_clicks"),
#     ],
#     [State("bar-email-modal", "is_open")],
# )(toggle_modal)

app.callback(
    Output("table-notepad", "is_open"),
    [
        Input("open-table-notepad-btn", "n_clicks"),
        Input("close-table-notepad-btn", "n_clicks"),
    ],
    [State("table-notepad", "is_open")],
)(toggle_modal)

app.callback(
    Output("bar-graph-notepad", "is_open"),
    [
        Input("open-bar-graph-notepad-btn", "n_clicks"),
        Input("close-bar-graph-notepad-btn", "n_clicks"),
    ],
    [State("bar-graph-notepad", "is_open")],
)(toggle_modal)

app.callback(
    Output("bar-chart-notepad", "is_open"),
    [
        Input("open-bar-chart-notepad-btn", "n_clicks"),
        Input("close-bar-chart-notepad-btn", "n_clicks"),
    ],
    [State("bar-chart-notepad", "is_open")],
)(toggle_modal)

app.callback(
    Output("line-chart-notepad", "is_open"),
    [
        Input("open-line-chart-notepad-btn", "n_clicks"),
        Input("close-line-chart-notepad-btn", "n_clicks"),
    ],
    [State("line-chart-notepad", "is_open")],
)(toggle_modal)

app.callback(
    Output("pie-charts-notepad", "is_open"),
    [
        Input("open-pie-charts-notepad-btn", "n_clicks"),
        Input("close-pie-charts-notepad-btn", "n_clicks"),
    ],
    [State("pie-charts-notepad", "is_open")],
)(toggle_modal)


def create_data_table(df):
    children = [
        dash_table.DataTable(
            id='the-data-table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            page_size=16,
            editable=True,
            row_deletable=True,
            filter_action="native",

            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white',
                'fontWeight': 'bold'
            },
            style_cell={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white',
                'textAlign': 'left',
                'padding-left': '50px',
                'padding-right': '50px',
                'font-size': '1.06vw'
            },
            style_filter={
                'backgroundColor': 'lightgrey',
                'color': 'white',
                'fontWeight': 'bold'
            },
        )
    ]
    return children


@app.callback(Output('export-csv-link', 'href'),
              [Input('export-table-btn', 'n_clicks')],
              [State('the-data-table', 'data')])
def export_as_csv(n_clicks, data):
    if n_clicks is not None and data is not None:
        if n_clicks >= 1:
            dfm = pd.DataFrame(data)
            csv_string = dfm.to_csv(index=False, encoding='utf-8')
            csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + urllib.parse.quote(csv_string)
            return csv_string


def create_bar_chart(df):
    # count how frequently each error messages occurs
    counts = df['error_messages'].value_counts()
    unique_error_frequencies = {
        "unique_error_msgs": list(counts.index.values)[:8],
        "frequencies": counts.tolist()[:8]
    }

    fig_bar_chart = go.Figure(data=[go.Bar(
        x=unique_error_frequencies['unique_error_msgs'],
        y=unique_error_frequencies['frequencies'],
        marker_color=colors,  # marker color can be a single color value or an iterable
        orientation="v"
    )])

    fig_bar_chart.update_layout(
        plot_bgcolor=colours['background'],
        paper_bgcolor=colours['background'],
        font_color=colours['text'],
        xaxis=dict(
            title='Error Messages',
            titlefont_size=16,
            tickfont_size=11,
        ),
        yaxis=dict(
            title='Frequency',
            titlefont_size=16,
            tickfont_size=11,
        ),
    )

    children = [
        dcc.Graph(
            # style={'padding-left': '80px', 'padding-right': '80px'},
            figure=fig_bar_chart,
        )
    ]

    output = [children, fig_bar_chart]

    return output


def create_line_chart(df):
    # convert date to datetime object
    df['date'] = pd.to_datetime(df['date'])

    # extract only the unique years and put them in a list
    df['Year'] = pd.DatetimeIndex(df['date']).year
    years_list = df['Year'].unique().tolist()

    # count the number of errors in each year and put results in a list
    error_per_year = df.groupby(pd.Grouper(key='date', freq='Y'))['error_messages'].count().tolist()

    fig_line_chart = go.Figure()

    fig_line_chart.add_trace(go.Scatter(x=years_list, y=error_per_year, name="spline", line_shape='spline'))

    fig_line_chart.update_traces(hoverinfo='text+y', mode='lines+markers')
    fig_line_chart.update_layout(
        plot_bgcolor=colours['background'],
        paper_bgcolor=colours['background'],
        font_color=colours['text'],
        legend=dict(
            traceorder='reversed', font_size=16
        ),
        xaxis=dict(
            title='Year',
            titlefont_size=16,
            tickfont_size=11,
        ),
        yaxis=dict(
            title='Frequency',
            titlefont_size=16,
            tickfont_size=11,
        ),
    )

    children1 = [
        dcc.Graph(
            figure=fig_line_chart,
        )
    ]

    output = [children1, fig_line_chart]

    return output


def create_pie_chart_1(df):
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

    output = [children, fig_pie_chart]

    return output


def create_pie_chart_2(df):
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

    output = [children, fig_pie_chart]
    return output


def retrieve_stats(df):
    earliest_date = str(min(df['date']))
    earliest_date = earliest_date.split()[0]
    latest_date = str(max(df['date']))
    latest_date = latest_date.split()[0]
    error_counts = df['error_messages'].nunique()
    day_most_occuring = df['day_of_the_week'].mode().tolist()[0]

    children = [
        dbc.Col(
            dbc.Fade(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2(earliest_date, className="card-title"),
                            html.P("Earliest Date in the Log File", className="card-text", ),
                        ]
                    ),
                    color='primary',
                    inverse=True,
                ),
                is_in=True,
                style={"transition": "opacity 1000ms ease"}
            ),
            width=3,
            className='shadow-lg bg-black rounded',
        ),

        dbc.Col(
            dbc.Fade(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2(error_counts, className="card-title"),
                            html.P("Error Types Detected", className="card-text", ),
                        ]
                    ),
                    color='warning',
                    inverse=True,
                ),
                is_in=True,
                style={"transition": "opacity 3000ms ease"}
            ),
            width=3,
            className='shadow-lg bg-black rounded',
        ),

        dbc.Col(
            dbc.Fade(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2(day_most_occuring, className="card-title"),
                            html.P("Most Errors Occur on this day", className="card-text", ),
                        ]
                    ),
                    color='info',
                    inverse=True,
                ),
                is_in=True,
                style={"transition": "opacity 5000ms ease"}
            ),
            width=3,
            className='shadow-lg bg-black rounded',
        ),

        dbc.Col(
            dbc.Fade(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2(latest_date, className="card-title"),
                            html.P("Latest Date in the Log File", className="card-text", ),
                        ]
                    ),
                    color='light',
                    inverse=True,
                ),
                is_in=True,
                style={"transition": "opacity 7000ms ease"}
            ),
            width=3,
            className='shadow-lg bg-black rounded'
        ),
    ]

    return children


# Email functionality
# @app.callback(
#     Output('email-sent-confirmation', 'children'),
#     [Input('send-email-btn', 'n_clicks')]
# )
# def send_email(n):
#     if n is not None:
#         #import chart_studio.plotly as py
#         if n >= 1:
#             all_graphs = [
#                 #'https://plotly.com/~christopherp/308'
#                 graphs[0]
#             ]
#
#             from IPython.display import display, HTML
#
#             template = (''
#                         '<img src="data:image/png;base64,{image}">'
#                         '{caption}'  # Optional caption to include below the graph
#                         '<br>'
#                         '<hr>'
#                         '')
#
#             # A collection of Plotly graphs
#             figures = [
#                 {'data': [{'x': [1, 2, 3], 'y': [3, 1, 6]}], 'layout': {'title': 'the first graph'}},
#                 {'data': [{'x': [1, 2, 3], 'y': [3, 7, 6], 'type': 'bar'}], 'layout': {'title': 'the second graph'}}
#             ]
#
#             # Generate their images using `py.image.get`
#             images = [base64.b64encode(py.image.get(figure)).decode("ascii") for figure in figures]
#
#             email_body = ''
#             for image in images:
#                 _ = template
#                 _ = _.format(image=image, caption='')
#                 email_body += _
#
#             display(HTML(email_body))
#
#             me = 'pakoaba@gmail.com'
#             recipient = 'u17076146@tuks.co.za'
#             subject = 'Graph Report'
#
#             email_server_host = 'smtp.gmail.com'
#             port = 587
#             email_username = me
#             email_password = ''
#
#             import smtplib
#             from email.mime.multipart import MIMEMultipart
#             from email.mime.text import MIMEText
#             import os
#
#             msg = MIMEMultipart('alternative')
#             msg['From'] = me
#             msg['To'] = recipient
#             msg['Subject'] = subject
#
#             msg.attach(MIMEText(email_body, 'html'))
#
#             server = smtplib.SMTP(email_server_host, port)
#             server.ehlo()
#             server.starttls()
#             server.login(email_username, email_password)
#             server.sendmail(me, recipient, msg.as_string())
#             server.close()
#
#             return dbc.Alert(html.H5("Email Sent!", className="alert-heading"), color="success", dismissable=True, duration=4000, fade=True)


