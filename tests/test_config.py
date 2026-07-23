from dataclasses import FrozenInstanceError

import pytest

from src import config

ENVIRONMENT_VARIABLES = (
    "APP_NAME",
    "APP_VERSION",
    "APP_ENV",
    "AWS_REGION",
    "TABLE_NAME",
    "LOG_LEVEL",
)


def isolate_environment(monkeypatch) -> None:
    monkeypatch.setattr(config, "load_dotenv", lambda: None)

    for variable in ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(variable, raising=False)


def test_load_settings_uses_safe_defaults(monkeypatch):
    isolate_environment(monkeypatch)

    loaded_settings = config.load_settings()

    assert loaded_settings == config.Settings(
        app_name=config.DEFAULT_APP_NAME,
        app_version=config.DEFAULT_APP_VERSION,
        app_env=config.DEFAULT_APP_ENV,
        aws_region=config.DEFAULT_AWS_REGION,
        table_name=config.DEFAULT_TABLE_NAME,
        log_level=config.DEFAULT_LOG_LEVEL,
    )


def test_load_settings_uses_normalised_environment_overrides(monkeypatch):
    isolate_environment(monkeypatch)
    monkeypatch.setenv("APP_NAME", " Custom Cocktail API ")
    monkeypatch.setenv("APP_VERSION", " 1.2.3 ")
    monkeypatch.setenv("APP_ENV", " PRODUCTION ")
    monkeypatch.setenv("AWS_REGION", " us-east-1 ")
    monkeypatch.setenv("TABLE_NAME", " TestCocktails ")
    monkeypatch.setenv("LOG_LEVEL", " debug ")

    loaded_settings = config.load_settings()

    assert loaded_settings == config.Settings(
        app_name="Custom Cocktail API",
        app_version="1.2.3",
        app_env="production",
        aws_region="us-east-1",
        table_name="TestCocktails",
        log_level="DEBUG",
    )


@pytest.mark.parametrize("value", ["local", "staging", "production-like"])
def test_load_settings_rejects_invalid_app_env(monkeypatch, value):
    isolate_environment(monkeypatch)
    monkeypatch.setenv("APP_ENV", value)

    with pytest.raises(config.ConfigurationError, match="APP_ENV"):
        config.load_settings()


@pytest.mark.parametrize("value", ["TRACE", "VERBOSE", "10"])
def test_load_settings_rejects_invalid_log_level(monkeypatch, value):
    isolate_environment(monkeypatch)
    monkeypatch.setenv("LOG_LEVEL", value)

    with pytest.raises(config.ConfigurationError, match="LOG_LEVEL"):
        config.load_settings()


@pytest.mark.parametrize(
    "variable",
    ["APP_NAME", "APP_VERSION", "AWS_REGION", "TABLE_NAME"],
)
def test_load_settings_rejects_empty_required_values(monkeypatch, variable):
    isolate_environment(monkeypatch)
    monkeypatch.setenv(variable, "   ")

    with pytest.raises(config.ConfigurationError, match=variable):
        config.load_settings()


def test_settings_are_immutable(monkeypatch):
    isolate_environment(monkeypatch)
    loaded_settings = config.load_settings()

    with pytest.raises(FrozenInstanceError):
        loaded_settings.app_env = "production"
