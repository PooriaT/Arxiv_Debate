from app.services.arxiv_client import ArxivClient, ArxivSearchRequest


def get_arxiv_data(
    search_input,
    search_field,
    id_list,
    start,
    max_results,
    sortBy,
    sortOrder,
):
    request = ArxivSearchRequest(
        query=search_input,
        search_field=search_field,
        id_list=id_list or None,
        start=start,
        max_results=max_results,
        sort_by=sortBy,
        sort_order=sortOrder,
    )

    return ArxivClient().fetch_articles_xml(request)
