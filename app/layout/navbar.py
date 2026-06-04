import dash
from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand(
                    [
                        html.I(className="fas fa-book-reader me-2"),
                        "ARXIV DEBATE DASHBOARD",
                    ],
                    className="ms-2 app-navbar-brand",
                ),
                dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className=(
                                                f"fas {page.get('icon', 'fa-circle')} me-2"
                                            )
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
