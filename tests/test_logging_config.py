import importlib
import logging
from types import SimpleNamespace

import pytest

from src import logging_config


@pytest.fixture
def restore_application_logger_level():
    original_level = logging_config.logger.level

    try:
        yield
    finally:
        logging_config.logger.setLevel(original_level)


def test_application_logger_is_named():
    assert logging_config.logger.name == "cocktail_api"


def test_import_creates_no_log_files(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    importlib.reload(logging_config)

    assert not (tmp_path / "logs").exists()
    assert not (tmp_path / "cocktail-api.log").exists()


def test_configuration_uses_stream_handler_without_file_handler(
    monkeypatch,
    restore_application_logger_level,
):
    configuration_calls = []
    monkeypatch.setattr(
        logging_config.logging,
        "basicConfig",
        lambda **kwargs: configuration_calls.append(kwargs),
    )

    logging_config.configure_logging()

    handlers = configuration_calls[0]["handlers"]
    assert any(isinstance(handler, logging.StreamHandler) for handler in handlers)
    assert not any(isinstance(handler, logging.FileHandler) for handler in handlers)


@pytest.mark.parametrize(
    ("level_name", "expected_level"),
    [
        ("DEBUG", logging.DEBUG),
        ("INFO", logging.INFO),
        ("ERROR", logging.ERROR),
    ],
)
def test_application_logger_uses_configured_level(
    monkeypatch,
    restore_application_logger_level,
    level_name,
    expected_level,
):
    monkeypatch.setattr(
        logging_config,
        "settings",
        SimpleNamespace(log_level=level_name),
    )
    monkeypatch.setattr(logging_config.logging, "basicConfig", lambda **kwargs: None)

    configured_logger = logging_config.configure_logging()

    assert configured_logger.level == expected_level
    assert configured_logger.getEffectiveLevel() == expected_level


def test_reloading_configuration_does_not_grow_root_handlers():
    importlib.reload(logging_config)
    handler_count = len(logging.getLogger().handlers)

    importlib.reload(logging_config)

    assert len(logging.getLogger().handlers) == handler_count
