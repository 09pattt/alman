import logging
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler
from rich.console import Console
from dataclasses import dataclass


@dataclass
class LoggingConfig:
    LOG_LEVEL: str | int = 'INFO'
    SHOW_PATH: bool = True
    LOG_TO_FILE: bool = False
    LOG_FILE_NAME: str | None = None
    LOG_FILE_MAX_BYTES: int = 524288
    LOG_FILE_BACKUP_COUNT: int = 3
    LOG_FILE_FORMATTER: str = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'


def get_logger(name: str = "almora", console: Console = Console(), config: LoggingConfig = LoggingConfig()):
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
            filename=config.LOG_FILE_NAME,
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