import unittest
from unittest.mock import Mock

from app.models.article import Article
from app.services.arxiv_client import ArxivClientError
from app.services.arxiv_parser import ArxivParseError
from app.services.search_workflow import SearchWorkflow
from app.services.summarizer import SummarizationError

ARTICLE = Article(
    id="http://arxiv.org/abs/2501.00001v1",
    title="Service-layer search",
    summary="A focused refactor.",
    authors=["Ada Lovelace"],
    published="2025-01-01T00:00:00Z",
    pdf_url="http://arxiv.org/pdf/2501.00001v1",
    category="cs.SE",
)


class SearchWorkflowTest(unittest.TestCase):
    def test_search_fetches_parses_and_summarizes_articles(self):
        arxiv_client = Mock()
        arxiv_client.fetch_articles_xml.return_value = "<feed />"
        parser = Mock(return_value=[ARTICLE])
        summarizer = Mock()
        summarizer.summarize.return_value = "AI summary"

        result = SearchWorkflow(arxiv_client, parser, summarizer).search(
            "machine learning",
            5,
        )

        request = arxiv_client.fetch_articles_xml.call_args.args[0]
        self.assertEqual(request.query, "machine learning")
        self.assertEqual(request.max_results, 5)
        parser.assert_called_once_with("<feed />")
        summarizer.summarize.assert_called_once_with([ARTICLE])
        self.assertEqual(result.articles, [ARTICLE])
        self.assertEqual(result.summary, "AI summary")
        self.assertIsNone(result.error)
        self.assertIsNone(result.summary_error)

    def test_search_returns_error_when_arxiv_fetch_fails(self):
        arxiv_client = Mock()
        arxiv_client.fetch_articles_xml.side_effect = ArxivClientError("timeout")
        parser = Mock()
        summarizer = Mock()

        result = SearchWorkflow(arxiv_client, parser, summarizer).search(
            "machine learning",
            5,
        )

        self.assertEqual(result.articles, [])
        self.assertIn("Could not retrieve arXiv articles", result.error)
        self.assertIn("timeout", result.error)
        self.assertIsNone(result.summary)
        self.assertIsNone(result.summary_error)
        parser.assert_not_called()
        summarizer.summarize.assert_not_called()

    def test_search_returns_error_when_parsing_fails(self):
        arxiv_client = Mock()
        arxiv_client.fetch_articles_xml.return_value = "<bad xml"
        parser = Mock(side_effect=ArxivParseError("malformed"))
        summarizer = Mock()

        result = SearchWorkflow(arxiv_client, parser, summarizer).search(
            "machine learning",
            5,
        )

        self.assertEqual(result.articles, [])
        self.assertIn("Could not parse arXiv articles", result.error)
        self.assertIn("malformed", result.error)
        self.assertIsNone(result.summary)
        self.assertIsNone(result.summary_error)
        summarizer.summarize.assert_not_called()

    def test_search_treats_empty_arxiv_results_as_no_results(self):
        arxiv_client = Mock()
        arxiv_client.fetch_articles_xml.return_value = "<feed />"
        parser = Mock(return_value=[])
        summarizer = Mock()

        result = SearchWorkflow(arxiv_client, parser, summarizer).search(
            "very specific missing topic",
            5,
        )

        self.assertEqual(result.articles, [])
        self.assertIsNone(result.summary)
        self.assertIsNone(result.error)
        self.assertIsNone(result.summary_error)
        summarizer.summarize.assert_not_called()

    def test_search_keeps_articles_when_summarization_fails(self):
        arxiv_client = Mock()
        arxiv_client.fetch_articles_xml.return_value = "<feed />"
        parser = Mock(return_value=[ARTICLE])
        summarizer = Mock()
        summarizer.summarize.side_effect = SummarizationError("Gemini is unavailable")

        result = SearchWorkflow(arxiv_client, parser, summarizer).search(
            "machine learning",
            5,
        )

        self.assertEqual(result.articles, [ARTICLE])
        self.assertIsNone(result.summary)
        self.assertIsNone(result.error)
        self.assertEqual(
            result.summary_error,
            "AI summary unavailable: Gemini is unavailable",
        )


if __name__ == "__main__":
    unittest.main()
