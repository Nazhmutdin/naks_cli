from uuid import UUID
import typing as t

from _types import (
    WelderDataBaseRequest, 
    WelderCertificationDataBaseRequest, 
    NDTDataBaseRequest
)
from db.repositories import BaseRepository
from utils.UoWs import UnitOfWork
from db.repositories import *
from shemas import *


__all__: list[str] = [
    "BaseDBService",
    "WelderDBService",
    "WelderCertificationDBService",
    "NDTDBService",
]


class BaseDBService[Shema: BaseShema, CreateShema: BaseShema, UpdateShema: BaseShema]:
    _uow: UnitOfWork[BaseRepository[Shema]]


    def get(self, ident: str | UUID) -> Shema | None:
        with self._uow as uow:
            return uow.repository.get(ident)


    def add(self, *data: CreateShema) -> None:
        with self._uow as uow:
            for item in data:
                uow.repository.add(item.model_dump())

            uow.commit()


    def update(self, ident: str | UUID, data: UpdateShema) -> None:
        with self._uow as uow:
            uow.repository.update(ident, data.model_dump(exclude_unset=True))
            uow.commit()


    def delete(self, *idents: str | UUID) -> None:
        with self._uow as uow:
            for ident in idents:
                uow.repository.delete(ident)

            uow.commit()

    
    def count(self) -> int:
        with self._uow as uow:
            return uow.repository.count()


class WelderDBService(BaseDBService[WelderShema, CreateWelderShema, UpdateWelderShema]):
    _uow = UnitOfWork(WelderRepository)

    
    def get_many(self, **filters: t.Unpack[WelderDataBaseRequest]) -> list[WelderShema] | None:
        with self._uow as uow:
            return uow.repository.get_many(filters)


class WelderCertificationDBService(BaseDBService[WelderCertificationShema, CreateWelderCertificationShema, UpdateWelderCertificationShema]):
    _uow = UnitOfWork(WelderCertificationRepository)

    
    def get_many(self, **filters: t.Unpack[WelderCertificationDataBaseRequest]) -> list[WelderCertificationShema] | None:
        with self._uow as uow:
            return uow.repository.get_many(filters)


class NDTDBService(BaseDBService[NDTShema, CreateNDTShema, UpdateNDTShema]):
    _uow = UnitOfWork(NDTRepository)

    
    def get_many(self, **filters: t.Unpack[NDTDataBaseRequest]) -> list[NDTShema] | None:
        with self._uow as uow:
            return uow.repository.get_many(filters)
