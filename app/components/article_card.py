from datetime import datetime

from dash import html
import dash_bootstrap_components as dbc

from app.models.article import Article

ABSTRACT_PREVIEW_LENGTH = 650
AUTHOR_PREVIEW_LIMIT = 3


def render_article_card(article: Article):
    """Render a reusable, scannable card for a single arXiv article."""
    arxiv_url = _format_arxiv_url(article.id)
    pdf_url = _normalize_optional_text(article.pdf_url)
    paper_identifier = _format_paper_identifier(article.id)
    action = _render_action(pdf_url, arxiv_url)

    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H5(
                        article.title or "Untitled article",
                        className="card-title article-card-title mb-2",
                    ),
                    html.Div(
                        _render_metadata(article, paper_identifier),
                        className="article-card-meta text-muted d-flex flex-wrap align-items-center gap-2 mb-3",
                    ),
                    html.P(
                        _truncate_text(article.summary or "No abstract available."),
                        className="article-abstract-preview mb-3",
                    ),
                    html.Div(
                        action,
                        className="article-card-actions d-flex flex-wrap gap-2 pt-2 border-top",
                    ),
                ]
            )
        ],
        className="article-card mb-3 shadow-sm",
    )


def render_article_cards(articles: list[Article]):
    return [render_article_card(article) for article in articles]


def _render_metadata(article: Article, paper_identifier: str | None):
    metadata = [
        html.Span(
            [
                html.I(className="fas fa-users me-1"),
                _format_authors(article.authors),
            ],
            className="article-card-meta-item",
        ),
        html.Span(
            [
                html.I(className="fas fa-calendar me-1"),
                _format_published(article.published),
            ],
            className="article-card-meta-item",
        ),
    ]

    category = _format_category(article.category)
    if category:
        metadata.insert(
            1,
            dbc.Badge(
                category,
                color="secondary",
                className="article-card-category text-uppercase",
            ),
        )

    if paper_identifier:
        metadata.append(
            html.Span(
                [
                    html.I(className="fas fa-fingerprint me-1"),
                    paper_identifier,
                ],
                className="article-card-meta-item article-card-id",
            )
        )

    return metadata


def _render_action(pdf_url: str | None, arxiv_url: str | None):
    if pdf_url:
        return [
            dbc.Button(
                [html.I(className="fas fa-file-pdf me-2"), "Read PDF"],
                href=pdf_url,
                target="_blank",
                color="primary",
                size="sm",
                className="article-card-action",
            )
        ]

    if arxiv_url:
        return [
            dbc.Button(
                [html.I(className="fas fa-external-link-alt me-2"), "View on arXiv"],
                href=arxiv_url,
                target="_blank",
                color="secondary",
                outline=True,
                size="sm",
                className="article-card-action",
            )
        ]

    return [html.Span("No article link available", className="text-muted small")]


def _format_authors(authors: list[str] | None) -> str:
    cleaned_authors = [
        author.strip() for author in (authors or []) if author and author.strip()
    ]
    if not cleaned_authors:
        return "Unknown authors"

    visible_authors = cleaned_authors[:AUTHOR_PREVIEW_LIMIT]
    formatted_authors = ", ".join(visible_authors)
    remaining_count = len(cleaned_authors) - AUTHOR_PREVIEW_LIMIT
    if remaining_count > 0:
        return f"{formatted_authors}, +{remaining_count} more"

    return formatted_authors


def _format_published(published: str | None) -> str:
    if not published:
        return "Unknown date"

    normalized = published.strip()
    if not normalized:
        return "Unknown date"

    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        return normalized[:10]

    return parsed.date().isoformat()


def _format_category(category: str | None) -> str | None:
    return _normalize_optional_text(category)


def _truncate_text(text: str, max_length: int = ABSTRACT_PREVIEW_LENGTH) -> str:
    normalized = " ".join((text or "").split())
    if not normalized:
        return "No abstract available."

    if len(normalized) <= max_length:
        return normalized

    return f"{normalized[:max_length].rstrip()}…"


def _format_arxiv_url(article_id: str | None) -> str | None:
    normalized = _normalize_optional_text(article_id)
    if not normalized:
        return None

    if normalized.startswith(("http://", "https://")):
        return normalized

    return f"https://arxiv.org/abs/{normalized}"


def _format_paper_identifier(article_id: str | None) -> str | None:
    normalized = (_normalize_optional_text(article_id) or "").rstrip("/")
    if not normalized:
        return None

    identifier = normalized.rsplit("/", 1)[-1]
    if identifier.endswith(".pdf"):
        identifier = identifier[:-4]

    return identifier or None


def _normalize_optional_text(value: str | None) -> str | None:
    normalized = (value or "").strip()
    return normalized or None
