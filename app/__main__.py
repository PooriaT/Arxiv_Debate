import dash
from dash import Dash
import dash_bootstrap_components as dbc

from .core.config import get_config
from .layout import create_app_shell

app = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.1.1/css/all.min.css",
    ],
)

app.layout = create_app_shell()


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
    config = get_config()
    app.run(host=config.host, port=config.port, debug=config.debug)
