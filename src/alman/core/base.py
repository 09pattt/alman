from alman.infrastructure.logging import get_logger
from alman.infrastructure.config import LoggingConfig
from alman.core.config import rich_theme
from rich.console import Console

__all__ = [
    'console',
    'log'
]

console = Console(theme=rich_theme)

logging_config = LoggingConfig()

log = get_logger(__name__, console=console, config=logging_config)