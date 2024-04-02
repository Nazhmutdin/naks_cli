import pytest
from datetime import date

from pydantic import ValidationError

from services.db_services import *
from utils.funcs import str_to_datetime
from errors import FieldValidationException
from shemas import *


class TestWelderDBService:
    service = WelderDBService()

    @pytest.mark.usefixtures('welders')
    def test_add(self, welders: list[WelderShema]) -> None:
        for welder in welders:
            self.service.add(**welder.model_dump())
            assert self.service.get(welder.ident) == welder

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

        assert self.service.get(getattr(welder, attr)) == welder

    
    @pytest.mark.parametrize(
            "ident, data",
            [
                ("095898d1419641b3adf45af287aad3e7", {"name": "dsdsds", "birthday": "15.12.1995"}),
                ("dc20817ed3844660a69b5c89d7df15ac", {"passport_number": "T15563212", "sicil": "1585254"}),
                ("d00b26c65fdf4a819c5065e301dd81dd", {"nation": "RUS", "status": 1}),
            ]
    )
    def test_update(self, ident: str, data: dict) -> None:
        self.service.update(ident, **data)
        welder = self.service.get(ident)

        for key, value in data.items():
            if isinstance(getattr(welder, key), date):
                assert getattr(welder, key) == str_to_datetime(value, False).date()
                continue

            assert getattr(welder, key) == value

    
    @pytest.mark.parametrize(
            "ident, data, exception",
            [
                ("095898d1419641b3adf45af287aad3e7", {"kleymo": "aaa"}, FieldValidationException),
                ("9c66aab293244178bb63e579b43474d4", {"name": 111}, ValidationError),
            ]
    )
    def test_fail_update(self, ident: str, data: dict, exception) -> None:
        with pytest.raises(exception):
            self.service.update(ident, **data)


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete(self, welders: list[WelderShema], index: int) -> None:
        welder = welders[index]

        self.service.delete(welder.ident)

        assert not bool(self.service.get(welder.ident))

        self.service.add(**welder.model_dump())


class TestWelderCertificationDBService:
    service = WelderCertificationDBService()

    @pytest.mark.usefixtures('welder_certifications')
    def test_add(self, welder_certifications: list[WelderCertificationShema]) -> None:
        for certification in welder_certifications:
            self.service.add(**certification.model_dump())
            assert self.service.get(certification.ident) == certification

        assert self.service.count() == 100


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [1, 7, 31, 80]
    )
    def test_get(self, index: int, welder_certifications: list[WelderCertificationShema]) -> None:
        certification = welder_certifications[index]

        assert self.service.get(certification.ident) == certification


    @pytest.mark.parametrize(
            "ident, data",
            [
                ("cccba2a0ea9047c8837691a740513f6d", {"groups_materials_for_welding": ["dsdsds"], "certification_date": "15.12.1995"}),
                ("422786ffabd54d74867a8f34950ee0b5", {"job_title": "ппмфва", "kleymo": "11F9", "expiration_date": "1990-05-15"}),
                ("71c20a79706d4fb28f7b84e94881565c", {"insert": "В1", "company": "asasas", "expiration_date_fact": "2025-10-20"}),
                ("435a9de3ade64c38b316dd08c3c7bc7c", {"connection_type": "gggg", "outer_diameter_from": 11.65, "details_type": ["2025-10-20", "ffff"]}),
            ]
    )
    def test_update(self, ident: str, data: dict) -> None:
        self.service.update(ident, **data)
        certification = self.service.get(ident)

        for key, value in data.items():
            if isinstance(getattr(certification, key), date):
                assert getattr(certification, key) == str_to_datetime(value, False).date()
                continue

            assert getattr(certification, key) == value

    
    @pytest.mark.parametrize(
            "ident, data, exception",
            [
                ("65ea5301573b4e8e8c114c4385a2a5a8", {"certification_date": "dsdsds"}, FieldValidationException),
                ("1840a50837784bf9bbf1b282c1fcfb49", {"expiration_date": "T15563212"}, FieldValidationException),
                ("06beeb64be754167a251e7f756a1d2be", {"expiration_date_fact": "RUS"}, FieldValidationException),
            ]
    )
    def test_fail_update(self, ident: str, data: dict, exception) -> None:
        with pytest.raises(exception):
            self.service.update(ident, **data)


    @pytest.mark.usefixtures('welder_certifications')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete(self, welder_certifications: list[WelderCertificationShema], index: int) -> None:
        certification = welder_certifications[index]

        self.service.delete(certification.ident)

        assert not bool(self.service.get(certification.ident))

        self.service.add(**certification.model_dump())


class TestNDTDBService:
    service = NDTDBService()

    @pytest.mark.usefixtures('ndts')
    def test_add(self, ndts: list[NDTShema]) -> None:
        for ndt in ndts:
            self.service.add(**ndt.model_dump())
            assert self.service.get(ndt.ident) == ndt

        assert self.service.count() == len(ndts)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [1, 7, 31, 80]
    )
    def test_get(self, index: int, ndts: list[NDTShema]) -> None:
        ndt = ndts[index]

        assert self.service.get(ndt.ident) == ndt


    @pytest.mark.parametrize(
            "ident, data",
            [
                ("97c1a8b30a764bae84be20dab742644a", {"kleymo": "11F9", "company": "adsdsad"}),
                ("0d92a1ae45f942a5bfba4d26b8a34cd7", {"subcompany": "ппмffфва", "welding_date": "1990-05-15"}),
                ("45c040e0a78e4a3994b6cc12d3ba3d81", {"total_weld_1": 0.5, "total_weld_2": 5.36}),
            ]
    )
    def test_update(self, ident: str, data: dict) -> None:
        self.service.update(ident, **data)
        ndt = self.service.get(ident)

        for key, value in data.items():
            if isinstance(getattr(ndt, key), date):
                assert getattr(ndt, key) == str_to_datetime(value, False).date()
                continue

            assert getattr(ndt, key) == value

    
    @pytest.mark.parametrize(
            "ident, data, exception",
            [
                ("45c040e0a78e4a3994b6cc12d3ba3d81", {"welding_date": "dsdsds"}, FieldValidationException),
            ]
    )
    def test_fail_update(self, ident: str, data: dict, exception) -> None:
        with pytest.raises(exception):
            self.service.update(ident, **data)


    @pytest.mark.usefixtures('ndts')
    @pytest.mark.parametrize(
            "index",
            [0, 34, 65, 1, 88, 90]
    )
    def test_delete(self, ndts: list[NDTShema], index: int) -> None:
        ndt = ndts[index]

        self.service.delete(ndt.ident)

        assert not bool(self.service.get(ndt.ident))

        self.service.add(**ndt.model_dump())
