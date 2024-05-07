import pytest
from uuid import UUID
from datetime import date

from pydantic import ValidationError

from services.db_services import *
from utils.funcs import str_to_datetime
from errors import FieldValidationException
from shemas import *


@pytest.mark.usefixtures("prepare_db")
class BaseTestDBService[Shema: BaseShema]:
    service: BaseDBService[Shema, Shema, Shema]
    __create_shema__: type[BaseShema]
    __update_shema__: type[BaseShema]


    def test_add(self, item: Shema) -> None:
        self.service.add(self.__create_shema__.model_validate(item, from_attributes=True))
        assert self.service.get(item.ident) == item


    def test_get(self, ident: str, item: Shema) -> None:

        assert self.service.get(ident) == item


    def test_update(self, ident: str, data: dict) -> None:

        assert self.service.get(ident)

        self.service.update(ident, self.__update_shema__.model_validate(data, from_attributes=True))
        item = self.service.get(ident)

        for key, value in data.items():
            if isinstance(getattr(item, key), date):
                assert getattr(item, key) == str_to_datetime(value, False).date()
                continue

            assert getattr(item, key) == value

    
    def test_fail_update(self, ident: str, data: dict, exception) -> None:
        with pytest.raises(exception):
            self.service.update(ident, self.__update_shema__.model_validate(data, from_attributes=True))


    def test_delete(self, item: Shema) -> None:

        self.service.delete(item.ident)

        assert not bool(self.service.get(item.ident))

        self.service.add(self.__create_shema__.model_validate(item, from_attributes=True))


class TestWelderDBService(BaseTestDBService[WelderShema]):
    service = WelderDBService()
    __create_shema__ = CreateWelderShema
    __update_shema__ = UpdateWelderShema


    @pytest.mark.usefixtures('welders')
    def test_add(self, welders: list[WelderShema]) -> None:
        for welder in welders:
            super().test_add(welder)

        assert self.service.count() == 100


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

        super().test_get(ident, welders[index])

    
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

    
    @pytest.mark.parametrize(
            "ident, data, exception",
            [
                ("095898d1419641b3adf45af287aad3e7", {"kleymo": "aaa"}, FieldValidationException),
                ("9c66aab293244178bb63e579b43474d4", {"name": 111}, ValidationError),
            ]
    )
    def test_fail_update(self, ident: str, data: dict, exception) -> None:
        super().test_fail_update(ident, data, exception)


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete(self, welders: list[WelderShema], index: int) -> None:
        super().test_delete(welders[index])


class TestWelderCertificationDBService(BaseTestDBService[WelderCertificationShema]):
    service = WelderCertificationDBService()
    __create_shema__ = CreateWelderCertificationShema
    __update_shema__ = UpdateWelderCertificationShema


    @pytest.mark.usefixtures('welder_certifications')
    def test_add(self, welder_certifications: list[WelderCertificationShema]) -> None:
        for certification in welder_certifications:
            super().test_add(certification)

        assert self.service.count() == len(welder_certifications)


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 7, 31, 80]
    )
    def test_get(self, index: int, welder_certifications: list[WelderCertificationShema]) -> None:
        cert = welder_certifications[index]

        ident = cert.ident

        super().test_get(ident, welder_certifications[index])


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
    

    @pytest.mark.parametrize(
            "ident, data, exception",
            [
                ("65ea5301573b4e8e8c114c4385a2a5a8", {"certification_date": "dsdsds"}, FieldValidationException),
                ("1840a50837784bf9bbf1b282c1fcfb49", {"expiration_date": "T15563212"}, FieldValidationException),
                ("06beeb64be754167a251e7f756a1d2be", {"expiration_date_fact": "RUS"}, FieldValidationException),
            ]
    )
    def test_fail_update(self, ident: str, data: dict, exception) -> None:
        super().test_fail_update(ident, data, exception)


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        super().test_delete(welder_certifications[index])


class TestNDTDBService(BaseTestDBService[NDTShema]):
    service = NDTDBService()
    __create_shema__ = CreateNDTShema
    __update_shema__ = UpdateNDTShema


    @pytest.mark.usefixtures('ndts')
    def test_add(self, ndts: list[NDTShema]) -> None:
        for ndt in ndts:
            super().test_add(ndt)

        assert self.service.count() == len(ndts)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [1, 7, 31, 80]
    )
    def test_get(self, index: int, ndts: list[NDTShema]) -> None:
        ndt = ndts[index]

        ident = ndt.ident
        
        super().test_get(ident, ndts[index])


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

    
    @pytest.mark.parametrize(
            "ident, data, exception",
            [
                ("45c040e0a78e4a3994b6cc12d3ba3d81", {"welding_date": "dsdsds"}, FieldValidationException),
            ]
    )
    def test_fail_update(self, ident: str, data: dict, exception) -> None:
        super().test_fail_update(ident, data, exception)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete(self, ndts: list[NDTShema], index: int) -> None:
        super().test_delete(ndts[index])
