from calendar import c
import dash
from dash import html, dcc

dash.register_page(__name__, path="/about")

layout = (
    html.Div(
        [
            html.H1("ABOUT", className="container text-center"),
            html.Div(
                [
                    html.Div(
                        [
                            html.P(
                                """
                                This is the AI-driven app to help you have an overview of recent Arxiv papers.
                                It is only required to search the desired topic and the app will provide you
                                  with the summary of the most relevant papers.
                            """,
                                className="container",
                            ),
                        ],
                    ),
                    html.Div(
                        [
                            html.H3("Contact & Information"),
                            html.Div(
                                [
                                    html.P("Report Issues:  ", className="d-md-inline"),
                                    dcc.Link(
                                        "GitHub Issue Tracker",
                                        href="https://github.com/PooriaT/Arxiv_Debate/issues",
                                        className="d-md-inline",
                                    ),
                                ],
                                className="container",
                            ),
                            html.Div(
                                [
                                    html.P("Project Link:  ", className="d-md-inline"),
                                    dcc.Link(
                                        "GitHub Repository",
                                        href="https://github.com/PooriaT/Arxiv_Debate",
                                        className="d-md-inline",
                                    ),
                                ],
                                className="container",
                            ),
                            html.Div(
                                [
                                    html.P(
                                        "Support the developer:  ",
                                        className="d-md-inline",
                                    ),
                                    dcc.Link(
                                        "Buy me a Coffee",
                                        href="https://buymeacoffee.com/pooria7",
                                        className="d-md-inline",
                                    ),
                                ],
                                className="container",
                            ),
                            html.Div(
                                [
                                    html.P(
                                        "Follow the developer on X:  ",
                                        className="d-md-inline",
                                    ),
                                    dcc.Link(
                                        "Pooria's X",
                                        href="https://x.com/PooriaTaghdiri",
                                        className="d-md-inline",
                                    ),
                                ],
                                className="container",
                            ),
                        ],
                        className="container",
                    ),
                ],
                className="container",
            ),
        ],
    ),
)
