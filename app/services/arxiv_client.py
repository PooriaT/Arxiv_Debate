from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import threading
import time
from typing import Any

import requests


ARXIV_API_BASE_URL = "http://export.arxiv.org/api/query"
DEFAULT_USER_AGENT = "arxiv-debate/0.1"
DEFAULT_TIMEOUT_SECONDS = (10, 60)
DEFAULT_RATE_LIMIT_RETRY_SECONDS = 3.0
DEFAULT_MIN_REQUEST_INTERVAL_SECONDS = 3.0
DEFAULT_MAX_RETRIES = 3
MAX_RETRY_DELAY_SECONDS = 30.0
MAX_RESULTS_LIMIT = 50
RATE_LIMIT_STATUS_CODE = 429
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
    _rate_limit_lock = threading.Lock()
    _last_request_started_at = 0.0

    def __init__(
        self,
        base_url: str = ARXIV_API_BASE_URL,
        timeout: (
            int | float | tuple[int | float, int | float]
        ) = DEFAULT_TIMEOUT_SECONDS,
        max_retries: int = DEFAULT_MAX_RETRIES,
        retry_delay_seconds: int | float = DEFAULT_RATE_LIMIT_RETRY_SECONDS,
        min_request_interval_seconds: (
            int | float
        ) = DEFAULT_MIN_REQUEST_INTERVAL_SECONDS,
        sleep: Callable[[float], None] = time.sleep,
        monotonic: Callable[[], float] = time.monotonic,
        user_agent: str = DEFAULT_USER_AGENT,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max(0, int(max_retries))
        self.retry_delay_seconds = float(retry_delay_seconds)
        self.min_request_interval_seconds = float(min_request_interval_seconds)
        self.sleep = sleep
        self.monotonic = monotonic
        self.user_agent = user_agent

    def fetch_articles_xml(self, request: ArxivSearchRequest) -> str:
        params = self._build_params(request)

        for attempt in range(self.max_retries + 1):
            self._wait_for_rate_limit()
            try:
                response = requests.get(
                    self.base_url,
                    params=params,
                    timeout=self.timeout,
                    headers={"User-Agent": self.user_agent},
                )
            except requests.RequestException as exc:
                if _is_retryable_request_exception(exc) and attempt < self.max_retries:
                    self.sleep(self.retry_delay_seconds)
                    continue

                raise ArxivClientError(_format_request_exception(exc)) from exc

            if response.status_code == 200:
                return response.text

            if (
                response.status_code == RATE_LIMIT_STATUS_CODE
                and attempt < self.max_retries
            ):
                self.sleep(self._retry_delay_for(response))
                continue

            raise ArxivClientError(self._format_response_error(response))

        raise ArxivClientError("arXiv API rate limit persisted after retries")

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

    def _retry_delay_for(self, response: requests.Response) -> float:
        retry_after = _get_header(response, "Retry-After")
        if retry_after:
            parsed_delay = _parse_retry_after_seconds(retry_after)
            if parsed_delay is not None:
                return min(parsed_delay, MAX_RETRY_DELAY_SECONDS)

        return min(max(0.0, self.retry_delay_seconds), MAX_RETRY_DELAY_SECONDS)

    def _format_response_error(self, response: requests.Response) -> str:
        if response.status_code == RATE_LIMIT_STATUS_CODE:
            return (
                "arXiv is rate limiting requests. Please wait a moment and try again."
            )

        return f"arXiv API returned status code {response.status_code}"

    def _wait_for_rate_limit(self) -> None:
        with self._rate_limit_lock:
            elapsed = self.monotonic() - self.__class__._last_request_started_at
            delay = self.min_request_interval_seconds - elapsed
            if delay > 0:
                self.sleep(delay)

            self.__class__._last_request_started_at = self.monotonic()


def _get_header(response: requests.Response, header_name: str) -> str | None:
    headers = getattr(response, "headers", None) or {}
    if hasattr(headers, "get"):
        header = headers.get(header_name)
        if header:
            return str(header)

    lower_header_name = header_name.lower()
    for key, value in dict(headers).items():
        if str(key).lower() == lower_header_name and value:
            return str(value)

    return None


def _parse_retry_after_seconds(value: str) -> float | None:
    try:
        return max(0.0, float(value.strip()))
    except ValueError:
        pass

    try:
        retry_at = parsedate_to_datetime(value)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None

    if retry_at.tzinfo is None:
        retry_at = retry_at.replace(tzinfo=timezone.utc)

    return max(0.0, (retry_at - datetime.now(timezone.utc)).total_seconds())


def _format_request_exception(exc: requests.RequestException) -> str:
    if isinstance(exc, requests.ConnectTimeout):
        return "Timed out while connecting to arXiv. Please try again in a moment."

    if isinstance(exc, requests.ReadTimeout):
        return "Timed out while waiting for arXiv to respond. Please try again in a moment."

    if isinstance(exc, requests.Timeout):
        return "Timed out while contacting arXiv. Please try again in a moment."

    if isinstance(exc, requests.ConnectionError):
        return (
            "Could not connect to arXiv. Check your internet connection or try again "
            "later."
        )

    return f"Could not complete the arXiv request: {exc}"


def _is_retryable_request_exception(exc: requests.RequestException) -> bool:
    return isinstance(exc, requests.Timeout)
