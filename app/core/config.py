from dataclasses import dataclass
import os
from collections.abc import Mapping

from dotenv import load_dotenv


DEFAULT_GEMINI_MODEL_NAME = "gemini-3.5-flash"
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8050
DEFAULT_DEBUG = False

load_dotenv()


class ConfigError(ValueError):
    """Raised when environment configuration cannot be parsed."""


@dataclass(frozen=True)
class AppConfig:
    gemini_api_key: str | None
    gemini_model_name: str
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT
    debug: bool = DEFAULT_DEBUG


def _parse_port(value: str | None) -> int:
    if value is None or not value.strip():
        return DEFAULT_PORT

    try:
        port = int(value)
    except ValueError as exc:
        raise ConfigError(
            f"Invalid PORT value {value!r}: expected an integer from 1 to 65535."
        ) from exc

    if not 1 <= port <= 65535:
        raise ConfigError(
            f"Invalid PORT value {value!r}: expected an integer from 1 to 65535."
        )

    return port


def _parse_debug(value: str | None) -> bool:
    if value is None or not value.strip():
        return DEFAULT_DEBUG

    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_config(environ: Mapping[str, str] | None = None) -> AppConfig:
    source = environ if environ is not None else os.environ
    model_name = source.get("GEMINI_MODEL_NAME", DEFAULT_GEMINI_MODEL_NAME).strip()
    host = source.get("HOST", DEFAULT_HOST).strip() or DEFAULT_HOST

    return AppConfig(
        gemini_api_key=source.get("GEMINI_API_KEY") or None,
        gemini_model_name=model_name or DEFAULT_GEMINI_MODEL_NAME,
        host=host,
        port=_parse_port(source.get("PORT")),
        debug=_parse_debug(source.get("DEBUG")),
    )
