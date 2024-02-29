import os

from core.settings.base import *

DEBUG = True

ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

DOMAIN = os.environ["DOMAIN"]


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.db.backends": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
}
