from app.apis.arxiv_api import get_arxiv_data
from app.services.arxiv_parser import parse_arxiv_feed


def xml_to_dic(
    search_input,
    search_field="all",
    id_list="",
    start=0,
    max_results=10,
    sortBy="submittedDate",
    sortOrder="descending",
):
    xml = get_arxiv_data(
        search_input,
        search_field,
        id_list,
        start,
        max_results,
        sortBy,
        sortOrder,
    )
    return [
        {
            "id": article.id,
            "published": article.published,
            "title": article.title,
            "summary": article.summary,
            "authors": article.authors,
            "link": article.pdf_url,
            "category": article.category,
        }
        for article in parse_arxiv_feed(xml)
    ]
