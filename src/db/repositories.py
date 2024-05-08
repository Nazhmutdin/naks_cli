import typing as t
from sqlalchemy import (
    Select, 
    Insert,
    Row,
    Update,
    Delete,
    Column, 
    select, 
    and_, 
    or_, 
    any_,
    inspect, 
    delete, 
    insert, 
    update, 
    desc, 
    func
)
from sqlalchemy.exc import IntegrityError
from abc import ABC
from sqlalchemy.orm import Session, InstrumentedAttribute
from re import fullmatch

from shemas import BaseShema, WelderShema, WelderCertificationShema, NDTShema
from db.models import WelderCertificationModel, WelderModel, NDTModel, Base
from errors import DBException
from _types import *


__all__: list[str] = [
    "BaseRepository",
    "WelderRepository",
    "WelderCertificationRepository",
    "NDTRepository"
]


"""
====================================================================================================
Base repository
====================================================================================================
"""


class BaseRepository(ABC):
    __model__: type[Base]


    def __init__(self, session: Session) -> None:
        self._session = session


    def get(self, ident: str) -> Row | None:
        try:
            stmt = self._dump_get_stmt(ident)
            response = self._session.execute(stmt)
            result = response.one_or_none()

            return result

        except IntegrityError as e:
            raise DBException(e.args[0])


    def add(self, *data: dict[str, t.Any]) -> None:
        try:
            stmt = self._dump_add_stmt(data)
            self._session.execute(stmt)
        except IntegrityError as e:
            raise DBException(e.args[0])


    def update(self, ident: str, data: dict[str, t.Any]) -> None:
        try:
            stmt = self._dump_update_stmt(ident, data)
            self._session.execute(stmt)
        except IntegrityError as e:
            raise DBException(e.args[0])


    def delete(self, ident: str) -> None:
        try:
            stmt = self._dump_delete_stmt(ident)
            self._session.execute(stmt)
        except IntegrityError as e:
            raise DBException(e.args[0])


    def count(self, stmt: Select | None = None) -> int:
        if stmt:
            stmt.select(func.count()).select_from(self.__model__)

            return (self._session.execute(stmt)).scalar_one()

        else:
            return (self._session.execute(select(func.count()).select_from(self.__model__))).scalar_one()

    
    def _get_column(self, ident: str) -> Column:
        return inspect(self.__model__).primary_key[0]
    

    def _dump_add_stmt(self, data: tuple[dict[str, t.Any]]) -> Insert:
        return insert(self.__model__).values(
            list(data)
        )
    

    def _dump_get_stmt(self, ident: str) -> Select:
        return select(self.__model__).where(
            self._get_column(ident) == ident
        )
    

    def _dump_update_stmt(self, ident: str, data: dict[str, t.Any]) -> Update:
        return update(self.__model__).where(
            self._get_column(ident) == ident
        ).values(
            **data
        )


    def _dump_delete_stmt(self, ident: str) -> Delete:
        return delete(self.__model__).where(
            self._get_column(ident) == ident
        )


"""
====================================================================================================
Welder repository
====================================================================================================
"""


class WelderRepository(BaseRepository):
    __model__ = WelderModel
    

    def _get_column(self, ident: str) -> InstrumentedAttribute:

        if fullmatch(r"[A-Z0-9]{4}", ident):
            return WelderModel.kleymo
        else:
            return WelderModel.ident


"""
====================================================================================================
Welder certification repository
====================================================================================================
"""


class WelderCertificationRepository(BaseRepository):
    __model__ = WelderCertificationModel


"""
===================================================================================================
NDT repository
====================================================================================================
"""


class NDTRepository(BaseRepository):
    __model__ = NDTModel
