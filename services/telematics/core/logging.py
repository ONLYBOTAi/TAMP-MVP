import logging
import json
from datetime import datetime
from typing import Any, Dict

class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    Includes timestamp, log level, message, and extra fields.
    """
    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Add extra fields if they exist
        if hasattr(record, "extra"):
            log_data.update(record.extra)

        # Add exception info if it exists
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }

        return json.dumps(log_data)

def setup_logging():
    """
    Configure logging with JSON formatter and appropriate handlers.
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Set JSON formatter
    console_handler.setFormatter(JSONFormatter())
    
    # Add handler to logger
    logger.addHandler(console_handler)

    # Create file handler for errors
    error_handler = logging.FileHandler("error.log")
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    logger.addHandler(error_handler)

    return logger 