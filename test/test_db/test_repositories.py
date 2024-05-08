import pytest
import typing as t
from uuid import UUID
from datetime import date

from pydantic import ValidationError

from utils.funcs import to_date
from utils.UoWs import UnitOfWork
from errors import DBException
from db.repositories import *
from shemas import *


"""
===================================================================================================================
Welder repository
===================================================================================================================
"""


@pytest.mark.usefixtures("prepare_db")
class BaseTestRepository[Shema: BaseShema]:
    __shema__: type[Shema]
    __repository__: type[BaseRepository]


    def test_add(self, data: list[Shema]) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:
            insert_data = [
                el.model_dump() for el in data
            ]
            uow.repository.add(*insert_data)

            for el in data:
                result = self.__shema__.model_validate(uow.repository.get(el.ident.hex)[0], from_attributes=True)
                assert result == el

            assert uow.repository.count() == len(data)

            uow.commit()

    
    def test_get(self, ident: str, el: Shema) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:
            result = self.__shema__.model_validate(uow.repository.get(ident)[0], from_attributes=True)

            assert result == el


    def test_add_existing(self, data: Shema) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:
            with pytest.raises(DBException):
                uow.repository.add(data.model_dump())


    def test_update(self, ident: str, data: dict[str, t.Any]) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:

            uow.repository.update(ident, data)
            result = self.__shema__.model_validate(uow.repository.get(ident)[0], from_attributes=True)

            for key, value in data.items():
                if isinstance(getattr(result, key), date):
                    assert getattr(result, key) == to_date(value, False)
                    continue

                assert getattr(result, key) == value

            uow.commit()

    
    def test_delete(self, item: Shema) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:

            uow.repository.delete(item.ident.hex)

            assert not bool(uow.repository.get(item.ident.hex))

            uow.repository.add(item.model_dump())
            uow.commit()



"""
===================================================================================================================
Welder repository
===================================================================================================================
"""


@pytest.mark.run(order=1)
class TestWelderRepository(BaseTestRepository[WelderShema]):
    __shema__ = WelderShema
    __repository__ = WelderRepository


    @pytest.mark.usefixtures('welders')
    def test_add(self, welders: list[WelderShema]) -> None:
        super().test_add(welders)


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "attr, index",
            [
                ("kleymo", 1), 
                ("ident", 7), 
                ("kleymo", 31), 
                ("ident", 80)
            ]
    )
    def test_get(self, attr: str, index: int, welders: list[WelderShema]) -> None:
        welder = welders[index]

        ident = getattr(welder, attr)

        if isinstance(ident, UUID):
            ident = ident.hex

        super().test_get(ident, welders[index])


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 63, 4, 5, 11]
    )
    def test_add_existing(self, welders: list[WelderShema], index: int) -> None:
        super().test_add_existing(welders[index])


    @pytest.mark.parametrize(
            "ident, data",
            [
                ("095898d1419641b3adf45af287aad3e7", {"name": "dsdsds", "birthday": "15.12.1995"}),
                ("dc20817ed3844660a69b5c89d7df15ac", {"passport_number": "T15563212", "sicil": "1585254"}),
                ("d00b26c65fdf4a819c5065e301dd81dd", {"nation": "RUS", "status": 1}),
            ]
    )
    def test_update(self, ident: str, data: dict) -> None:
        super().test_update(ident, data)


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete(self, welders: list[WelderShema], index: int) -> None:
        super().test_delete(welders[index])


"""
===================================================================================================================
Welder certification repository
===================================================================================================================
"""


@pytest.mark.run(order=2)
class TestWelderCertificationRepository(BaseTestRepository[WelderCertificationShema]):
    __shema__ = WelderCertificationShema
    __repository__ = WelderCertificationRepository


    @pytest.mark.usefixtures('welder_certifications')
    def test_add(self, welder_certifications: list[WelderCertificationShema]) -> None:
        super().test_add(welder_certifications)


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 3, 4, 5, 6]
    )
    def test_get(self, index: int, welder_certifications: list[WelderCertificationShema]) -> None:
        cert = welder_certifications[index]

        ident = cert.ident.hex

        super().test_get(ident, welder_certifications[index])


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 13, 63, 31, 75, 89]
    )
    def test_add_existing(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        super().test_add_existing(welder_certifications[index])


    @pytest.mark.parametrize(
            "ident, data",
            [
                ("cccba2a0ea9047c8837691a740513f6d", {"welding_materials_groups": ["dsdsds"], "certification_date": "15.12.1995"}),
                ("422786ffabd54d74867a8f34950ee0b5", {"job_title": "ппмфва", "kleymo": "11F9", "expiration_date": "1990-05-15"}),
                ("71c20a79706d4fb28f7b84e94881565c", {"insert": "В1", "company": "asasas", "expiration_date_fact": "2025-10-20"}),
                ("435a9de3ade64c38b316dd08c3c7bc7c", {"connection_type": "gggg", "outer_diameter_from": 11.65, "details_type": ["2025-10-20", "ffff"]}),
            ]
    )
    def test_update(self, ident: str, data: dict) -> None:
        super().test_update(ident, data)


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        super().test_delete(welder_certifications[index])


"""
===================================================================================================================
NDT repository
===================================================================================================================
"""


@pytest.mark.run(order=3)
class TestNDTRepository(BaseTestRepository[NDTShema]):
    __shema__ = NDTShema
    __repository__ = NDTRepository


    @pytest.mark.usefixtures('ndts')
    def test_add(self, ndts: list[NDTShema]) -> None:
        super().test_add(ndts)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index", [1, 7, 31, 80]
    )
    def test_get(self, index: int, ndts: list[NDTShema]) -> None:
        ndt = ndts[index]

        ident = ndt.ident.hex

        super().test_get(ident, ndts[index])


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 63, 4, 5, 11]
    )
    def test_add_existing(self, ndts: list[NDTShema], index: int) -> None:
        super().test_add_existing(ndts[index])

    
    @pytest.mark.parametrize(
            "ident, data",
            [
                ("97c1a8b30a764bae84be20dab742644a", {"kleymo": "11F9", "company": "adsdsad"}),
                ("0d92a1ae45f942a5bfba4d26b8a34cd7", {"subcompany": "ппмffфва", "welding_date": "1990-05-15"}),
                ("45c040e0a78e4a3994b6cc12d3ba3d81", {"total_weld_1": 0.5, "total_weld_2": 5.36}),
            ]
    )
    def test_update(self, ident: str, data: dict) -> None:
        super().test_update(ident, data)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete(self, ndts: list[NDTShema], index: int) -> None:
        super().test_delete(ndts[index])
