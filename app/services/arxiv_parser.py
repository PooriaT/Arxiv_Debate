import xml.etree.ElementTree as ET

from app.models.article import Article

ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"
NAMESPACES = {"atom": ATOM_NS, "arxiv": ARXIV_NS}


class ArxivParseError(Exception):
    pass


def parse_arxiv_feed(xml: str) -> list[Article]:
    if not xml or not xml.strip():
        raise ArxivParseError("arXiv XML feed is empty")

    try:
        root = ET.fromstring(xml)
    except ET.ParseError as exc:
        raise ArxivParseError("arXiv XML feed is malformed") from exc

    return [_parse_entry(entry) for entry in root.findall("atom:entry", NAMESPACES)]


def _parse_entry(entry: ET.Element) -> Article:
    article_id = _find_text(entry, "atom:id")
    title = _find_text(entry, "atom:title")
    summary = _find_text(entry, "atom:summary")
    authors = [
        name
        for author in entry.findall("atom:author", NAMESPACES)
        if (name := _find_text(author, "atom:name"))
    ]

    return Article(
        id=article_id,
        title=title,
        summary=summary,
        authors=authors,
        published=_find_optional_text(entry, "atom:published"),
        pdf_url=_find_pdf_url(entry),
        category=_find_primary_category(entry),
    )


def _find_text(entry: ET.Element, path: str) -> str:
    text = _find_optional_text(entry, path)
    return text or ""


def _find_optional_text(entry: ET.Element, path: str) -> str | None:
    element = entry.find(path, NAMESPACES)
    if element is None or element.text is None:
        return None

    text = element.text.strip()
    return text or None


def _find_pdf_url(entry: ET.Element) -> str | None:
    for link in entry.findall("atom:link", NAMESPACES):
        if link.attrib.get("title") == "pdf":
            return link.attrib.get("href")
    return None


def _find_primary_category(entry: ET.Element) -> str | None:
    category = entry.find("arxiv:primary_category", NAMESPACES)
    if category is None:
        return None
    return category.attrib.get("term")
