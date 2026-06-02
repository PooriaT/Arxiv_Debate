import sys
import unittest
import importlib
from unittest.mock import Mock, patch

from app.core.config import AppConfig, DEFAULT_GEMINI_MODEL_NAME, get_config
import app.services.gemini_summarizer as gemini_summarizer
from app.services.gemini_summarizer import GeminiSummarizer, build_summary_prompt
from app.services.summarizer import SummarizationError


class ConfigTest(unittest.TestCase):
    def test_get_config_uses_default_gemini_model_name(self):
        config = get_config({})

        self.assertIsNone(config.gemini_api_key)
        self.assertEqual(config.gemini_model_name, DEFAULT_GEMINI_MODEL_NAME)

    def test_get_config_supports_gemini_environment_values(self):
        config = get_config(
            {
                "GEMINI_API_KEY": "test-key",
                "GEMINI_MODEL_NAME": "custom-model",
            }
        )

        self.assertEqual(config.gemini_api_key, "test-key")
        self.assertEqual(config.gemini_model_name, "custom-model")


class GeminiSummarizerTest(unittest.TestCase):
    def test_gemini_is_not_initialized_at_import_time(self):
        def guarded_import(name, *args, **kwargs):
            if name == "google.generativeai":
                raise AssertionError(
                    "Gemini should not be imported at module import time"
                )
            return original_import(name, *args, **kwargs)

        original_import = __import__

        with patch("builtins.__import__", guarded_import):
            importlib.reload(gemini_summarizer)

    def test_missing_api_key_raises_clear_error(self):
        summarizer = GeminiSummarizer(AppConfig(None, "test-model"))

        with self.assertRaises(SummarizationError) as context:
            summarizer.summarize([])

        self.assertIn("GEMINI_API_KEY", str(context.exception))

    def test_prompt_excludes_assistant_preamble_text(self):
        prompt = build_summary_prompt("paper abstracts")

        self.assertIn("paper abstracts", prompt)
        self.assertNotIn("Okay, here's a summary", prompt)
        self.assertNotIn("Don't add the first sentence", prompt)

    def test_compatibility_api_can_mock_summarizer_without_gemini(self):
        import app.apis.gemini_api as gemini_api

        mock_summarizer = Mock()
        mock_summarizer.summarize.return_value = "mock summary"

        with patch.dict(sys.modules, {"google.generativeai": None}):
            with patch.object(
                gemini_api, "get_default_summarizer", return_value=mock_summarizer
            ):
                summary = gemini_api.get_summarization(["paper"])

        self.assertEqual(summary, "mock summary")
        mock_summarizer.summarize.assert_called_once_with(["paper"])


if __name__ == "__main__":
    unittest.main()
