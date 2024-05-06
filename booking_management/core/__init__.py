from booking_management.core.celery_config import app as celery_app


import os

from dotenv import load_dotenv

if os.getenv("ENV") != "DOCKER":
    load_dotenv(".env.local")

    assert os.getenv("ENV") == "LOCAL"

__all__ = ("celery_app",)
