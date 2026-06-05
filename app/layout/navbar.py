import dash
from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    return dbc.Navbar(
        dbc.Container(
            [
                dbc.NavbarBrand(
                    [
                        html.I(
                            className="fas fa-book-reader me-2",
                            **{"aria-hidden": "true"},
                        ),
                        "ARXIV DEBATE DASHBOARD",
                    ],
                    className="ms-2 app-navbar-brand",
                ),
                dbc.NavbarToggler(
                    id="navbar-toggler",
                    n_clicks=0,
                    **{"aria-label": "Toggle navigation menu"},
                ),
                dbc.Collapse(
                    dbc.Nav(
                        [
                            dbc.NavItem(
                                dbc.NavLink(
                                    [
                                        html.I(
                                            className=f"{_normalize_icon_class(page.get('icon'))} me-2",
                                            **{"aria-hidden": "true"},
                                        ),
                                        f"{page['name']}",
                                    ],
                                    href=page["relative_path"],
                                    active="exact",
                                    className="nav-link-custom d-flex align-items-center",
                                )
                            )
                            for page in dash.page_registry.values()
                        ],
                        className="ms-auto navbar-links",
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


def _normalize_icon_class(icon: str | None) -> str:
    normalized_icon = (icon or "fa-circle").strip()
    if normalized_icon.startswith(("fa ", "fas ", "far ", "fab ")):
        return normalized_icon

    return f"fas {normalized_icon}"
