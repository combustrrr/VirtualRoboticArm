"""Logging helpers for the Virtual Robotic Arm project."""
from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

_LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
_DEFAULT_MAX_BYTES = 1_000_000
_DEFAULT_BACKUP_COUNT = 5


def _ensure_log_dir() -> Path:
    """Ensure the log directory exists and return its path."""
    _LOG_DIR.mkdir(parents=True, exist_ok=True)
    return _LOG_DIR


def configure_logging(application_name: str, level: int = logging.INFO) -> None:
    """Configure root logging with rotating file and console handlers."""
    log_dir = _ensure_log_dir()
    log_file = log_dir / f"{application_name}.log"

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=_DEFAULT_MAX_BYTES,
        backupCount=_DEFAULT_BACKUP_COUNT,
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    _remove_existing_handlers(root_logger)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    root_logger.debug("Logging configured for %s", application_name)


def _remove_existing_handlers(logger: logging.Logger) -> None:
    """Remove existing handlers so configuration remains idempotent."""
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a module-level logger."""
    return logging.getLogger(name if name else __name__)
