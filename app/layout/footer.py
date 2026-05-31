from datetime import date

from dash import html
import dash_bootstrap_components as dbc


def create_footer():
    return html.Footer(
        dbc.Container(
            [
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            html.P(
                                [
                                    f"© {date.today().year} ArXiv Debate Dashboard. ",
                                    html.Span(
                                        "Powered by Dash and Bootstrap",
                                        className="text-muted",
                                    ),
                                ],
                                className="text-center mb-0",
                            )
                        )
                    ]
                ),
            ]
        ),
        className="footer",
    )
