# src/utils/logging.py
import structlog

def get_logger(name: str = "duckbot"):
    logger = structlog.get_logger(name)
    return logger
