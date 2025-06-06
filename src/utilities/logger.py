import logging
import os
from datetime import datetime
from typing import Optional
import sys
from config import PATHS

class CustomFormatter(logging.Formatter):
    """
    Custom formatter with colors for different log levels
    """
    
    # Color codes
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    # Format string
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format_str + reset,
        logging.INFO: blue + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

class LogManager:
    """
    Centralized logging management
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """
        Initialize the logger with file and console handlers
        """
        # Create logs directory if it doesn't exist
        os.makedirs(PATHS["LOGS"], exist_ok=True)

        # Create root logger
        self.logger = logging.getLogger('PooterCooter')
        self.logger.setLevel(logging.DEBUG)

        # Remove any existing handlers
        self.logger.handlers = []

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(CustomFormatter())
        self.logger.addHandler(console_handler)

        # Create file handler
        current_date = datetime.now().strftime('%Y-%m-%d')
        file_handler = logging.FileHandler(
            os.path.join(PATHS["LOGS"], f'pootercooter_{current_date}.log')
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """
        Get a logger instance with the specified name
        """
        if name:
            return self.logger.getChild(name)
        return self.logger

    def rotate_logs(self, max_days: int = 7):
        """
        Remove log files older than max_days
        """
        try:
            current_time = datetime.now().timestamp()
            log_dir = PATHS["LOGS"]
            
            for filename in os.listdir(log_dir):
                if filename.endswith('.log'):
                    filepath = os.path.join(log_dir, filename)
                    file_time = os.path.getctime(filepath)
                    
                    # Remove if older than max_days
                    if (current_time - file_time) > (max_days * 86400):
                        try:
                            os.remove(filepath)
                            self.logger.info(f"Removed old log file: {filename}")
                        except Exception as e:
                            self.logger.error(f"Error removing log file {filename}: {str(e)}")
                            
        except Exception as e:
            self.logger.error(f"Error rotating logs: {str(e)}")

# Create error tracking methods
def log_error(logger: logging.Logger, error: Exception, context: str = ""):
    """
    Log an error with full traceback and context
    """
    import traceback
    error_message = f"{context} - {str(error)}\n{traceback.format_exc()}"
    logger.error(error_message)

def log_warning(logger: logging.Logger, message: str, context: str = ""):
    """
    Log a warning with context
    """
    warning_message = f"{context} - {message}"
    logger.warning(warning_message)

# Example usage:
# logger = LogManager().get_logger('ComponentName')
# try:
#     # Some code that might raise an exception
#     raise ValueError("Something went wrong")
# except Exception as e:
#     log_error(logger, e, "Failed during operation X")
