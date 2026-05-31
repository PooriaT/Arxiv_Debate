from dataclasses import dataclass
import os
from collections.abc import Mapping

from dotenv import load_dotenv


DEFAULT_GEMINI_MODEL_NAME = "gemini-3.5-flash"

load_dotenv()


@dataclass(frozen=True)
class AppConfig:
    gemini_api_key: str | None
    gemini_model_name: str


def get_config(environ: Mapping[str, str] | None = None) -> AppConfig:
    source = environ if environ is not None else os.environ
    model_name = source.get("GEMINI_MODEL_NAME", DEFAULT_GEMINI_MODEL_NAME).strip()

    return AppConfig(
        gemini_api_key=source.get("GEMINI_API_KEY") or None,
        gemini_model_name=model_name or DEFAULT_GEMINI_MODEL_NAME,
    )
