import logging
import sys

def setup_logger(name: str, level=logging.INFO):
    """
    Setup a logger with consistent formatting.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger

# Create default loggers
orchestrator_logger = setup_logger('orchestrator')
websocket_logger = setup_logger('websocket')
controller_logger = setup_logger('controller')