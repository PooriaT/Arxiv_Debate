from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from app.models.article import Article
from app.services.arxiv_client import ArxivClient, ArxivClientError, ArxivSearchRequest
from app.services.arxiv_parser import ArxivParseError, parse_arxiv_feed
from app.services.summarizer import (
    SummarizationError,
    Summarizer,
    get_default_summarizer,
)


class ArxivFetcher(Protocol):
    def fetch_articles_xml(self, request: ArxivSearchRequest) -> str: ...


ArticleParser = Callable[[str], list[Article]]


@dataclass(frozen=True)
class SearchWorkflowResult:
    articles: list[Article]
    summary: str | None = None
    error: str | None = None
    summary_error: str | None = None


class SearchWorkflow:
    def __init__(
        self,
        arxiv_client: ArxivFetcher,
        parser: ArticleParser,
        summarizer: Summarizer,
    ) -> None:
        self.arxiv_client = arxiv_client
        self.parser = parser
        self.summarizer = summarizer

    def search(self, query: str, max_results: int) -> SearchWorkflowResult:
        request = ArxivSearchRequest(query=query, max_results=max_results)

        try:
            arxiv_xml = self.arxiv_client.fetch_articles_xml(request)
            articles = self.parser(arxiv_xml)
        except ArxivClientError as exc:
            return SearchWorkflowResult(
                articles=[],
                error=f"Could not retrieve arXiv articles: {exc}",
            )
        except ArxivParseError as exc:
            return SearchWorkflowResult(
                articles=[],
                error=f"Could not parse arXiv articles: {exc}",
            )

        if not articles:
            return SearchWorkflowResult(articles=[])

        try:
            summary = self.summarizer.summarize(articles)
        except SummarizationError as exc:
            return SearchWorkflowResult(
                articles=articles,
                summary_error=f"AI summary unavailable: {exc}",
            )

        return SearchWorkflowResult(articles=articles, summary=summary)


def get_default_search_workflow() -> SearchWorkflow:
    return SearchWorkflow(
        arxiv_client=ArxivClient(),
        parser=parse_arxiv_feed,
        summarizer=get_default_summarizer(),
    )
