import logging

from src.config import settings

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def configure_logging() -> logging.Logger:
    """Configure console logging and return the named application logger."""

    log_level = getattr(logging, settings.log_level)

    logging.basicConfig(
        level=log_level,
        format=LOG_FORMAT,
        handlers=[logging.StreamHandler()],
    )

    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    application_logger = logging.getLogger("cocktail_api")
    application_logger.setLevel(log_level)

    return application_logger


logger = configure_logging()
