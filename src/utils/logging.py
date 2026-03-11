import structlog

def get_logger(name: str = "duckbot"):
    # Returns a structlog logger instance; attach to app/state where needed
    logger = structlog.get_logger(name)
    return logger
#TO BE REMOVED, RAILWAY ALREADY
#TELLS WHATS WRONG
