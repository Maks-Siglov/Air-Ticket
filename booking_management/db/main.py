from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from booking_management.core.settings import DB_URL


def _create_sessionmaker(db_engine: Engine) -> sessionmaker:
    return sessionmaker(bind=db_engine, expire_on_commit=False, future=True)


engine = create_engine(DB_URL)
maker = _create_sessionmaker(engine)


def get_session() -> Session:
    session = scoped_session(maker)
    return session()
