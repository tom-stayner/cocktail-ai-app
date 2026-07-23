from src.logging_config import logger


def test_application_logger_is_named():
    assert logger.name == "cocktail_api"
