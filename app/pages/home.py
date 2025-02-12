from operator import ge
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.arxiv_xml_extr import xml_to_dic
from apis.gemini_api import get_summarization

dash.register_page(__name__, path="/", name="Home", icon="fas fa-home")
layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1("ArXiv Summarization"))),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Search for an arXiv item:"),
                        dbc.Input(
                            id="input", type="text", placeholder="e.g. quantum physics"
                        ),
                        dbc.Button(
                            "Submit",
                            id="submit-button",
                            color="primary",
                            className="mt-2",
                        ),
                        dcc.Loading(
                            id="loading",
                            type="circle",
                            color="#119DFF",
                            fullscreen=True,
                        ),
                    ]
                ),
            ]
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(dbc.Col(html.H2("AI Summarization"))),
                    dbc.Row(
                        dbc.Col(
                            dcc.Markdown(
                                id="output_summary",
                                style={"whiteSpace": "pre-wrap", "margin": "20px"},
                            )
                        )
                    ),
                ]
            ),
            className="mb-3",
            style={"margin": "10px"},
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(dbc.Col(html.H2("Related Articles"))),
                    dbc.Row(
                        dbc.Col(
                            [
                                html.Ul(id="output-article"),
                            ]
                        )
                    ),
                ]
            ),
            className="mb-3",
            style={"margin": "10px"},
        ),
    ]
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
            html.Li(
                [
                    html.A(data["title"], href=data["link"], target="_blank"),
                    html.P(f"Authors: {', '.join(data['authors'])}"),
                    html.P(f"Published: {data['published'][:10]}"),
                    html.P(f"Summary: {data['summary']}"),
                ]
            )
        )
    return get_summarization(arxiv_data), articles, loading_state
