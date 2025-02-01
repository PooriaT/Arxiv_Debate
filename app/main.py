from calendar import c
import dash
from dash import Dash, html, dcc

app = Dash(__name__, use_pages=True)

app.layout = html.Div(
    [
        html.H1("ARXIV DEBATE DASHBOARD", className="container text-center"),
        html.Div(
            [
                html.Nav(
                    dcc.Link(f"{page['name']}", href=page["relative_path"]),
                    className="nav-link",
                )
                for page in dash.page_registry.values()
            ],
            className="navbar navbar-expand-lg bg-light",
        ),
        dash.page_container,
    ],
    className="container",
)

if __name__ == "__main__":
    app.run(debug=True)
