import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from app.components.article_card import render_article_cards
from app.services.search_workflow import get_default_search_workflow

dash.register_page(__name__, path="/", name="Home", icon="fas fa-home")

layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                html.P(
                                    [
                                        html.I(
                                            className="fas fa-magnifying-glass me-2"
                                        ),
                                        "arXiv search with AI-assisted synthesis",
                                    ],
                                    className="text-uppercase text-primary fw-semibold mb-2",
                                ),
                                html.H1(
                                    "Find arXiv papers and summarize the research",
                                    className="display-5 fw-semibold mb-3",
                                ),
                                html.P(
                                    "Search for a research topic, choose how many papers to fetch, "
                                    "and submit to generate an AI-assisted summary with related arXiv articles.",
                                    className="lead text-muted mb-0",
                                ),
                            ],
                            className="text-center py-4 py-lg-5",
                        )
                    ],
                    lg=9,
                    className="mx-auto",
                )
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.H2(
                                                    [
                                                        html.I(
                                                            className="fas fa-search me-2"
                                                        ),
                                                        "Search arXiv",
                                                    ],
                                                    className="h4 card-title mb-2",
                                                ),
                                                html.P(
                                                    "Use a concise topic or field name so the search can find relevant papers.",
                                                    className="text-muted mb-4",
                                                ),
                                            ]
                                        ),
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Label(
                                                            "Research topic",
                                                            html_for="input",
                                                            className="fw-semibold",
                                                        ),
                                                        dbc.InputGroup(
                                                            [
                                                                dbc.Input(
                                                                    id="input",
                                                                    type="text",
                                                                    placeholder="e.g., large language models",
                                                                    className="border-end-0",
                                                                ),
                                                                dbc.Button(
                                                                    [
                                                                        html.I(
                                                                            className="fas fa-paper-plane me-2"
                                                                        ),
                                                                        "Search",
                                                                    ],
                                                                    id="submit-button",
                                                                    color="primary",
                                                                    className="ms-0",
                                                                ),
                                                            ],
                                                            size="lg",
                                                            className="mb-2",
                                                        ),
                                                        dbc.FormText(
                                                            [
                                                                "Good searches are specific research areas, such as ",
                                                                html.Strong(
                                                                    "large language models"
                                                                ),
                                                                ", ",
                                                                html.Strong(
                                                                    "graph neural networks"
                                                                ),
                                                                ", or ",
                                                                html.Strong(
                                                                    "protein folding"
                                                                ),
                                                                ".",
                                                            ],
                                                            className="d-block",
                                                        ),
                                                    ],
                                                    lg=9,
                                                ),
                                                dbc.Col(
                                                    [
                                                        dbc.Label(
                                                            "Max results",
                                                            html_for="max-results",
                                                            className="fw-semibold",
                                                        ),
                                                        dbc.Input(
                                                            id="max-results",
                                                            type="number",
                                                            min=5,
                                                            max=50,
                                                            step=1,
                                                            value=10,
                                                            size="sm",
                                                            className="max-results-input mb-2",
                                                        ),
                                                        dbc.FormText(
                                                            "Fetch 5 to 50 papers. Larger result sets may take longer.",
                                                            className="d-block",
                                                        ),
                                                    ],
                                                    lg=3,
                                                    className="mt-4 mt-lg-0",
                                                ),
                                            ],
                                            className="g-4 align-items-start",
                                        ),
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
                    lg=10,
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
                                        html.Div(
                                            [
                                                html.H2(
                                                    [
                                                        html.I(
                                                            className="fas fa-robot me-2"
                                                        ),
                                                        "AI-assisted summary",
                                                    ],
                                                    className="h4 mb-1",
                                                ),
                                                html.P(
                                                    "The generated synthesis appears here after a search.",
                                                    className="text-muted mb-0",
                                                ),
                                            ]
                                        )
                                    ],
                                    className="bg-light",
                                ),
                                dbc.CardBody(
                                    [
                                        dcc.Markdown(
                                            id="output_summary",
                                            children="Enter a research topic above to generate an AI-assisted summary of matching arXiv papers.",
                                            className="prose summary-output result-placeholder mb-0",
                                        )
                                    ]
                                ),
                            ],
                            className="shadow-sm h-100",
                        )
                    ],
                    lg=5,
                    className="mb-4 mb-lg-0",
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(
                                    [
                                        html.Div(
                                            [
                                                html.H2(
                                                    [
                                                        html.I(
                                                            className="fas fa-newspaper me-2"
                                                        ),
                                                        "Related articles",
                                                    ],
                                                    className="h4 mb-1",
                                                ),
                                                html.P(
                                                    "Matching papers render here as article cards.",
                                                    className="text-muted mb-0",
                                                ),
                                            ]
                                        )
                                    ],
                                    className="bg-light",
                                ),
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            [
                                                html.P(
                                                    "Search results will list the related arXiv papers here.",
                                                    className="result-placeholder mb-0",
                                                )
                                            ],
                                            id="output-article",
                                            className="article-list",
                                        )
                                    ]
                                ),
                            ],
                            className="shadow-sm h-100",
                        )
                    ],
                    lg=7,
                ),
            ],
            className="g-4 align-items-stretch",
        ),
    ],
    fluid="md",
    className="py-4",
)


@dash.callback(
    [
        dash.Output("output_summary", "children"),
        dash.Output("output-article", "children"),
        dash.Output("loading", "children"),
    ],
    [dash.Input("submit-button", "n_clicks")],
    [dash.State("input", "value"), dash.State("max-results", "value")],
)
def update_output(n_clicks, input_value, max_results):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise dash.exceptions.PreventUpdate

    loading_state = ctx.triggered[0]["prop_id"].split(".")[0] == "submit-button"

    query = (input_value or "").strip()
    if not n_clicks or not query:
        raise dash.exceptions.PreventUpdate

    normalized_max_results = _normalize_max_results(max_results)
    if normalized_max_results is None:
        return (
            "Max number of research papers must be between 5 and 50.",
            [],
            loading_state,
        )

    result = get_default_search_workflow().search(query, normalized_max_results)
    summary = result.error or result.summary_error or result.summary or ""

    return summary, render_article_cards(result.articles), loading_state


def _normalize_max_results(max_results):
    try:
        normalized = int(max_results)
    except (TypeError, ValueError):
        return None

    if not 5 <= normalized <= 50:
        return None

    return normalized
