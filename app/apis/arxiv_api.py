import requests


def get_arxiv_data(
    search_input,
    search_field="all",
    id_list="",
    start=0,
    max_results=100,
    sortBy="submittedDate",
    sortOrder="descending",
):
    url = url_helper(
        search_input, search_field, id_list, start, max_results, sortBy, sortOrder
    )

    if not url:
        return "Request Failed"

    response = requests.get(url)

    if response.status_code != 200:
        return "Request Failed"

    return response.text


def url_helper(
    search_input, search_field, id_list, start, max_results, sortBy, sortOrder
):
    BASE_URL = "https://export.arxiv.org/api/query?"
    if not search_input:
        return None

    search_input = search_input.replace(" ", "+")
    url = BASE_URL + f"search_query={search_field}:{search_input}"

    if id_list:
        url = url + f"&id_list={id_list}"
    if start:
        url = url + f"&start={start}"
    if max_results:
        url = url + f"&max_results={max_results}"
    if sortBy:
        url = url + f"&sortBy={sortBy}"
    if sortOrder:
        url = url + f"&sortOrder={sortOrder}"

    return url
