"""
I will change this entirely,
I need to catch bugs with slack itself.
Also needs to work with JSON.
"""
import structlog

def get_logger(name: str = "duckbot"):
    # Returns a structlog logger instance; attach to app/state where needed
    logger = structlog.get_logger(name)
    return logger
