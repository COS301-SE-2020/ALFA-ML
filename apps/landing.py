import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

badges = html.Span(
    [
        dbc.Badge("Data Science", pill=True, color="primary", className="mr-1"),
        dbc.Badge("Machine Learning", pill=True, color="secondary", className="mr-1"),
        dbc.Badge("Visualisations", pill=True, color="success", className="mr-1"),
        dbc.Badge("Artificial Intelligence", pill=True, color="warning", className="mr-1"),
        dbc.Badge("PyraSpace Software", pill=True, color="danger", className="mr-1"),
        dbc.Badge("Technology", pill=True, color="info", className="mr-1"),
        dbc.Badge("Project ALFA", pill=True, color="light", className="mr-1"),
        dbc.Badge("Dark Mode", pill=True, color="dark"),
    ]
)

log_file_options = dbc.CardDeck(
    [
        # dbc.Card([
        #     dbc.CardBody(
        #         [
        #             html.H3("OpenSSH", className="card-title"),
        #             html.P(
        #                 "OpenSSH is the premier connectivity tool for remote login with the SSH protocol. ",
        #                 className="card-text",
        #             ),
        #         ],
        #     ),
        #     dbc.CardFooter([
        #         dbc.Button("Go to Dashboard", color="light", outline=True, href="/openssh"),
        #     ], style={'background': '#282828'}),
        # ]),
        dbc.Card([
            dbc.CardBody(
                [
                    html.H3("Apache", className="card-title"),
                    html.P(
                        "Apache HTTP Server is one of the most popular web servers "
                        "Apache servers usually generate two types of logs: access logs and error logs.",
                        className="card-text",
                    ),
                ],
            ),
            dbc.CardFooter([
                dbc.Button("Go to Dashboard", color="light", outline=True, href="/apache"),
            ], style={'background': '#282828'}),
        ]),
        # dbc.Card(
        #     dbc.CardBody(
        #         [
        #             html.H3("Spark", className="card-title"),
        #             html.P(
        #                 "This card has some text content, which is longer "
        #                 "than both of the other two cards, in order to "
        #                 "demonstrate the equal height property of cards in a "
        #                 "card group.",
        #                 className="card-text",
        #             ),
        #             dbc.Button(
        #                 "Click here", color="danger", className="mt-auto"
        #             ),
        #         ]
        #     )
        # ),
        # dbc.Card(
        #     dbc.CardBody(
        #         [
        #             html.H3("Hadoop", className="card-title"),
        #             html.P(
        #                 "This card has some text content, which is longer "
        #                 "than both of the other two cards, in order to "
        #                 "demonstrate the equal height property of cards in a "
        #                 "card group.",
        #                 className="card-text",
        #             ),
        #             dbc.Button(
        #                 "Click here", color="danger", className="mt-auto"
        #             ),
        #         ]
        #     )
        # ),
    ]
)

layout = html.Div(
    style={
        'overflow-x': 'hidden',
        'margin-left': '3rem', 'margin-right': '3rem'
    },
    children=[
        dbc.Jumbotron(
            [
                dbc.Fade(
                    html.H1("ALFA Dashboard", className="display-3"),
                    is_in=True,
                    style={"transition": "opacity 2000ms ease"}),
                dbc.Fade(
                    [
                        html.P(
                            "Made for the most productive, modern-day Data Scientist & Machine Learning Engineer.",
                            className="lead",
                        ),
                        badges
                    ],
                    is_in=True,
                    style={"transition": "opacity 2000ms ease"}
                ),
            ],
            className='shadow-lg bg-black rounded',
        ),
        html.Div([
            log_file_options,
        ]),
    ],
)