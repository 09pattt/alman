from alman.infrastructure.logging import get_logger
from alman.infrastructure.config import logging_config, rich_theme
from rich.console import Console
import time

__all__ = [
    'console',
    'log'
]

console = Console(theme=rich_theme)

log = get_logger(__name__, console=console, config=logging_config)