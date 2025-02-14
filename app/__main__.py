import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from datetime import date

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css",
    ],
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(
                [html.I(className="fas fa-book-reader me-2"), "ARXIV DEBATE DASHBOARD"],
                className="ms-2",
                style={"fontSize": "1.5rem", "fontWeight": "bold"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                [
                                    html.I(
                                        className=f"fas {page.get('icon', 'fa-circle')} me-2"
                                    ),
                                    f"{page['name']}",
                                ],
                                href=page["relative_path"],
                                active="exact",
                                className="nav-link-custom",
                            )
                        )
                        for page in dash.page_registry.values()
                    ],
                    className="ms-auto",
                    navbar=True,
                ),
                id="navbar-collapse",
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .nav-link-custom {
                transition: all 0.3s ease;
                border-radius: 5px;
                margin: 0 5px;
            }
            .nav-link-custom:hover {
                background-color: rgba(255, 255, 255, 0.1);
                transform: translateY(-2px);
            }
            .nav-link-custom.active {
                background-color: rgba(255, 255, 255, 0.2);
                font-weight: bold;
            }
            .page-content {
                min-height: calc(100vh - 200px);
                padding: 20px;
            }
            .footer {
                margin-top: auto;
                padding: 20px 0;
                background-color: #f8f9fa;
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

app.layout = html.Div(
    [
        navbar,
        dbc.Container(
            [
                html.Div(dash.page_container, className="page-content"),
                html.Footer(
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
                ),
            ],
            fluid=True,
            className="px-4",
        ),
    ]
)


@app.callback(
    dash.Output("navbar-collapse", "is_open"),
    [dash.Input("navbar-toggler", "n_clicks")],
    [dash.State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run(debug=False)
