import os
import concurrent_log
import logging.handlers
from logging.config import dictConfig

log_config = {
    'version': 1,  # 必须存在

    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["consoleHandler"],
        },
        "ocr": {
            "level": "DEBUG",
            "handlers": ["consoleHandler", "OcrHandler"],
            "qualname": "ocr",
            "propagate": False
        }
    },

    "handlers": {
        "consoleHandler": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "defaultFormatter",
            "stream": 'ext://sys.stdout'
        },
        "OcrHandler": {
            "class": "logging.handlers.ConcurrentTimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "defaultFormatter",
            "when": "midnight",
            "filename": os.path.join(os.path.abspath(os.getenv('LOG_PATH', './logs')), 'ocr.log'),
            "interval": 1,
            "backupCount": 30,
            "encoding": "utf-8"
        }
    },

    "formatters": {
        "defaultFormatter": {
            "format": "%(asctime)s - %(levelname)s - %(pathname)s - line %(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    }
}

logging.config.dictConfig(log_config)
logger = logging.getLogger('ocr')
