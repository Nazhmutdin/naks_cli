from uuid import UUID
import typing as t

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
    __shema__: type[Shema]
    __create_shema__: type[CreateShema]
    __update_shema__: type[UpdateShema]
    _uow: UnitOfWork[BaseRepository]


    def get(self, ident: str | UUID) -> Shema | None:
        with self._uow as uow:
            if isinstance(ident, UUID):
                ident = ident.hex

            result = uow.repository.get(ident)

            if not result:
                return None

            return self.__shema__.model_validate(result[0], from_attributes=True)


    def add(self, *data: dict[str, t.Any]) -> None:
        with self._uow as uow:
            uow.repository.add(
                *[
                    self.__create_shema__.model_validate(item, from_attributes=True).model_dump() for item in data
                ]
            )

            uow.commit()


    def update(self, ident: str | UUID, data: dict[str, t.Any]) -> None:
        with self._uow as uow:
            uow.repository.update(
                ident, 
                self.__update_shema__.model_validate(data).model_dump(exclude_unset=True)
            )

            uow.commit()


    def delete(self, *idents: str | UUID) -> None:
        with self._uow as uow:
            for ident in idents:

                if isinstance(ident, UUID):
                    ident = ident.hex
                    
                uow.repository.delete(ident)

            uow.commit()

    
    def count(self) -> int:
        with self._uow as uow:
            return uow.repository.count()


class WelderDBService(BaseDBService[WelderShema, CreateWelderShema, UpdateWelderShema]):
    _uow = UnitOfWork(WelderRepository)
    __create_shema__ = CreateWelderShema
    __update_shema__ = UpdateWelderShema
    __shema__ = WelderShema


class WelderCertificationDBService(BaseDBService[WelderCertificationShema, CreateWelderCertificationShema, UpdateWelderCertificationShema]):
    _uow = UnitOfWork(WelderCertificationRepository)
    __create_shema__ = CreateWelderCertificationShema
    __update_shema__ = UpdateWelderCertificationShema
    __shema__ = WelderCertificationShema


class NDTDBService(BaseDBService[NDTShema, CreateNDTShema, UpdateNDTShema]):
    _uow = UnitOfWork(NDTRepository)
    __create_shema__ = CreateNDTShema
    __update_shema__ = UpdateNDTShema
    __shema__ = NDTShema
