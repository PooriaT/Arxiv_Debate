from dash import html
import dash_bootstrap_components as dbc


def render_initial_state():
    return _render_status_card(
        icon="fas fa-compass",
        title="Ready when you are",
        message="Enter a research topic, choose 5 to 50 results, and start a search to see an AI-assisted summary with related arXiv papers.",
        suggestions=[
            "Try a focused topic such as graph neural networks or protein folding.",
            "Use fewer results if you want a faster first search.",
        ],
        color="primary",
    )


def render_loading_state():
    return dbc.Alert(
        [
            html.Div(
                [
                    dbc.Spinner(size="sm", color="primary", spinner_class_name="me-2"),
                    html.Strong("Searching arXiv and preparing your summary..."),
                ],
                className="d-flex align-items-center",
            ),
            html.Div(
                "This can take a moment while papers are fetched and the AI summary is generated.",
                className="small mt-2 mb-0",
            ),
        ],
        color="info",
        className="mb-0",
    )


def render_no_results_state(query: str | None = None):
    message = "arXiv did not return any papers for this search."
    if query:
        message = f'arXiv did not return any papers for "{query}".'

    return _render_status_card(
        icon="fas fa-search",
        title="No matching papers found",
        message=message,
        suggestions=[
            "Try a broader topic or fewer keywords.",
            "Check spelling, remove filters, or search for a related research area.",
        ],
        color="secondary",
    )


def render_arxiv_error(message: str):
    return _render_alert(
        icon="fas fa-cloud-arrow-down",
        title="Could not reach arXiv",
        message=message,
        suggestions=[
            "Try the search again in a minute.",
            "If the problem continues, use a smaller result count or a simpler query.",
        ],
        color="warning",
    )


def render_parser_error(message: str):
    return _render_alert(
        icon="fas fa-file-circle-exclamation",
        title="Could not read the arXiv response",
        message=message,
        suggestions=[
            "Try the search again; arXiv may have returned an unusual response.",
            "If it keeps happening, try a broader query or fewer results.",
        ],
        color="warning",
    )


def render_summary_error(message: str):
    return _render_alert(
        icon="fas fa-robot",
        title="AI summary is unavailable",
        message=message,
        suggestions=[
            "You can still review the matching papers listed here.",
            "Try again later, or confirm Gemini is configured if you run this app locally.",
        ],
        color="info",
    )


def render_invalid_max_results():
    return _render_alert(
        icon="fas fa-sliders",
        title="Choose a valid result count",
        message="Max results must be a whole number between 5 and 50.",
        suggestions=[
            "Enter a value from 5 to 50 and run the search again.",
        ],
        color="warning",
    )


def render_unexpected_error():
    return _render_alert(
        icon="fas fa-triangle-exclamation",
        title="Something went wrong",
        message="The app hit an unexpected problem while preparing your results.",
        suggestions=[
            "Try the search again in a moment.",
            "If it keeps happening, simplify the query or lower the result count.",
        ],
        color="danger",
    )


def _render_status_card(
    icon: str,
    title: str,
    message: str,
    suggestions: list[str],
    color: str,
):
    return dbc.Card(
        dbc.CardBody(_status_body(icon, title, message, suggestions, color)),
        className="border-0 bg-light h-100",
    )


def _render_alert(
    icon: str,
    title: str,
    message: str,
    suggestions: list[str],
    color: str,
):
    return dbc.Alert(
        _status_body(icon, title, _clean_message(message), suggestions, color),
        color=color,
        className="mb-0",
    )


def _status_body(
    icon: str,
    title: str,
    message: str,
    suggestions: list[str],
    color: str,
) -> list:
    return [
        html.Div(
            [
                html.I(className=f"{icon} text-{color} me-2"),
                html.Strong(title),
            ],
            className="mb-2",
        ),
        html.P(message, className="mb-2"),
        html.Ul(
            [html.Li(suggestion) for suggestion in suggestions], className="mb-0 ps-3"
        ),
    ]


def _clean_message(message: str) -> str:
    cleaned = " ".join(str(message).split())
    if not cleaned:
        return "Please try again."
    if len(cleaned) > 240:
        return f"{cleaned[:237]}..."
    return cleaned
