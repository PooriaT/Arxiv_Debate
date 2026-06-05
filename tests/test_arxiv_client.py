import unittest
from unittest.mock import Mock, patch

import requests

from app.services.arxiv_client import (
    ARXIV_API_BASE_URL,
    DEFAULT_USER_AGENT,
    ArxivClient,
    ArxivClientError,
    ArxivSearchRequest,
)


class ArxivClientTest(unittest.TestCase):
    def setUp(self):
        ArxivClient._last_request_started_at = 0.0

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_builds_query_params(self, mock_get):
        mock_get.return_value = Mock(status_code=200, text="<feed />")

        client = ArxivClient(timeout=5)
        xml = client.fetch_articles_xml(
            ArxivSearchRequest(
                query="quantum computing",
                search_field="ti",
                id_list="1234.5678",
                start=2,
                max_results=25,
                sort_by="lastUpdatedDate",
                sort_order="ascending",
            )
        )

        self.assertEqual(xml, "<feed />")
        mock_get.assert_called_once_with(
            ARXIV_API_BASE_URL,
            params={
                "search_query": "ti:quantum computing",
                "id_list": "1234.5678",
                "start": 2,
                "max_results": 25,
                "sortBy": "lastUpdatedDate",
                "sortOrder": "ascending",
            },
            timeout=5,
            headers={"User-Agent": DEFAULT_USER_AGENT},
        )

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_leaves_spaces_and_special_characters_to_params(
        self,
        mock_get,
    ):
        mock_get.return_value = Mock(status_code=200, text="<feed />")

        ArxivClient().fetch_articles_xml(
            ArxivSearchRequest(query="graph neural networks & transformers")
        )

        params = mock_get.call_args.kwargs["params"]
        self.assertEqual(
            params["search_query"],
            "all:graph neural networks & transformers",
        )

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_rejects_missing_query(self, mock_get):
        client = ArxivClient()

        with self.assertRaisesRegex(ArxivClientError, "query must not be empty"):
            client.fetch_articles_xml(ArxivSearchRequest(query=" "))

        mock_get.assert_not_called()

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_rejects_invalid_max_results(self, mock_get):
        client = ArxivClient()

        with self.assertRaisesRegex(ArxivClientError, "max_results"):
            client.fetch_articles_xml(
                ArxivSearchRequest(query="machine learning", max_results=51)
            )

        mock_get.assert_not_called()

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_rejects_negative_start(self, mock_get):
        client = ArxivClient()

        with self.assertRaisesRegex(ArxivClientError, "start must not be negative"):
            client.fetch_articles_xml(
                ArxivSearchRequest(query="machine learning", start=-1)
            )

        mock_get.assert_not_called()

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_rejects_invalid_sort_order(self, mock_get):
        client = ArxivClient()

        with self.assertRaisesRegex(ArxivClientError, "sort_order"):
            client.fetch_articles_xml(
                ArxivSearchRequest(query="machine learning", sort_order="newest")
            )

        mock_get.assert_not_called()

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_raises_on_non_200_response(self, mock_get):
        mock_get.return_value = Mock(status_code=503, text="unavailable")

        with self.assertRaisesRegex(ArxivClientError, "status code 503"):
            ArxivClient().fetch_articles_xml(
                ArxivSearchRequest(query="machine learning")
            )

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_retries_rate_limited_response(self, mock_get):
        sleep = Mock()
        mock_get.side_effect = [
            Mock(status_code=429, text="too many", headers={}),
            Mock(status_code=200, text="<feed />", headers={}),
        ]

        xml = ArxivClient(
            max_retries=1,
            retry_delay_seconds=3,
            min_request_interval_seconds=0,
            sleep=sleep,
        ).fetch_articles_xml(ArxivSearchRequest(query="machine learning"))

        self.assertEqual(xml, "<feed />")
        self.assertEqual(mock_get.call_count, 2)
        sleep.assert_called_once_with(3)

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_uses_retry_after_header(self, mock_get):
        sleep = Mock()
        mock_get.side_effect = [
            Mock(status_code=429, text="too many", headers={"Retry-After": "7"}),
            Mock(status_code=200, text="<feed />", headers={}),
        ]

        ArxivClient(
            max_retries=1,
            min_request_interval_seconds=0,
            sleep=sleep,
        ).fetch_articles_xml(ArxivSearchRequest(query="machine learning"))

        sleep.assert_called_once_with(7.0)

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_raises_friendly_rate_limit_error_after_retries(
        self,
        mock_get,
    ):
        mock_get.return_value = Mock(status_code=429, text="too many", headers={})

        with self.assertRaisesRegex(ArxivClientError, "rate limiting"):
            ArxivClient(
                max_retries=1,
                min_request_interval_seconds=0,
                sleep=Mock(),
            ).fetch_articles_xml(ArxivSearchRequest(query="machine learning"))

        self.assertEqual(mock_get.call_count, 2)

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_raises_on_request_exception(self, mock_get):
        mock_get.side_effect = requests.Timeout("timed out")

        with self.assertRaisesRegex(ArxivClientError, "Timed out"):
            ArxivClient(max_retries=0).fetch_articles_xml(
                ArxivSearchRequest(query="machine learning")
            )

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_raises_clear_connection_error(self, mock_get):
        mock_get.side_effect = requests.ConnectionError("dns failed")

        with self.assertRaisesRegex(ArxivClientError, "Could not connect to arXiv"):
            ArxivClient().fetch_articles_xml(
                ArxivSearchRequest(query="machine learning")
            )

    @patch("app.services.arxiv_client.requests.get")
    def test_fetch_articles_xml_throttles_successive_clients(self, mock_get):
        sleep = Mock()
        mock_get.return_value = Mock(status_code=200, text="<feed />")
        ArxivClient._last_request_started_at = 10.0

        ArxivClient(
            min_request_interval_seconds=3,
            sleep=sleep,
            monotonic=Mock(return_value=11.0),
        ).fetch_articles_xml(ArxivSearchRequest(query="machine learning"))

        sleep.assert_called_once_with(2.0)


if __name__ == "__main__":
    unittest.main()
