import sys

from loguru import logger


logger.remove()

logger.add(
    sys.stdout,
    format=(
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level} | "
        "{name}:{function}:{line} | "
        "{message}"
    ),
    level="INFO",
    colorize=True,
)

logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="10 days",
    compression="zip",
    level="INFO",
)

__all__ = ["logger"]