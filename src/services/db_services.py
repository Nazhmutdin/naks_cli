from uuid import UUID
import typing as t

from _types import (
    WelderData, 
    WelderCertificationData, 
    NDTData, 
    DataBaseRequest,
    WelderDataBaseRequest, 
    WelderCertificationDataBaseRequest, 
    NDTDataBaseRequest
)
from repositories import SQLAlchemyRepository
from utils.UoWs import UnitOfWork
from repositories import *
from shemas import *


__all__: list[str] = [
    "BaseDBService",
    "WelderDBService",
    "WelderCertificationDBService",
    "NDTDBService",
]


class BaseDBService[Shema: BaseShema, Request: DataBaseRequest]:
    def __init__(self, repository_type: type[SQLAlchemyRepository]) -> None:
        self.uow = UnitOfWork(repository_type=repository_type)
        self.create_shema: type[BaseShema] = NotImplemented
        self.update_shema: type[BaseShema] = NotImplemented


    def get(self, ident: str | UUID) -> Shema | None:
        with self.uow as uow:
            return uow.repository.get(ident)


    def get_many(self, **filters: t.Unpack[Request]) -> list[Shema] | None:
        with self.uow as uow:
            return uow.repository.get_many(filters)


    def add(self, data: dict) -> None:
        with self.uow as uow:
            uow.repository.add(**data)
            uow.commit()


    def update(self, ident: str | UUID, data: dict) -> None:
        with self.uow as uow:
            uow.repository.update(ident, **data)
            uow.commit()


    def delete(self, ident: str | UUID) -> None:
        with self.uow as uow:
            uow.repository.delete(ident)
            uow.commit()

    
    def count(self) -> int:
        with self.uow as uow:
            return uow.repository.count()


class WelderDBService(BaseDBService[WelderShema, WelderDataBaseRequest]):
    def __init__(self) -> None:
        self.uow = UnitOfWork(WelderRepository)
        self.create_shema = CreateWelderShema
        self.update_shema = UpdateWelderShema

    
    def add(self, **data: t.Unpack[WelderData]) -> None:
        validated_data = self.create_shema.model_validate(data).model_dump()
        super().add(validated_data)
    

    def update(self, ident: str | UUID, **data: t.Unpack[WelderData]) -> None:
        validated_data = self.update_shema.model_validate(data).model_dump(exclude_unset=True)
        super().update(ident, validated_data)

    
    def get_many(self, **filters: t.Unpack[WelderDataBaseRequest]) -> list[WelderShema] | None:
        return super().get_many(**filters)


class WelderCertificationDBService(BaseDBService[WelderCertificationShema, WelderCertificationDataBaseRequest]):
    def __init__(self) -> None:
        self.uow = UnitOfWork(WelderCertificationRepository)
        self.create_shema = CreateWelderCertificationShema
        self.update_shema = UpdateWelderCertificationShema

    
    def add(self, **data: t.Unpack[WelderCertificationData]) -> None:
        validated_data = self.create_shema.model_validate(data).model_dump()
        super().add(validated_data)
    

    def update(self, ident: str | UUID, **data: t.Unpack[WelderCertificationData]) -> None:
        validated_data = self.update_shema.model_validate(data).model_dump(exclude_unset=True)
        super().update(ident, validated_data)


    def get_many(self, **filters: t.Unpack[WelderCertificationDataBaseRequest]) -> list[WelderCertificationShema] | None:
        return super().get_many(**filters)


class NDTDBService(BaseDBService[NDTShema, NDTDataBaseRequest]):
    def __init__(self) -> None:
        self.uow = UnitOfWork(NDTRepository)
        self.create_shema = CreateNDTShema
        self.update_shema = UpdateNDTShema

    
    def add(self, **data: t.Unpack[NDTData]) -> None:
        validated_data = self.create_shema.model_validate(data).model_dump()
        super().add(validated_data)
    

    def update(self, ident: str | UUID, **data: t.Unpack[NDTData]) -> None:
        validated_data = self.update_shema.model_validate(data).model_dump(exclude_unset=True)
        super().update(ident, validated_data)

    
    def get_many(self, **filters: t.Unpack[NDTDataBaseRequest]) -> list[NDTShema] | None:
        return super().get_many(**filters)
