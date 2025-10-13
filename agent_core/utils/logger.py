# agent_core/utils/logger.py
import logging
import sys
from agent_core.config.settings import settings


def setup_logger():
    """Configure a global application logger."""
    logger = logging.getLogger("agent_core")
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Avoid duplicate handlers during re-import
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(log_level)

    return logger


# Single shared instance
log = setup_logger()
