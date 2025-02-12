import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about", name="About", icon="fa-info-circle")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.I(
                                    className="fas fa-book-reader fa-3x mb-3 text-primary"
                                ),
                                html.H1("About ArXiv Debate", className="mb-3"),
                                html.P(
                                    "Discover and analyze the latest research papers with AI-powered insights",
                                    className="lead text-muted",
                                ),
                            ],
                            className="text-center py-5",
                        )
                    ]
                )
            ],
            className="mb-5",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.H3(
                                            [
                                                html.I(
                                                    className="fas fa-rocket me-2 text-primary"
                                                ),
                                                "Our Mission",
                                            ],
                                            className="card-title mb-4",
                                        ),
                                        html.P(
                                            """
                        This is the AI-driven app to help you have an overview of recent Arxiv papers.
                        It is only required to search the desired topic and the app will provide you
                        with the summary of the most relevant papers.
                        """,
                                            className="lead",
                                        ),
                                    ]
                                )
                            ],
                            className="shadow-sm mb-5",
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
                                                    className="fas fa-link me-2 text-primary"
                                                ),
                                                "Connect & Contribute",
                                            ],
                                            className="mb-0",
                                        )
                                    ]
                                ),
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Card(
                                                            [
                                                                dbc.CardBody(
                                                                    [
                                                                        html.H5(
                                                                            [
                                                                                html.I(
                                                                                    className="fab fa-github me-2"
                                                                                ),
                                                                                "GitHub",
                                                                            ],
                                                                            className="card-title",
                                                                        ),
                                                                        dbc.ListGroup(
                                                                            [
                                                                                dbc.ListGroupItem(
                                                                                    [
                                                                                        html.I(
                                                                                            className="fas fa-code-branch me-2"
                                                                                        ),
                                                                                        dcc.Link(
                                                                                            "Project Repository",
                                                                                            href="https://github.com/PooriaT/Arxiv_Debate",
                                                                                            className="text-decoration-none",
                                                                                            target="_blank",
                                                                                        ),
                                                                                    ],
                                                                                    className="d-flex align-items-center",
                                                                                ),
                                                                                dbc.ListGroupItem(
                                                                                    [
                                                                                        html.I(
                                                                                            className="fas fa-bug me-2"
                                                                                        ),
                                                                                        dcc.Link(
                                                                                            "Issue Tracker",
                                                                                            href="https://github.com/PooriaT/Arxiv_Debate/issues",
                                                                                            className="text-decoration-none",
                                                                                            target="_blank",
                                                                                        ),
                                                                                    ],
                                                                                    className="d-flex align-items-center",
                                                                                ),
                                                                            ],
                                                                            flush=True,
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                            className="h-100 shadow-sm",
                                                        )
                                                    ],
                                                    md=6,
                                                    className="mb-4",
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Card(
                                                            [
                                                                dbc.CardBody(
                                                                    [
                                                                        html.H5(
                                                                            [
                                                                                html.I(
                                                                                    className="fas fa-share-alt me-2"
                                                                                ),
                                                                                "Social",
                                                                            ],
                                                                            className="card-title",
                                                                        ),
                                                                        dbc.ListGroup(
                                                                            [
                                                                                dbc.ListGroupItem(
                                                                                    [
                                                                                        html.I(
                                                                                            className="fab fa-twitter me-2"
                                                                                        ),
                                                                                        dcc.Link(
                                                                                            "Follow on X (Twitter)",
                                                                                            href="https://x.com/PooriaTaghdiri",
                                                                                            className="text-decoration-none",
                                                                                            target="_blank",
                                                                                        ),
                                                                                    ],
                                                                                    className="d-flex align-items-center",
                                                                                ),
                                                                                dbc.ListGroupItem(
                                                                                    [
                                                                                        html.I(
                                                                                            className="fas fa-coffee me-2"
                                                                                        ),
                                                                                        dcc.Link(
                                                                                            "Buy me a Coffee",
                                                                                            href="https://buymeacoffee.com/pooria7",
                                                                                            className="text-decoration-none",
                                                                                            target="_blank",
                                                                                        ),
                                                                                    ],
                                                                                    className="d-flex align-items-center",
                                                                                ),
                                                                            ],
                                                                            flush=True,
                                                                        ),
                                                                    ]
                                                                )
                                                            ],
                                                            className="h-100 shadow-sm",
                                                        )
                                                    ],
                                                    md=6,
                                                    className="mb-4",
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                            ],
                            className="shadow mb-5",
                        )
                    ]
                )
            ]
        ),
    ],
    className="py-4",
)
