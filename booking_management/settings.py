BOOKING_MINUTES_LIFETIME = 0

DEACTIVATE_BOOKING_MINUTE_SCHEDULE = 5

CELERY_BROKER_URL = "redis://localhost:6379/0"
REDBEAT_REDIS_URL = "redis://localhost:6379/1"

DB_ENGINE = "postgresql+psycopg2"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "air_ticket"

DB_URL = (
    f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}" f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
