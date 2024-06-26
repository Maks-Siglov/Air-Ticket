import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


if os.getenv("ENV") != "DOCKER":
    env_path = BASE_DIR.parent.joinpath(".env.local")
    load_dotenv(env_path)

    assert os.getenv("ENV") == "LOCAL"


DB_ENGINE = "postgresql+psycopg2"
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ["DB_NAME"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]


DB_URL = (
    f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}" f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

CELERY_TASK_TRACK_STARTED = True
CELERY_ACCEPT_CONTENT = ("application/json",)
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/Kiev"

CELERY_BROKER_URL = os.environ["CELERY_BROKER_URL"]
REDBEAT_REDIS_URL = os.environ["REDBEAT_REDIS_URL"]
CELERY_RESULT_BACKEND = os.environ["CELERY_RESULT_BACKEND"]

DOMAIN_FOR_CELERY_TASKS = os.environ["DOMAIN_FOR_CELERY_TASKS"]

BOOKING_MINUTES_LIFETIME = 15

DEACTIVATE_BOOKING_MINUTE_SCHEDULE = 5
