from app.core.config import AppConfig, get_config
from app.services.summarizer import SummarizationError


def build_summary_prompt(arxiv_data) -> str:
    return f"""
Below you can find a series of articles from arXiv for a specific topic.
Review the provided abstracts and give an insightful summary of the latest
developments in that field.

{arxiv_data}

Respond with only the summary.
""".strip()


class GeminiSummarizer:
    def __init__(self, config: AppConfig | None = None):
        self.config = config or get_config()
        self._model = None

    def summarize(self, arxiv_data) -> str:
        prompt = build_summary_prompt(arxiv_data)
        try:
            response = self._get_model().generate_content(prompt)
        except SummarizationError:
            raise
        except Exception as exc:
            raise SummarizationError("Gemini summarization request failed.") from exc

        return response.text

    def _get_model(self):
        if self._model is not None:
            return self._model

        if not self.config.gemini_api_key:
            raise SummarizationError(
                "Gemini summarization is not configured. Set GEMINI_API_KEY to enable AI summaries."
            )

        try:
            import google.generativeai as genai
        except ImportError as exc:
            raise SummarizationError(
                "Gemini summarization is unavailable because google-generativeai is not installed."
            ) from exc

        try:
            genai.configure(api_key=self.config.gemini_api_key)
            self._model = genai.GenerativeModel(
                model_name=self.config.gemini_model_name
            )
        except Exception as exc:
            raise SummarizationError(
                "Gemini summarization could not be initialized."
            ) from exc

        return self._model
