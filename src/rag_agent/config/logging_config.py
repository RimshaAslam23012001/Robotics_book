import logging
from .settings import settings


def setup_logging():
    """
    Configure logging for the application with minimal debug logging
    """
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.getLevelName(settings.log_level))

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.getLevelName(settings.log_level))

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)

    # Add handler to root logger
    root_logger.addHandler(console_handler)

    # Set minimal logging level as specified in requirements
    if not settings.debug:
        # Only log warnings and above unless debug is enabled
        logging.getLogger().setLevel(logging.WARNING)

    return root_logger


# Set up logging when module is imported
logger = setup_logging()