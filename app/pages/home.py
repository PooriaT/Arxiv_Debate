import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.arxiv_xml_extr import xml_to_dic
from apis.gemini_api import get_summarization

dash.register_page(__name__, path="/", name="Home", icon="fas fa-home")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.I(
                                    className="fas fa-brain fa-3x mb-3 text-primary"
                                ),
                                html.H1(
                                    "ArXiv Paper Summarization",
                                    className="display-4 mb-3",
                                ),
                                html.P(
                                    "Discover and understand research papers with AI-powered summaries",
                                    className="lead text-muted",
                                ),
                            ],
                            className="text-center py-5",
                        )
                    ]
                )
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H4(
                                            [
                                                html.I(className="fas fa-search me-2"),
                                                "Search ArXiv Papers",
                                            ],
                                            className="card-title mb-4",
                                        ),
                                        dbc.InputGroup(
                                            [
                                                dbc.Input(
                                                    id="input",
                                                    type="text",
                                                    placeholder="Enter your research topic (e.g., quantum physics)",
                                                    className="border-end-0",
                                                ),
                                                dbc.Button(
                                                    [
                                                        html.I(
                                                            className="fas fa-paper-plane"
                                                        ),
                                                        " Search",
                                                    ],
                                                    id="submit-button",
                                                    color="primary",
                                                    className="ms-0",
                                                ),
                                            ],
                                            size="lg",
                                            className="mb-3",
                                        ),
                                        html.Small(
                                            "Enter a topic or keyword to find relevant papers",
                                            className="text-muted",
                                        ),
                                        # Loading spinner
                                        dcc.Loading(
                                            id="loading",
                                            type="circle",
                                            color="#119DFF",
                                            fullscreen=True,
                                        ),
                                    ]
                                )
                            ],
                            className="shadow-sm mb-4",
                        )
                    ],
                    lg=8,
                    className="mx-auto",
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.H3(
                                            [
                                                html.I(className="fas fa-robot me-2"),
                                                "AI Summary",
                                            ],
                                            className="mb-0",
                                        )
                                    ],
                                    className="bg-light",
                                ),
                                dbc.CardBody(
                                    [
                                        dcc.Markdown(
                                            id="output_summary",
                                            className="prose max-w-none",
                                            style={
                                                "font-size": "1.1rem",
                                                "line-height": "1.7",
                                                "padding": "1rem",
                                            },
                                        )
                                    ]
                                ),
                            ],
                            className="shadow-sm mb-4",
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.H3(
                                            [
                                                html.I(
                                                    className="fas fa-newspaper me-2"
                                                ),
                                                "Related Articles",
                                            ],
                                            className="mb-0",
                                        )
                                    ],
                                    className="bg-light",
                                ),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            id="output-article",
                                            className="article-list",
                                        )
                                    ]
                                ),
                            ],
                            className="shadow-sm",
                        )
                    ]
                )
            ]
        ),
    ],
    fluid="md",
    className="py-4",
)


@dash.callback(
    [
        dash.Output("output_summary", "children"),
        dash.Output("output-article", "children"),
        dash.Output("loading", "active"),
    ],
    [dash.Input("submit-button", "n_clicks")],
    [dash.State("input", "value")],
)
def update_output(n_clicks, input_value):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    loading_state = ctx.triggered[0]["prop_id"].split(".")[0] == "submit-button"

    if not n_clicks or not input_value:
        raise dash.exceptions.PreventUpdate

    arxiv_data = xml_to_dic(input_value)
    articles = []

    for data in arxiv_data:
        articles.append(
            dbc.Card(
                [
                    dbc.CardBody(
                        [
                            html.H5(
                                [
                                    html.A(
                                        data["title"],
                                        href=data["link"],
                                        target="_blank",
                                        className="text-decoration-none",
                                    )
                                ],
                                className="card-title",
                            ),
                            html.Div(
                                [
                                    html.Span(
                                        [
                                            html.I(className="fas fa-users me-2"),
                                            f"Authors: {', '.join(data['authors'])}",
                                        ],
                                        className="me-3",
                                    ),
                                    html.Span(
                                        [
                                            html.I(className="fas fa-calendar me-2"),
                                            f"Published: {data['published'][:10]}",
                                        ]
                                    ),
                                ],
                                className="text-muted mb-3",
                            ),
                            html.P(
                                [
                                    html.I(className="fas fa-info-circle me-2"),
                                    f"Summary: {data['summary']}",
                                ],
                                className="mb-0",
                            ),
                        ]
                    )
                ],
                className="mb-3 shadow-sm",
            )
        )

    return get_summarization(arxiv_data), articles, loading_state


# Add custom CSS
app = dash.get_app()
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .article-list {
                max-height: 800px;
                overflow-y: auto;
                padding-right: 10px;
            }
            .article-list::-webkit-scrollbar {
                width: 8px;
            }
            .article-list::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 4px;
            }
            .article-list::-webkit-scrollbar-thumb {
                background: #888;
                border-radius: 4px;
            }
            .article-list::-webkit-scrollbar-thumb:hover {
                background: #555;
            }
            .prose {
                font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
