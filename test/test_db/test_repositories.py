import pytest
import typing as t
from datetime import date

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
    __create_shema__: type[BaseShema]
    __update_shema__: type[BaseShema]
    __repository__: type[BaseRepository]


    def test_add(self, data: list[Shema]) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:
            for el in data:
                uow.repository.add(self.__create_shema__.model_validate(el, from_attributes=True).model_dump())
                assert uow.repository.get(el.ident) == el

            assert uow.repository.count() == len(data)

            uow.commit()

    
    def test_get(self, attr: str, el: Shema) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:

            assert uow.repository.get(getattr(el, attr)) == el


    def test_res_type(self, ident: int | str, expectation: type[Shema]) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:
            assert type(uow.repository.get(ident)) == expectation


    def test_add_existing(self, data: Shema) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:
            with pytest.raises(DBException):
                uow.repository.add(self.__create_shema__.model_validate(data, from_attributes=True).model_dump())


    def test_update(self, ident: str, data: dict[str, t.Any]) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:

            uow.repository.update(ident, data)
            el = uow.repository.get(ident)

            for key, value in data.items():
                if isinstance(getattr(el, key), date):
                    assert getattr(el, key) == to_date(value, False)
                    continue

                assert getattr(el, key) == value

            uow.commit()

    
    def test_delete(self, item: Shema) -> None:
        with UnitOfWork(repository_type=self.__repository__) as uow:

            uow.repository.delete(item.ident)

            assert not bool(uow.repository.get(item.ident))

            uow.repository.add(self.__create_shema__.model_validate(item, from_attributes=True).model_dump())
            uow.commit()



"""
===================================================================================================================
Welder repository
===================================================================================================================
"""


@pytest.mark.run(order=1)
class TestWelderRepository(BaseTestRepository[WelderShema]):
    __create_shema__ = CreateWelderShema
    __update_shema__ = UpdateWelderShema
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
        super().test_get(attr, welders[index])


    @pytest.mark.parametrize(
            "ident, expectation",
            [
                ("1M65", WelderShema),
                ("1E41", WelderShema),
                ("1HC0", WelderShema),
            ]
    )
    def test_res_type(self, ident: int | str, expectation: type[WelderShema]) -> None:
        super().test_res_type(ident, expectation)


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
    __create_shema__ = CreateWelderCertificationShema
    __update_shema__ = UpdateWelderCertificationShema
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
        super().test_get("ident", welder_certifications[index])


    @pytest.mark.parametrize(
            "ident, expectation",
            [
                ("46a9381ae8cb4143958152bf25c30fbe", WelderCertificationShema),
                ("10c58804bc7c4bfdb24bceba51334f00", WelderCertificationShema),
                ("11d0248261db4f6ca236f194087daeca", WelderCertificationShema),
            ]
    )
    def test_res_type(self, ident: int | str, expectation: WelderCertificationShema | None) -> None:
        super().test_res_type(ident, expectation)


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
    __create_shema__ = CreateNDTShema
    __update_shema__ = UpdateNDTShema
    __repository__ = NDTRepository


    @pytest.mark.usefixtures('ndts')
    def test_add(self, ndts: list[NDTShema]) -> None:
        super().test_add(ndts)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index", [1, 7, 31, 80]
    )
    def test_get(self, index: int, ndts: list[NDTShema]) -> None:
        with UnitOfWork(repository_type=NDTRepository) as uow:
            super().test_get("ident", ndts[index])


    @pytest.mark.parametrize(
        "ident, expectation", 
            [
                ("bb380cb216fb4505aa0d78a1b6b7abc4", NDTShema),
                ("b5636169bc624eeb9a4b61c1bdb059b5", NDTShema),
                ("f0f0ba353ebf4fd39924afbccad0a24b", NDTShema),
            ]
    )
    def test_res_type(self, ident: int | str, expectation) -> None:
        super().test_res_type(ident, expectation)


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
