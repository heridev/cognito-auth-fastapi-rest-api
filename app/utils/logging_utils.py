import logging
import logging.handlers
import os
from typing import Optional, Any

"""Usage in any module
from utils.logging_utils import LoggerFactory

logger = LoggerFactory.get_logger(__name__)
logger.info("This is a log message")
"""

"""Usage in classes
from utils.logging_utils import with_logger

@with_logger
class MyService:
    def some_method(self):
        self.logger.info("Using logger in my service")
"""


class LoggerFactory:
    """Centralized logger configuration and instantiation"""

    _configured = False
    _default_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @classmethod
    def configure_logging(cls,
                          log_level: int = logging.INFO,
                          log_format: Optional[str] = None,
                          log_file: Optional[str] = None) -> None:
        """Configure global logging settings"""

        if cls._configured:
            return

        # set basic configuration
        logging.basicConfig(
            level=log_level,
            format=log_format or cls._default_format
        )

        # add file handler if specified
        if log_file:
            os.maredirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=10485760,  # 10MB
                backupCount=5
            )
            file_handler.setFormatter(logging.Formatter(log_format or cls._default_format))
            logging.getLogger().addHandler(file_handler)

        cls._configured = True

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get a logger with the specified name"""
        if not cls._configured:
            cls.configure_logging()

        return logging.getLogger(name)


def with_logger(cls: Any) -> Any:
    """Class decorator to add a logger to a class"""
    cls.logger = LoggerFactory.get_logger(cls.__module__)
    return cls
