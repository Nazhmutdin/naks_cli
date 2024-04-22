import typing

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase
from pydantic import BaseModel

from settings import Settings


Shema = typing.TypeVar("Shema", bound=BaseModel)

DB_URL = "postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
    Settings.USER(), 
    Settings.DB_PASSWORD(), 
    Settings.HOST(), 
    Settings.PORT(), 
    Settings.DB_NAME()
)


class Base(DeclarativeBase):
    __shema__: Shema = NotImplementedError

engine = create_engine(DB_URL)

Base.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine, autoflush=False)
