from loguru import logger
import sys
from config.settings import Settings

def configure_logger():
    logger.remove()
    logger.add(
        sys.stdout,
        level=Settings().LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    return logger

log = configure_logger()