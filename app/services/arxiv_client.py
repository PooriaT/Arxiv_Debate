from dataclasses import dataclass
from typing import Any

import requests


ARXIV_API_BASE_URL = "https://export.arxiv.org/api/query"
DEFAULT_TIMEOUT_SECONDS = 10
MAX_RESULTS_LIMIT = 50
SUPPORTED_SORT_ORDERS = {"ascending", "descending"}


class ArxivClientError(Exception):
    """Raised when an arXiv request cannot be built or completed."""


@dataclass(frozen=True)
class ArxivSearchRequest:
    query: str
    search_field: str = "all"
    id_list: str | None = None
    start: int = 0
    max_results: int = 10
    sort_by: str = "submittedDate"
    sort_order: str = "descending"


class ArxivClient:
    def __init__(
        self,
        base_url: str = ARXIV_API_BASE_URL,
        timeout: int | float = DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def fetch_articles_xml(self, request: ArxivSearchRequest) -> str:
        params = self._build_params(request)

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise ArxivClientError("Failed to fetch arXiv data") from exc

        if response.status_code != 200:
            raise ArxivClientError(
                f"arXiv API returned status code {response.status_code}"
            )

        return response.text

    def _build_params(self, request: ArxivSearchRequest) -> dict[str, Any]:
        self._validate_request(request)

        params: dict[str, Any] = {
            "search_query": f"{request.search_field}:{request.query.strip()}",
            "start": request.start,
            "max_results": request.max_results,
            "sortBy": request.sort_by,
            "sortOrder": request.sort_order,
        }

        if request.id_list:
            params["id_list"] = request.id_list

        return params

    def _validate_request(self, request: ArxivSearchRequest) -> None:
        if not request.query or not request.query.strip():
            raise ArxivClientError("arXiv query must not be empty")

        if not isinstance(request.start, int):
            raise ArxivClientError("arXiv start must be an integer")

        if request.start < 0:
            raise ArxivClientError("arXiv start must not be negative")

        if not isinstance(request.max_results, int):
            raise ArxivClientError("arXiv max_results must be an integer")

        if not 1 <= request.max_results <= MAX_RESULTS_LIMIT:
            raise ArxivClientError(
                f"arXiv max_results must be between 1 and {MAX_RESULTS_LIMIT}"
            )

        if request.sort_order not in SUPPORTED_SORT_ORDERS:
            supported = ", ".join(sorted(SUPPORTED_SORT_ORDERS))
            raise ArxivClientError(f"arXiv sort_order must be one of: {supported}")
