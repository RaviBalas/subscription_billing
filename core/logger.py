import os
from pathlib import Path

# Define the BASE_DIR for log file path
BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,  # Keeps Django's default logging
    "formatters": {
        "verbose": {
            "format": "{asctime} [{levelname}] {name} - {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",  # Or DEBUG, WARNING, etc.
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "django.log"),
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
