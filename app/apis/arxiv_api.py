from app.services.arxiv_client import ArxivClient, ArxivSearchRequest


def get_arxiv_data(
    search_input,
    search_field="all",
    id_list="",
    start=0,
    max_results=10,
    sortBy="submittedDate",
    sortOrder="descending",
):
    request_params = {
        "query": search_input,
        "search_field": search_field,
        "id_list": id_list or None,
        "start": start,
        "sort_by": sortBy,
        "sort_order": sortOrder,
    }

    if max_results is not None:
        request_params["max_results"] = max_results

    request = ArxivSearchRequest(**request_params)

    return ArxivClient().fetch_articles_xml(request)
