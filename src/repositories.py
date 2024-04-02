import typing as t
from sqlalchemy import (
    Select, 
    BinaryExpression, 
    Column, 
    select, 
    and_, 
    or_, 
    inspect, 
    delete, 
    insert, 
    update, 
    desc, 
    func
)
from sqlalchemy.exc import IntegrityError
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from re import fullmatch
from uuid import UUID

from shemas import BaseShema, WelderShema, WelderCertificationShema, NDTShema, UserShema
from models import WelderCertificationModel, WelderModel, NDTModel, UserModel, Base
from errors import DBException
from _types import *


__all__: list[str] = [
    "SQLAlchemyRepository",
    "WelderRepository",
    "WelderCertificationRepository",
    "NDTRepository",
    "UserRepository",
]


class SQLAlchemyRepository[Shema: BaseShema, Model: type[Base]](ABC):
    __tablemodel__: Model
    __shema__: Shema


    def __init__(self, session: Session) -> None:
        self._session = session


    @abstractmethod
    def get(ident: str | UUID) -> Shema | None: ...


    @abstractmethod
    def add(**kwargs) -> None: ...


    @abstractmethod
    def update(ident: str | UUID, **kwargs) -> None: ...


    @abstractmethod
    def delete(ident: str | UUID) -> None: ...


    def _get(self, ident: str | UUID, column: Column | None = None) -> Shema | None:
        col = column if column else self.pk_column
        stmt: Select = select(self.__tablemodel__).where(
            col == ident
        )

        res = self._session.execute(stmt).fetchone()

        result = self.__shema__.model_validate(
            res[0], 
            from_attributes=True
        ) if res != None else None

        return result


    def _add(self, data: dict) -> None:
        try:
            stmt = insert(self.__tablemodel__).values(**data)

            self._session.execute(stmt)

        except IntegrityError as e:
            raise DBException(e.args[0])


    def _update(self, id: str | int | UUID, data: dict, column: Column | None = None) -> None:
        try:
            col = column if column else self.pk_column
            stmt = update(self.__tablemodel__).where(
                col == id
            ).values(**data)

            self._session.execute(stmt)

        except IntegrityError as e:
            raise DBException(e.args[0])


    def _delete(self, id: str | UUID, column: Column | None = None) -> None:
        try:
            col = column if column else self.pk_column
            stmt = delete(self.__tablemodel__).where(
                col == id
            )
            
            self._session.execute(stmt)

        except IntegrityError as e:
            raise DBException(e.args[0])


    def count(self, stmt: Select | None = None) -> int:
        if stmt:
            return len(self._session.execute(stmt).all())

        else:
            return self._session.execute(select(func.count()).select_from(self.__tablemodel__)).scalar()


    @property
    def pk_column(self) -> Column:
        return inspect(self.__tablemodel__).primary_key[0]


"""
====================================================================================================
Welder repository
====================================================================================================
"""


class WelderRepository(SQLAlchemyRepository[WelderShema, WelderModel]):
    __tablemodel__ = WelderModel
    __shema__ = WelderShema


    def get(self, ident: str | UUID) -> WelderShema | None:
        if isinstance(ident, str) and not fullmatch(r"[A-Z0-9]{4}", ident):
            return self._get(UUID(ident))
        elif isinstance(ident, UUID):
            return self._get(ident)
        else:
            return self._get(ident, self.__tablemodel__.kleymo)


    def add(self, **kwargs: t.Unpack[WelderData]):
        self._add(kwargs)


    def update(self, ident: str | UUID, **kwargs: t.Unpack[WelderData]):
        if isinstance(ident, str) and not fullmatch(r"[A-Z0-9]{4}", ident):
            self._update(UUID(ident), kwargs)
        elif isinstance(ident, UUID):
            self._update(ident, kwargs)
        else:
            self._update(ident, kwargs, self.__tablemodel__.kleymo)


    def delete(self, ident: str | int):
        if isinstance(ident, str) and not fullmatch(r"[A-Z0-9]{4}", ident):
            self._delete(UUID(ident))
        elif isinstance(ident, UUID):
            self._delete(ident)
        else:
            self._delete(ident, self.__tablemodel__.kleymo)


"""
====================================================================================================
Welder certification repository
====================================================================================================
"""


class WelderCertificationRepository(SQLAlchemyRepository[WelderCertificationShema, WelderCertificationModel]):
    __tablemodel__ = WelderCertificationModel
    __shema__ = WelderCertificationShema

    def get(self, ident: str | UUID) -> WelderCertificationShema | None:
        if isinstance(ident, str):
            ident = UUID(ident)

        return self._get(ident)


    def add(self, **kwargs: t.Unpack[WelderCertificationData]):
        self._add(kwargs)


    def update(self, ident: str | UUID, **kwargs: t.Unpack[WelderCertificationData]):
        self._update(ident, kwargs)


    def delete(self, ident: str | int):
        self._delete(ident)


"""
===================================================================================================
NDT repository
====================================================================================================
"""


class NDTRepository(SQLAlchemyRepository[NDTShema, NDTModel]):
    __tablemodel__ = NDTModel
    __shema__ = NDTShema

    
    def get(self, ident: str | UUID) -> NDTShema | None:
        if isinstance(ident, str):
            ident = UUID(ident)

        return self._get(ident)

    
    def add(self, **kwargs: t.Unpack[NDTData]):
        self._add(kwargs)


    def update(self, ident: str | int, **kwargs: t.Unpack[NDTData]):
        self._update(ident, kwargs)


    def delete(self, ident: str | int):
        self._delete(ident)


"""
====================================================================================================
User repository
====================================================================================================
"""


class UserRepository(SQLAlchemyRepository[UserShema, UserModel]):
    __tablemodel__ = UserModel
    __shema__ = UserShema


    def get(self, ident: str | UUID) -> UserShema | None:
        if isinstance(ident, str):
            ident = UUID(ident)
            
        self._get(ident)


    def update(self, id: str | int, **kwargs: t.Unpack[UserData]):
        self._update(id, **kwargs)

    
    def add(self, **kwargs: t.Unpack[UserData]):
        self._add(kwargs)


    def delete(self, id: str | int):
        self._delete(id)
