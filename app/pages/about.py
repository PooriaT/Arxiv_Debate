import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/about", name="About", icon="fa-info-circle")


GITHUB_REPOSITORY_URL = "https://github.com/PooriaT/Arxiv_Debate"
ISSUE_TRACKER_URL = "https://github.com/PooriaT/Arxiv_Debate/issues"
ARXIV_URL = "https://arxiv.org/"
TWITTER_URL = "https://x.com/PooriaTaghdiri"
DONATION_URL = "https://buymeacoffee.com/pooria7"


def _section_heading(icon_class, title):
    return html.H2(
        [
            html.I(
                className=f"{icon_class} me-2 text-primary",
                **{"aria-hidden": "true"},
            ),
            title,
        ],
        className="h4 card-title mb-3",
    )


def _link_item(icon_class, label, href):
    return dbc.ListGroupItem(
        [
            html.I(
                className=f"{icon_class} me-2",
                **{"aria-hidden": "true"},
            ),
            html.A(
                label,
                href=href,
                className="text-decoration-none",
                target="_blank",
                rel="noopener noreferrer",
            ),
        ],
        className="d-flex align-items-center",
    )


layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.I(
                                    className="fas fa-book-reader fa-3x mb-3 text-primary",
                                    **{"aria-hidden": "true"},
                                ),
                                html.H1("About ArXiv Debate", className="mb-3"),
                                html.P(
                                    "A simple way to find arXiv papers on a topic, "
                                    "review their abstracts, and get an AI-assisted "
                                    "starting-point summary.",
                                    className="lead text-muted mb-0",
                                ),
                            ],
                            className="text-center py-5",
                        )
                    ],
                    lg=10,
                    className="mx-auto",
                )
            ],
            className="mb-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    _section_heading(
                                        "fas fa-compass", "What ArXiv Debate does"
                                    ),
                                    html.P(
                                        "ArXiv Debate helps researchers, students, and "
                                        "curious readers quickly explore recent research "
                                        "around a topic. Enter a research question or topic, "
                                        "then use the returned papers and summary to decide "
                                        "what to read next.",
                                        className="lead mb-0",
                                    ),
                                ]
                            ),
                            className="shadow-sm h-100",
                        )
                    ],
                    lg=6,
                    className="mb-4",
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    _section_heading("fas fa-database", "Data source"),
                                    html.P(
                                        [
                                            "Paper metadata and abstracts come from ",
                                            html.A(
                                                "arXiv",
                                                href=ARXIV_URL,
                                                target="_blank",
                                                rel="noopener noreferrer",
                                            ),
                                            ", an open repository for scholarly preprints.",
                                        ],
                                        className="lead mb-0",
                                    ),
                                ]
                            ),
                            className="shadow-sm h-100",
                        )
                    ],
                    lg=6,
                    className="mb-4",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    html.H2(
                                        [
                                            html.I(
                                                className="fas fa-gears me-2 text-primary",
                                                **{"aria-hidden": "true"},
                                            ),
                                            "How it works",
                                        ],
                                        className="h4 mb-0",
                                    )
                                ),
                                dbc.CardBody(
                                    [
                                        dbc.ListGroup(
                                            [
                                                dbc.ListGroupItem(
                                                    [
                                                        html.Strong(
                                                            "1. Search a topic. "
                                                        ),
                                                        "Type a research topic, question, or area "
                                                        "you want to investigate.",
                                                    ]
                                                ),
                                                dbc.ListGroupItem(
                                                    [
                                                        html.Strong(
                                                            "2. Fetch related arXiv papers. "
                                                        ),
                                                        "The app searches arXiv for papers that "
                                                        "match your topic.",
                                                    ]
                                                ),
                                                dbc.ListGroupItem(
                                                    [
                                                        html.Strong(
                                                            "3. Review paper details. "
                                                        ),
                                                        "Results show available metadata such as "
                                                        "titles, authors, categories, dates, links, "
                                                        "and abstracts.",
                                                    ]
                                                ),
                                                dbc.ListGroupItem(
                                                    [
                                                        html.Strong(
                                                            "4. Read the AI-assisted summary. "
                                                        ),
                                                        "The app uses the fetched paper information "
                                                        "to generate a high-level synthesis that can "
                                                        "help you spot themes and choose which papers "
                                                        "to open first.",
                                                    ]
                                                ),
                                            ],
                                            flush=True,
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
                                    html.H2(
                                        [
                                            html.I(
                                                className="fas fa-triangle-exclamation me-2 text-warning",
                                                **{"aria-hidden": "true"},
                                            ),
                                            "AI summary limitations",
                                        ],
                                        className="h4 mb-0",
                                    )
                                ),
                                dbc.CardBody(
                                    [
                                        html.P(
                                            "The summary is meant to be a reading aid, not "
                                            "a substitute for the original research.",
                                            className="lead",
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    "arXiv papers are preprints and may not have "
                                                    "been peer reviewed."
                                                ),
                                                html.Li(
                                                    "AI summaries can be incomplete, outdated, "
                                                    "misleading, or wrong."
                                                ),
                                                html.Li(
                                                    "Read the original paper before relying on a "
                                                    "claim, citing it, or using it to make a "
                                                    "decision."
                                                ),
                                            ],
                                            className="mb-0",
                                        ),
                                    ]
                                ),
                            ],
                            color="warning",
                            outline=True,
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
                                    html.H2(
                                        [
                                            html.I(
                                                className="fas fa-link me-2 text-primary",
                                                **{"aria-hidden": "true"},
                                            ),
                                            "Project links",
                                        ],
                                        className="h4 mb-0",
                                    )
                                ),
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H3(
                                                            [
                                                                html.I(
                                                                    className="fab fa-github me-2",
                                                                    **{
                                                                        "aria-hidden": "true"
                                                                    },
                                                                ),
                                                                "Contribute",
                                                            ],
                                                            className="h5",
                                                        ),
                                                        dbc.ListGroup(
                                                            [
                                                                _link_item(
                                                                    "fas fa-code-branch",
                                                                    "GitHub repository",
                                                                    GITHUB_REPOSITORY_URL,
                                                                ),
                                                                _link_item(
                                                                    "fas fa-bug",
                                                                    "Issue tracker",
                                                                    ISSUE_TRACKER_URL,
                                                                ),
                                                            ],
                                                            flush=True,
                                                        ),
                                                    ],
                                                    md=6,
                                                    className="mb-4 mb-md-0",
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.H3(
                                                            [
                                                                html.I(
                                                                    className="fas fa-share-alt me-2",
                                                                    **{
                                                                        "aria-hidden": "true"
                                                                    },
                                                                ),
                                                                "Connect",
                                                            ],
                                                            className="h5",
                                                        ),
                                                        dbc.ListGroup(
                                                            [
                                                                _link_item(
                                                                    "fab fa-twitter",
                                                                    "Follow on X (Twitter)",
                                                                    TWITTER_URL,
                                                                ),
                                                                _link_item(
                                                                    "fas fa-coffee",
                                                                    "Buy me a Coffee",
                                                                    DONATION_URL,
                                                                ),
                                                            ],
                                                            flush=True,
                                                        ),
                                                    ],
                                                    md=6,
                                                ),
                                            ]
                                        )
                                    ]
                                ),
                            ],
                            className="shadow-sm mb-5",
                        )
                    ]
                )
            ]
        ),
    ],
    className="py-4",
)
