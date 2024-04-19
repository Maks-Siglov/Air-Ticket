from sqlalchemy import create_engine, Engine, select
from sqlalchemy.orm import sessionmaker, Session

from booking_management.settings import DB_URL


class SessionExcept(Exception):
    pass


def get_session() -> Session:
    engine = create_engine(DB_URL)
    _check_connection(engine)
    maker = _create_sessionmaker(engine)
    return maker()


def _check_connection(db_engine: Engine) -> None:
    try:
        with db_engine.connect() as conn:
            conn.execute(select(1))
    except Exception as e:
        raise SessionExcept(e)


def _create_sessionmaker(db_engine: Engine) -> sessionmaker:
    return sessionmaker(bind=db_engine, expire_on_commit=False, future=True)
