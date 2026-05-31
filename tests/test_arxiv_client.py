import unittest
from unittest.mock import Mock, patch

import requests

from app.services.arxiv_client import (
    ARXIV_API_BASE_URL,
    ArxivClient,
    ArxivClientError,
    ArxivSearchRequest,
)


class ArxivClientTest(unittest.TestCase):
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
    def test_fetch_articles_xml_raises_on_request_exception(self, mock_get):
        mock_get.side_effect = requests.Timeout("timed out")

        with self.assertRaisesRegex(ArxivClientError, "Failed to fetch"):
            ArxivClient().fetch_articles_xml(
                ArxivSearchRequest(query="machine learning")
            )


if __name__ == "__main__":
    unittest.main()
