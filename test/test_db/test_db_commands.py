from click.testing import CliRunner
import pytest

from commands import (
    AddWelderCommand,
    UpdateWelderCommand,
    DeleteWelderCommand,
    AddWelderCertificationCommand,
    UpdateWelderCertificationCommand,
    DeleteWelderCertificationCommand,
    AddNDTCommand,
    UpdateNDTCommand,
    DeleteNDTCommand
)
from services.db_services import *
from shemas import WelderShema, WelderCertificationShema, NDTShema
from conftest import from_shema_to_cmd_arguments, from_dict_to_cmd_args


runner = CliRunner()


class TestWelderCommands:
    @pytest.mark.usefixtures('welders')
    def test_add_welder_command(self, welders: list[WelderShema]):
        service = WelderDBService()

        for welder in welders:

            args = from_shema_to_cmd_arguments(welder)
 
            ctx = AddWelderCommand().make_context(
                info_name="add-welder", 
                args=args
            )
            AddWelderCommand().invoke(ctx)

            assert service.get(welder.kleymo) == welder

        assert service.count() == len(welders)


    @pytest.mark.parametrize(
        "ident, data", 
        [
            ("01X0", {"kleymo": "01X0", "name": "ADADrf vvtt", "birthday": "1990-10-11"}),
            ("9090ae6f534141669b34e7019bbcf285", {"passport_number": "Y5562554", "sicil": "255614"}),
            ("0576", {"kleymo": "0576", "nation": "RUS", "status": 0})
        ]
    )
    def test_update_welder_command(self, ident: str,  data: dict) -> None:
        service = WelderDBService()
        welder = service.get(ident)

        assert bool(welder)

        welder.update_shema(data)

        ctx = UpdateWelderCommand().make_context(info_name="update-welder", args=[f"--ident={ident}", *from_dict_to_cmd_args(data)])
        UpdateWelderCommand().invoke(ctx)

        assert welder == service.get(welder.kleymo)


    @pytest.mark.parametrize(
            "ident", ["06PV","04LC","d0543b8fb17c4a17b32921dae2606c0e"]
    )
    def test_delete_welder_command(self, ident: str) -> None:
        service = WelderDBService()

        welder = service.get(ident)

        assert bool(welder)

        ctx = DeleteWelderCommand().make_context(info_name="delete-welder", args=[f"--ident={ident}"])
        DeleteWelderCommand().invoke(ctx)

        assert not bool(service.get(ident))

        service.add(**welder.model_dump())


class TestWelderCertificationCommands:

    @pytest.mark.usefixtures('welder_certifications')
    def test_add_welder_certification_command(self, welder_certifications: list[WelderCertificationShema]):
        service = WelderCertificationDBService()

        for cert in welder_certifications:
            if bool(service.get(cert.ident)):
                service.delete(cert.ident)

            args = from_shema_to_cmd_arguments(cert)

            ctx = AddWelderCertificationCommand().make_context(
                info_name="add-welder-certification", 
                args=args
            )
            AddWelderCertificationCommand().invoke(ctx)

            cert = service.get(cert.ident)
            assert service.get(cert.ident) == cert

        assert service.count() == len(welder_certifications)


    @pytest.mark.parametrize(
        "ident, data", 
        [
            ("cccba2a0ea9047c8837691a740513f6d", {"welding_materials_groups": ["aerre", "ggggg"], "certification_date": "15.12.1995"}),
            ("422786ffabd54d74867a8f34950ee0b5", {"job_title": "ппмфва", "kleymo": "11F9", "expiration_date": "1990-05-15"}),
            ("71c20a79706d4fb28f7b84e94881565c", {"insert": "В1", "company": "asasas", "expiration_date_fact": "2025-10-20"}),
            ("435a9de3ade64c38b316dd08c3c7bc7c", {"connection_type": "gggg", "outer_diameter_from": None, "details_type": ["ggg", "Л"]}),
        ]
    )
    def test_update_welder_certification_command(self, ident: str, data: dict) -> None:
        service = WelderCertificationDBService()

        cert = service.get(ident)
        args = list(from_dict_to_cmd_args(data))

        assert bool(cert)
        
        cert.update_shema(data)

        ctx = UpdateWelderCertificationCommand().make_context(info_name="update-welder-certification", args=[f"--ident={ident}", *args])
        UpdateWelderCertificationCommand().invoke(ctx)

        assert cert == service.get(ident)


    @pytest.mark.parametrize(
            "ident", 
            [
                "cccba2a0ea9047c8837691a740513f6d", 
                "422786ffabd54d74867a8f34950ee0b5", 
                "71c20a79706d4fb28f7b84e94881565c", 
                "435a9de3ade64c38b316dd08c3c7bc7c"
            ]
    )
    def test_delete_welder_command(self, ident: str) -> None:
        service = WelderCertificationDBService()

        cert = service.get(ident)

        assert bool(cert)

        ctx = DeleteWelderCertificationCommand().make_context(info_name="delete-welder-certification", args=[f"--ident={ident}"])
        DeleteWelderCertificationCommand().invoke(ctx)

        assert not bool(service.get(ident))

        service.add(**cert.model_dump())


class TestNDTCommands:

    @pytest.mark.usefixtures('ndts')
    def test_add_ndt_command(self, ndts: list[NDTShema]):
        service = NDTDBService()

        for ndt in ndts:
            if bool(service.get(ndt.ident)):
                service.delete(ndt.ident)

            args = from_shema_to_cmd_arguments(ndt)

            ctx = AddNDTCommand().make_context(
                info_name="add-ndt", 
                args=args
            )
            AddNDTCommand().invoke(ctx)
            assert service.get(ndt.ident) == ndt

        assert service.count() == len(ndts)


    @pytest.mark.parametrize(
        "ident, data", 
        [
            ("94c6aacab12a40f2af32abb3e376bd7f", {"kleymo": "01X0", "company": "ADADrf vvtt", "subcompany": "ffdff"}),
            ("d84b33123a484982920433d3797e6064", {"total_repair_3": "0.7", "welding_date": "25.01.2023"}),
            ("589d6b436c544737bf91059479c21b33", {"total_accepted_1": "54.3", "total_weld_2": None, "project": "GTD"})
        ]
    )
    def test_update_ndt_command(self, ident: str,  data: dict) -> None:
        service = NDTDBService()
        ndt = service.get(ident)

        assert bool(ndt)

        ndt.update_shema(data)

        ctx = UpdateNDTCommand().make_context(info_name="update-ndt", args=[f"--ident={ident}", *from_dict_to_cmd_args(data)])
        UpdateNDTCommand().invoke(ctx)

        assert ndt == service.get(ndt.ident)


    @pytest.mark.parametrize(
            "ident", ["b7b18d3d407a44818d0e57870303f280","ca00eec3ffff490695a01700365670b5","dededa2a08254be5a40945aa8f910b2a"]
    )
    def test_delete_ndt_command(self, ident: str) -> None:
        service = NDTDBService()

        ndt = service.get(ident)

        assert bool(ndt)

        ctx = DeleteNDTCommand().make_context(info_name="delete-ndt", args=[f"--ident={ident}"])
        DeleteNDTCommand().invoke(ctx)

        assert not bool(service.get(ident))

        service.add(**ndt.model_dump())
