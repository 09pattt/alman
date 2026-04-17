import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
from rich.console import Console
from alman.infrastructure.config import LoggingConfig, logging_config


def get_logger(name: str = "alman", console: Console = Console(), config: LoggingConfig = logging_config):
    logger = logging.getLogger(name)
    logger.setLevel(config.LOG_LEVEL)

    if logger.hasHandlers():
        logger.handlers.clear()

    rich_handler = RichHandler(
        console= console,
        rich_tracebacks=True,
        markup=True,
        show_path=config.SHOW_PATH
    )
    logger.addHandler(rich_handler)

    if config.LOG_TO_FILE:
        file_handler = RotatingFileHandler(
            filename=config.LOG_FILENAME,
            maxBytes=config.LOG_FILE_MAX_BYTES,
            backupCount=config.LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_formatter = logging.Formatter(
            config.LOG_FILE_FORMATTER
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger