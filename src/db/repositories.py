import typing as t
from sqlalchemy import (
    Select, 
    Insert,
    Row,
    Update,
    Delete,
    BinaryExpression, 
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
from uuid import UUID

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


class BaseRepository[Shema: BaseShema](ABC):
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
        

    def get_many(self, filters: dict) -> list[Shema]: ...


    def add(self, data: dict[str, t.Any]) -> None:
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

    
    def _get_column(self, ident: str | UUID) -> Column:
        return inspect(self.__model__).primary_key[0]
    

    def _dump_add_stmt(self, data: dict[str, t.Any]) -> Insert:
        return insert(self.__model__).values(
            **data
        )
    

    def _dump_get_stmt(self, ident: str | UUID) -> Select:
        return select(self.__model__).where(
            self._get_column(ident) == ident
        )
    

    def _dump_update_stmt(self, ident: str | UUID, data: dict[str, t.Any]) -> Update:
        return update(self.__model__).where(
            self._get_column(ident) == ident
        ).values(
            **data
        )


    def _dump_delete_stmt(self, ident: str | UUID) -> Delete:
        return delete(self.__model__).where(
            self._get_column(ident) == ident
        )


"""
====================================================================================================
Welder repository
====================================================================================================
"""


class WelderRepository(BaseRepository[WelderShema]):
    __shema__ = WelderShema
    __model__ = WelderModel

    
    def get_many(self, filters: WelderDataBaseRequest = {}) -> list[WelderShema] | None:
        and_expressions, or_expressions = self._get_expressions(filters)

        stmt = select(self.__model__).join(
            WelderCertificationModel
        ).filter(
            and_(
                or_(*or_expressions),
                *and_expressions
            )
        ).distinct()

        if filters.get("limit"):
            stmt = stmt.limit(filters.get("limit"))

        if filters.get("offset"):
            stmt = stmt.offset(filters.get("offset"))

        result = self._session.execute(stmt).all()

        return result
    

    def _get_column(self, ident: str | UUID) -> InstrumentedAttribute:
        if isinstance(ident, UUID):
            return WelderModel.ident
        
        try:
            ident = UUID(ident, version=4)
            return WelderModel.ident
        except:
            return WelderModel.kleymo

    
    def _get_expressions(self, filters: WelderDataBaseRequest) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
        and_expressions = []
        or_expressions = []

        if filters.get("names"):
            or_expressions.append(WelderModel.name.ilike(any_(filters.get("names"))))

        if filters.get("kleymos"):
            or_expressions.append(WelderModel.kleymo.in_(filters.get("kleymos")))

        if filters.get("idents"):
            or_expressions.append(WelderModel.ident.in_(filters.get("idents")))

        if filters.get("certification_numbers"):
            or_expressions.append(WelderCertificationModel.certification_number.in_(filters.get("certification_numbers")))

        if filters.get("methods"):
            and_expressions.append(WelderCertificationModel.method.in_(filters.get("methods")))

        if filters.get("gtds"):
            and_expressions.append(WelderCertificationModel.gtd.in_(filters.get("gtds")))

        if filters.get("certification_date_from"):
            and_expressions.append(WelderCertificationModel.certification_date > filters.get("certification_date_from"))

        if filters.get("certification_date_before"):
            and_expressions.append(WelderCertificationModel.certification_date < filters.get("certification_date_before"))

        if filters.get("expiration_date_from"):
            and_expressions.append(WelderCertificationModel.expiration_date > filters.get("expiration_date_from"))

        if filters.get("expiration_date_before"):
            and_expressions.append(WelderCertificationModel.expiration_date < filters.get("expiration_date_before"))

        if filters.get("expiration_date_fact_from"):
            and_expressions.append(WelderCertificationModel.expiration_date_fact > filters.get("expiration_date_fact_from"))

        if filters.get("expiration_date_fact_before"):
            and_expressions.append(WelderCertificationModel.expiration_date_fact < filters.get("expiration_date_fact_before"))

        return (and_expressions, or_expressions)


"""
====================================================================================================
Welder certification repository
====================================================================================================
"""


class WelderCertificationRepository(BaseRepository[WelderCertificationShema]):
    __shema__ = WelderCertificationShema
    __model__ = WelderCertificationModel


    def get_many(self, filters: WelderCertificationDataBaseRequest = {}) -> list[WelderCertificationShema] | None:
        and_expressions, or_expressions = self._get_expressions(filters)

        stmt = select(self.__model__).join(
            WelderModel
        ).filter(
            and_(
                or_(*or_expressions),
                *and_expressions
            )
        ).order_by(desc(WelderCertificationModel.certification_date))

        if filters.get("limit"):
            stmt = stmt.limit(filters.get("limit"))

        if filters.get("offset"):
            stmt = stmt.offset(filters.get("offset"))

        return [WelderCertificationShema.model_validate(welder[0], from_attributes=True) for welder in self._session.execute(stmt).all()]


    
    def _get_expressions(self, filters: WelderCertificationDataBaseRequest) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
        and_expressions = []
        or_expressions = []

        if filters.get("names"):
            or_expressions.append(WelderModel.name.ilike(any_(filters.get("names"))))

        if filters.get("kleymos"):
            or_expressions.append(WelderCertificationModel.kleymo.in_(filters.get("kleymos")))

        if filters.get("idents"):
            or_expressions.append(WelderCertificationModel.ident.in_(filters.get("idents")))

        if filters.get("certification_numbers"):
            or_expressions.append(WelderCertificationModel.certification_number.in_(filters.get("certification_numbers")))

        if filters.get("methods"):
            and_expressions.append(WelderCertificationModel.method.in_(filters.get("methods")))

        if filters.get("gtds"):
            and_expressions.append(WelderCertificationModel.gtd.in_(filters.get("gtds")))

        if filters.get("certification_date_from"):
            and_expressions.append(WelderCertificationModel.certification_date > filters.get("certification_date_from"))

        if filters.get("certification_date_before"):
            and_expressions.append(WelderCertificationModel.certification_date < filters.get("certification_date_before"))

        if filters.get("expiration_date_from"):
            and_expressions.append(WelderCertificationModel.expiration_date > filters.get("expiration_date_from"))

        if filters.get("expiration_date_before"):
            and_expressions.append(WelderCertificationModel.expiration_date < filters.get("expiration_date_before"))

        if filters.get("expiration_date_fact_from"):
            and_expressions.append(WelderCertificationModel.expiration_date_fact > filters.get("expiration_date_fact_from"))

        if filters.get("expiration_date_fact_before"):
            and_expressions.append(WelderCertificationModel.expiration_date_fact < filters.get("expiration_date_fact_before"))

        
        return (and_expressions, or_expressions)


"""
===================================================================================================
NDT repository
====================================================================================================
"""


class NDTRepository(BaseRepository[NDTShema]):
    __shema__ = NDTShema
    __model__ = NDTModel


    def get_many(self, filters: NDTDataBaseRequest = {}) -> list[NDTShema] | None:
        and_expressions, or_expressions = self._get_expressions(filters)

        stmt = select(self.__model__).join(
            WelderModel
        ).filter(
            and_(
                or_(*or_expressions),
                *and_expressions
            )
        ).order_by(desc(NDTModel.welding_date))

        if filters.get("limit"):
            stmt = stmt.limit(filters.get("limit"))

        if filters.get("offset"):
            stmt = stmt.offset(filters.get("offset"))

        return [NDTShema.model_validate(welder[0], from_attributes=True) for welder in self._session.execute(stmt).all()]

    
    def _get_expressions(self, filters: NDTDataBaseRequest) -> tuple[list[BinaryExpression], list[BinaryExpression]]:
        and_expressions = []
        or_expressions = []

        if filters.get("names"):
            or_expressions.append(WelderModel.name.ilike(any_(filters.get("names"))))

        if filters.get("kleymos"):
            or_expressions.append(NDTModel.kleymo.in_(filters.get("kleymos")))

        if filters.get("idents"):
            or_expressions.append(NDTModel.ident.in_(filters.get("idents")))

        if filters.get("comps"):
            and_expressions.append(NDTModel.company.in_(filters.get("comps")))

        if filters.get("subcomps"):
            and_expressions.append(NDTModel.subcompany.in_(filters.get("subcomps")))

        if filters.get("projects"):
            and_expressions.append(NDTModel.project.in_(filters.get("projects")))

        if filters.get("welding_date_from"):
            and_expressions.append(NDTModel.welding_date > filters.get("welding_date_from"))

        if filters.get("welding_date_before"):
            and_expressions.append(NDTModel.welding_date < filters.get("welding_date_before"))
        
        return (and_expressions, or_expressions)
