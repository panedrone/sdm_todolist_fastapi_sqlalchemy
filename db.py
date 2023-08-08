from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from dbal.data_store import create_ds, DataStore

SQLALCHEMY_DATABASE_URL = "sqlite:///./todolist.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

# sqlalchemy.exc.ArgumentError: autocommit=True is no longer supported
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


# Dependency
def get_ds() -> DataStore:
    # seems like it is from here:
    #   C:\Program Files\Python39\Lib\contextlib.py
    #       --> def contextmanager(func):
    session = SessionLocal()
    try:
        yield create_ds(session)
    finally:
        session.close()
