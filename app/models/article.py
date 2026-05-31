from dataclasses import dataclass


@dataclass(frozen=True)
class Article:
    id: str
    title: str
    summary: str
    authors: list[str]
    published: str | None
    pdf_url: str | None
    category: str | None
