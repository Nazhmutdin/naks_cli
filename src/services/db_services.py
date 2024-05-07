from uuid import UUID

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
    __shema__: type[Shema]


    def get(self, ident: str | UUID) -> Shema | None:
        with self._uow as uow:
            if isinstance(ident, UUID):
                ident = ident.hex

            result = uow.repository.get(ident)

            if not result:
                return None

            return self.__shema__.model_validate(result[0], from_attributes=True)


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

                if isinstance(ident, UUID):
                    ident = ident.hex
                    
                uow.repository.delete(ident)

            uow.commit()

    
    def count(self) -> int:
        with self._uow as uow:
            return uow.repository.count()


class WelderDBService(BaseDBService[WelderShema, CreateWelderShema, UpdateWelderShema]):
    _uow = UnitOfWork(WelderRepository)
    __shema__ = WelderShema


class WelderCertificationDBService(BaseDBService[WelderCertificationShema, CreateWelderCertificationShema, UpdateWelderCertificationShema]):
    _uow = UnitOfWork(WelderCertificationRepository)
    __shema__ = WelderCertificationShema


class NDTDBService(BaseDBService[NDTShema, CreateNDTShema, UpdateNDTShema]):
    _uow = UnitOfWork(NDTRepository)
    __shema__ = NDTShema
