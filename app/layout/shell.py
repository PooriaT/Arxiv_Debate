import dash
from dash import html
import dash_bootstrap_components as dbc

from .footer import create_footer
from .navbar import create_navbar


def create_app_shell():
    return html.Div(
        [
            create_navbar(),
            dbc.Container(
                [
                    html.Div(dash.page_container, className="page-content"),
                    create_footer(),
                ],
                fluid=True,
                className="px-4",
            ),
        ]
    )
