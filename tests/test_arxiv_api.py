import unittest
from unittest.mock import patch

from app.apis.arxiv_api import get_arxiv_data


class ArxivApiAdapterTest(unittest.TestCase):
    @patch("app.apis.arxiv_api.ArxivClient")
    def test_get_arxiv_data_uses_default_max_results_when_none(self, mock_client):
        mock_client.return_value.fetch_articles_xml.return_value = "<feed />"

        xml = get_arxiv_data(
            "machine learning",
            "all",
            "",
            0,
            None,
            "submittedDate",
            "descending",
        )

        request = mock_client.return_value.fetch_articles_xml.call_args.args[0]
        self.assertEqual(xml, "<feed />")
        self.assertEqual(request.max_results, 10)


if __name__ == "__main__":
    unittest.main()
