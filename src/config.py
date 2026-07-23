from dataclasses import dataclass
import logging
import os

from dotenv import load_dotenv

DEFAULT_APP_NAME = "Tom's Cocktail API"
DEFAULT_APP_VERSION = "0.4.0"
DEFAULT_APP_ENV = "development"
DEFAULT_AWS_REGION = "ap-southeast-2"
DEFAULT_TABLE_NAME = "Cocktails"
DEFAULT_LOG_LEVEL = "INFO"

SUPPORTED_APP_ENVS = {"development", "test", "production"}
SUPPORTED_LOG_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}


class ConfigurationError(ValueError):
    """Raised when application configuration is invalid."""


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_version: str
    app_env: str
    aws_region: str
    table_name: str
    log_level: str


def _read_required(variable: str, default: str) -> str:
    value = os.getenv(variable, default).strip()

    if not value:
        raise ConfigurationError(f"Invalid {variable}: value must not be empty")

    return value


def _validate_app_env(value: str) -> str:
    normalised = value.lower()

    if normalised not in SUPPORTED_APP_ENVS:
        raise ConfigurationError(f"Invalid APP_ENV: {normalised}")

    return normalised


def _validate_log_level(value: str) -> str:
    normalised = value.upper()
    level = getattr(logging, normalised, None)

    if normalised not in SUPPORTED_LOG_LEVELS or not isinstance(level, int):
        raise ConfigurationError(f"Invalid LOG_LEVEL: {normalised}")

    return normalised


def load_settings() -> Settings:
    load_dotenv()

    app_name = _read_required("APP_NAME", DEFAULT_APP_NAME)
    app_version = _read_required("APP_VERSION", DEFAULT_APP_VERSION)
    app_env = _validate_app_env(_read_required("APP_ENV", DEFAULT_APP_ENV))
    aws_region = _read_required("AWS_REGION", DEFAULT_AWS_REGION)
    table_name = _read_required("TABLE_NAME", DEFAULT_TABLE_NAME)
    log_level = _validate_log_level(_read_required("LOG_LEVEL", DEFAULT_LOG_LEVEL))

    return Settings(
        app_name=app_name,
        app_version=app_version,
        app_env=app_env,
        aws_region=aws_region,
        table_name=table_name,
        log_level=log_level,
    )


settings = load_settings()
