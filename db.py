from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dbal.data_store import create_ds, DataStore

SQLALCHEMY_DATABASE_URL = "sqlite:///./todolist.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_ds() -> DataStore:
    db = SessionLocal()
    try:
        yield create_ds(db)
    finally:
        db.close()
