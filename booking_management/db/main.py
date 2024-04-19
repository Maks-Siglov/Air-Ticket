from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from booking_management.settings import (
    DB_ENGINE,
    DB_NAME,
    DB_PASSWORD,
    DB_USER,
)

engine = create_engine(
    f"{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_PASSWORD}:{DB_PASSWORD}/{DB_NAME}"
)
Session = sessionmaker(bind=engine)
session = Session()
