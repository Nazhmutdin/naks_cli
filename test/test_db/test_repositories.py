import pytest
from datetime import date

from utils.funcs import str_to_datetime
from utils.UoWs import UnitOfWork
from errors import DBException
from repositories import *
from shemas import *


"""
===================================================================================================================
Welder repository
===================================================================================================================
"""


@pytest.mark.run(order=1)
class TestWelderRepository:

    @pytest.mark.usefixtures('welders')
    def test_add_welder(self, welders: list[WelderShema]) -> None:
        with UnitOfWork(repository_type=WelderRepository) as uow:
            for welder in welders:
                uow.repository.add(**welder.model_dump())
                uow.commit()
                assert uow.repository.get(welder.ident) == welder

            assert uow.repository.count() == 100


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
    def test_get_welder(self, attr: str, index: int, welders: list[WelderShema]) -> None:
        with UnitOfWork(repository_type=WelderRepository) as uow:
            welder = welders[index]

            assert uow.repository.get(getattr(welder, attr)) == welder


    @pytest.mark.parametrize(
            "id, expectation",
            [
                ("1M65", WelderShema),
                ("1E41", WelderShema),
                ("1HC0", WelderShema),
            ]
    )
    def test_res_is_welder_shema(self, id: int | str, expectation: type[WelderShema]) -> None:
        with UnitOfWork(repository_type=WelderRepository) as uow:
            assert type(uow.repository.get(id)) == expectation


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 63, 4, 5, 11]
    )
    def test_add_existing_welder(self, welders: list[WelderShema], index: int) -> None:
        with UnitOfWork(repository_type=WelderRepository) as uow:
            with pytest.raises(DBException):
                uow.repository.add(**welders[index].model_dump())


    @pytest.mark.parametrize(
            "ident, data",
            [
                ("095898d1419641b3adf45af287aad3e7", {"name": "dsdsds", "birthday": "15.12.1995"}),
                ("dc20817ed3844660a69b5c89d7df15ac", {"passport_number": "T15563212", "sicil": "1585254"}),
                ("d00b26c65fdf4a819c5065e301dd81dd", {"nation": "RUS", "status": 1}),
            ]
    )
    def test_update_welder(self, ident: str, data: dict) -> None:
        with UnitOfWork(repository_type=WelderRepository) as uow:

            uow.repository.update(ident, **data)
            welder = uow.repository.get(ident)

            for key, value in data.items():
                if isinstance(getattr(welder, key), date):
                    assert getattr(welder, key) == str_to_datetime(value, False).date()
                    continue

                assert getattr(welder, key) == value

            uow.commit()


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete_welder(self, welders: list[WelderShema], index: int) -> None:
        with UnitOfWork(repository_type=WelderRepository) as uow:
            welder = welders[index]

            uow.repository.delete(welder.ident)

            assert not bool(uow.repository.get(welder.ident))

            uow.repository.add(**welder.model_dump())
            uow.commit()


"""
===================================================================================================================
Welder certification repository
===================================================================================================================
"""


@pytest.mark.run(order=2)
class TestWelderCertificationRepository:

    @pytest.mark.usefixtures('welder_certifications')
    def test_add_welder_certification(self, welder_certifications: list[WelderCertificationShema]) -> None:
        with UnitOfWork(repository_type=WelderCertificationRepository) as uow:
            for certification in welder_certifications:
                uow.repository.add(**certification.model_dump())

                assert uow.repository.get(certification.ident) == certification

                uow.commit()
            
            assert uow.repository.count() == len(welder_certifications)


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 3, 4, 5, 6]
    )
    def test_get_welder_certification(self, index: int, welder_certifications: list[WelderCertificationShema]) -> None:
        with UnitOfWork(repository_type=WelderCertificationRepository) as uow:
            certification = welder_certifications[index]
            assert uow.repository.get(certification.ident) == certification


    @pytest.mark.parametrize(
            "id, expectation",
            [
                ("46a9381ae8cb4143958152bf25c30fbe", WelderCertificationShema),
                ("10c58804bc7c4bfdb24bceba51334f00", WelderCertificationShema),
                ("11d0248261db4f6ca236f194087daeca", WelderCertificationShema),
            ]
    )
    def test_res_is_welder_certification_shema(self, id: int | str, expectation: WelderCertificationShema | None) -> None:
        with UnitOfWork(repository_type=WelderCertificationRepository) as uow:
            assert type(uow.repository.get(id)) == expectation


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 13, 63, 31, 75, 89]
    )
    def test_add_with_existing_welder_certification(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        with UnitOfWork(repository_type=WelderCertificationRepository) as uow:
            with pytest.raises(DBException):
                uow.repository.add(**welder_certifications[index].model_dump())


    @pytest.mark.parametrize(
            "ident, data",
            [
                ("cccba2a0ea9047c8837691a740513f6d", {"welding_materials_groups": ["dsdsds"], "certification_date": "15.12.1995"}),
                ("422786ffabd54d74867a8f34950ee0b5", {"job_title": "ппмфва", "kleymo": "11F9", "expiration_date": "1990-05-15"}),
                ("71c20a79706d4fb28f7b84e94881565c", {"insert": "В1", "company": "asasas", "expiration_date_fact": "2025-10-20"}),
                ("435a9de3ade64c38b316dd08c3c7bc7c", {"connection_type": "gggg", "outer_diameter_from": 11.65, "details_type": ["2025-10-20", "ffff"]}),
            ]
    )
    def test_update_welder_certification(self, ident: str, data: dict) -> None:
        with UnitOfWork(repository_type=WelderCertificationRepository) as uow:
            uow.repository.update(ident, **data)
            certification = uow.repository.get(ident)

            for key, value in data.items():
                if isinstance(getattr(certification, key), date):
                    assert getattr(certification, key) == str_to_datetime(value, False).date()
                    continue

                assert getattr(certification, key) == value
            
            uow.commit()


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete_welder_certification(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        with UnitOfWork(repository_type=WelderCertificationRepository) as uow:
            certification = welder_certifications[index]

            uow.repository.delete(certification.ident)

            assert not bool(uow.repository.get(certification.ident))
            
            uow.commit()


"""
===================================================================================================================
NDT repository
===================================================================================================================
"""


@pytest.mark.run(order=3)
class TestNDTRepository:

    @pytest.mark.usefixtures('ndts')
    def test_add_ndt(self, ndts: list[NDTShema]) -> None:
        with UnitOfWork(repository_type=NDTRepository) as uow:
            for ndt in ndts:
                uow.repository.add(**ndt.model_dump())
                assert uow.repository.get(ndt.ident) == ndt

            assert uow.repository.count() == len(ndts)
            
            uow.commit()


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index", [1, 7, 31, 80]
    )
    def test_get_ndt(self, index: int, ndts: list[NDTShema]) -> None:
        with UnitOfWork(repository_type=NDTRepository) as uow:
            ndt = ndts[index]
            assert uow.repository.get(ndt.ident) == ndt


    @pytest.mark.parametrize(
        "ident", ["bb380cb216fb4505aa0d78a1b6b7abc4", "b5636169bc624eeb9a4b61c1bdb059b5", "f0f0ba353ebf4fd39924afbccad0a24b",]
    )
    def test_res_is_ndt_shema(self, ident: int | str) -> None:
        with UnitOfWork(repository_type=NDTRepository) as uow:
            assert isinstance(uow.repository.get(ident), NDTShema)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 63, 4, 5, 11]
    )
    def test_add_existing_ndt(self, ndts: list[NDTShema], index: int) -> None:
        with UnitOfWork(repository_type=NDTRepository) as uow:
            with pytest.raises(DBException):
                uow.repository.add(**ndts[index].model_dump())

    
    @pytest.mark.parametrize(
            "ident, data",
            [
                ("97c1a8b30a764bae84be20dab742644a", {"kleymo": "11F9", "company": "adsdsad"}),
                ("0d92a1ae45f942a5bfba4d26b8a34cd7", {"subcompany": "ппмffфва", "welding_date": "1990-05-15"}),
                ("45c040e0a78e4a3994b6cc12d3ba3d81", {"total_weld_1": 0.5, "total_weld_2": 5.36}),
            ]
    )
    def test_update_ndt(self, ident: str, data: dict) -> None:
        with UnitOfWork(repository_type=NDTRepository) as uow:
            uow.repository.update(ident, **data)
            ndt = uow.repository.get(ident)

            for key, value in data.items():
                if isinstance(getattr(ndt, key), date):
                    assert getattr(ndt, key) == str_to_datetime(value, False).date()
                    continue

                assert getattr(ndt, key) == value
            
            uow.commit()


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete_ndt(self, ndts: list[NDTShema], index: int) -> None:
        with UnitOfWork(repository_type=NDTRepository) as uow:
            ndt = ndts[index]

            uow.repository.delete(ndt.ident)

            assert not bool(uow.repository.get(ndt.ident))

            uow.repository.add(**ndt.model_dump())
            
            uow.commit()
