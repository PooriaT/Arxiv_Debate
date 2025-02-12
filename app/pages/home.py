import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", external_stylesheets=[dbc.themes.BOOTSTRAP])

layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1("This is our Home page"))),
        dbc.Row(dbc.Col(html.Div("This is our Home page content."))),
    ]
)
