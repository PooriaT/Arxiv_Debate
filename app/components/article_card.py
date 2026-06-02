from dash import html
import dash_bootstrap_components as dbc

from app.models.article import Article


def render_article_card(article: Article):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(
                        [
                            html.A(
                                article.title,
                                href=article.pdf_url or article.id or None,
                                target="_blank",
                                className="text-decoration-none",
                            )
                        ],
                        className="card-title",
                    ),
                    html.Div(
                        [
                            html.Span(
                                [
                                    html.I(className="fas fa-users me-2"),
                                    f"Authors: {_format_authors(article.authors)}",
                                ],
                                className="me-3",
                            ),
                            html.Span(
                                [
                                    html.I(className="fas fa-calendar me-2"),
                                    f"Published: {_format_published(article.published)}",
                                ]
                            ),
                        ],
                        className="text-muted mb-3",
                    ),
                    html.P(
                        [
                            html.I(className="fas fa-info-circle me-2"),
                            f"Summary: {article.summary or 'No summary available'}",
                        ],
                        className="mb-0",
                    ),
                ]
            )
        ],
        className="mb-3 shadow-sm",
    )


def render_article_cards(articles: list[Article]):
    return [render_article_card(article) for article in articles]


def _format_authors(authors: list[str]) -> str:
    return ", ".join(authors) if authors else "Unknown"


def _format_published(published: str | None) -> str:
    return published[:10] if published else "Unknown"
