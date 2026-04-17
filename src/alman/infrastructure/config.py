from dataclasses import dataclass

@dataclass
class LoggingConfig:
    LOG_LEVEL: str | int = 'INFO'
    SHOW_PATH: bool = True
    LOG_TO_FILE: bool = False
    LOG_FILE_PATH: str = ''
    LOG_FILE_MAX_BYTES: int = 512*1024
    LOG_FILE_BACKUP_COUNT: int = 3
    LOG_FILE_FORMATTER: str = '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'