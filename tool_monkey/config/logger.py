"""Logging configuration for tool_monkey package."""

import logging

# Create a logger for the package
logger = logging.getLogger("tool_monkey")

# Add NullHandler to prevent "No handlers could be found" warnings
# Applications using this package should configure their own handlers
logger.addHandler(logging.NullHandler())


def get_logger(name: str = "tool_monkey") -> logging.Logger:
    """
    Get a logger instance for the tool_monkey package.

    Args:
        name: Logger name, defaults to package name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def setup_default_logging(level: int = logging.INFO):
    logging.basicConfig(level=level, format='%(levelname)s: %(message)s')
    # make the others shush
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
