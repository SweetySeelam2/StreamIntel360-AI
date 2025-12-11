import logging
from typing import Optional


def setup_logging(level: int = logging.INFO) -> None:
    """
    Basic logging configuration for backend.
    Call this once in main.py at startup.
    """
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Return a logger with the given name.
    """
    return logging.getLogger(name or __name__)