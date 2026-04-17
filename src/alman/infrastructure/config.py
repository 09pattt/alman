from dataclasses import dataclass
from rich.theme import Theme

# Load value from function later
@dataclass
class LoggingConfig:
    LOG_LEVEL: str | int = 'DEBUG'
    SHOW_PATH: bool = True
    LOG_TO_FILE: bool = True
    LOG_FILENAME: str = '/Users/napat/Project/alman/logs/alman.log'
    LOG_FILE_MAX_BYTES: int = 512*1024
    LOG_FILE_BACKUP_COUNT: int = 3
    LOG_FILE_FORMATTER: str = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'

logging_config = LoggingConfig()

# Edit rich theme here
rich_theme = Theme({
    "success": "bold green",
    "error": "bold red",
    "warning": "yellow"
})