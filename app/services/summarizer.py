from typing import Protocol


class SummarizationError(Exception):
    """Raised when summarization cannot be completed."""


class Summarizer(Protocol):
    def summarize(self, arxiv_data) -> str: ...


def get_default_summarizer() -> Summarizer:
    from app.services.gemini_summarizer import GeminiSummarizer

    return GeminiSummarizer()
