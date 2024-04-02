from uuid import UUID
from json import dump
import typing as t

from click import Command, Option, Choice, group, echo
from click.core import Parameter
from pydantic import ValidationError
from rich.console import Console

from utils.funcs import filtrate_extra_args, get_options, dicts_as_console_table, save_as_json
from _types import WelderData, NDTData, WelderCertificationData
from services.db_services import *
from settings import Settings
from errors import (
    DBException, 
    AddCommandExeption, 
    UpdateCommandExeption, 
    DeleteCommandExeption, 
    GetCommandExeption,
    GetManyCommandExeption,
    NaksCommandExeption
)
from shemas import *


__all__: list[str] = [
    "welder_commands",
    "welder_certification_commands",
    "ndt_commands",
    "naks_commands",
    "attestation_commands"
]


"""
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Database commands
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
"""


class BaseAddCommand(Command):
    def __init__(self, name: str, options: t.Iterable[Option], help: str | None = None) -> None:
        super().__init__(
            name=name, 
            params=options, 
            help=help,
            callback=self.execute
        )


    def execute(self, **data) -> None:
        service = self._init_service()
        
        try:
            service.add(**filtrate_extra_args(data))
        except ValidationError as e:
            raise AddCommandExeption(f"data validation failed\n\nDetail: {e}")
        except DBException as e:
            raise AddCommandExeption(f"adding failed\n\nDetail: {e.message}")


    def _init_service(self) -> BaseDBService: ...


class BaseGetCommand[Shema: BaseShema](Command):
    def __init__(self, name: str, options: list[Option] = [], help: str | None = None) -> None:
        default_options = [Option(["--ident"], type=str), Option(["--mode"], type=Choice(["show", "json", "excel"]), default="show")]

        super().__init__(
            name=name,
            params=default_options + options,
            help=help,
            callback=self.execute
        )


    def execute(self, ident: str, mode: t.Literal["show", "json", "excel"]) -> None:
        res = self._get_data(ident)

        if not res:
            raise GetCommandExeption(f"data with ident ({ident}) not found")
        
        match mode:
            case "show":
                self._show_result(res)
            case "json":
                self._save_as_json(res)
            case "excel":
                raise NotImplementedError


    def _show_result(self, shema: Shema) -> None:
        Console().print(dicts_as_console_table(shema))

        
    def _save_as_json(self, shema: Shema) -> None:
        file_name = self._gen_file_name(shema)
        data = shema.model_dump(mode="json")
        path = f"{Settings.SAVES_DIR()}/{file_name}.json"

        save_as_json(data, path)
        
        echo(f"file ({file_name}.json) created")

    
    def _gen_file_name(self, shema: Shema) -> str:
        raise NotImplementedError


    def _get_data(self, ident: str) -> Shema | None:
        service = self._init_service()

        try:
            return service.get(ident)
        except DBException as e:
            raise GetCommandExeption(f"failed getting data\n\nDetail: {e.message}")
        except Exception as e:
            raise GetCommandExeption(f"something gone wrong\n\nDetail: {e.args[0]}")


    def _init_service(self) -> BaseDBService[BaseShema]: ...


class BaseUpdateCommand(Command):
    def __init__(self, name: str, options: t.Iterable[Option], help: str | None = None) -> None:
        super().__init__(
            name=name, 
            params=options, 
            help=help,
            callback=self.execute
        )


    def execute(self, ident: str | UUID, **data) -> None:
        service = self._init_service()
        try:
            service.update(ident, **filtrate_extra_args(data))
        except ValidationError as e:
            raise UpdateCommandExeption(f"data validation failed\n\nDetail: {e.title}")
        except DBException as e:
            raise UpdateCommandExeption(f"update failed\n\nDetail: {e.message}")


    def _init_service(self) -> BaseDBService: ...


class BaseDeleteCommand(Command):
    def __init__(self, name: str, options: t.Iterable[Option], help: str | None = None) -> None:
        super().__init__(
            name=name, 
            params=options, 
            help=help,
            callback=self.execute
        )


    def execute(self, ident: str | UUID) -> None:
        service = self._init_service()
        try:
            service.delete(ident)
        except DBException as e:
            raise DeleteCommandExeption(e.message)


    def _init_service(self) -> BaseDBService[BaseShema]: ...


"""
=========================================================
welder commands
=========================================================
"""

class AddWelderCommand(BaseAddCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)] + list(get_options(WelderData))
        super().__init__(
            name="add",
            options=options
        )

    
    def _init_service(self) -> WelderDBService:
        return WelderDBService()


class GetWelderCommand(BaseGetCommand):
    def __init__(self) -> None:
        super().__init__(
            name="get"
        )

    
    def _gen_file_name(self, shema: WelderShema) -> str:
        return f"{shema.kleymo}_{shema.name}"

    
    def _init_service(self) -> WelderDBService:
        return WelderDBService()


class UpdateWelderCommand(BaseUpdateCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)] + list(get_options(WelderData))
        super().__init__(
            name="update",
            options=options
        )


    def _init_service(self) -> WelderDBService:
        return WelderDBService()


class DeleteWelderCommand(BaseDeleteCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)]
        super().__init__(
            name="delete",
            options=options
        )


    def _init_service(self) -> WelderDBService:
        return WelderDBService()


@group("welder", help="CRUD actions with welder data")
def welder_commands():
    ...

welder_commands.add_command(AddWelderCommand())
welder_commands.add_command(GetWelderCommand())
welder_commands.add_command(UpdateWelderCommand())
welder_commands.add_command(DeleteWelderCommand())


"""
=========================================================
welder certification commands
=========================================================
"""


class AddWelderCertificationCommand(BaseAddCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)] + list(get_options(WelderCertificationData))
        super().__init__(
            name="add",
            options=options
        )

    
    def _init_service(self) -> WelderCertificationDBService:
        return WelderCertificationDBService()


class GetWelderCertificationCommand(BaseGetCommand):
    def __init__(self) -> None:
        super().__init__(
            name="get"
        )

    
    def _gen_file_name(self, shema: WelderCertificationShema) -> str:
        certification_number = shema.certification_number

        if shema.insert:
            certification_number = f"{certification_number}~{shema.insert}"

        return f"{shema.kleymo}_{certification_number}_{shema.certification_date}"

    
    def _init_service(self) -> WelderCertificationDBService:
        return WelderCertificationDBService()


class UpdateWelderCertificationCommand(BaseUpdateCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)] + list(get_options(WelderCertificationData))
        super().__init__(
            name="update",
            options=options
        )


    def _init_service(self) -> WelderCertificationDBService:
        return WelderCertificationDBService()


class DeleteWelderCertificationCommand(BaseDeleteCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)]
        super().__init__(
            name="delete",
            options=options
        )


    def _init_service(self) -> WelderCertificationDBService:
        return WelderCertificationDBService()


@group("welder-certification", help="CRUD actions with welder's certification data")
def welder_certification_commands():
    ...


welder_certification_commands.add_command(AddWelderCertificationCommand())
welder_certification_commands.add_command(GetWelderCertificationCommand())
welder_certification_commands.add_command(UpdateWelderCertificationCommand())
welder_certification_commands.add_command(DeleteWelderCertificationCommand())


"""
=========================================================
ndt commands
=========================================================
"""


class AddNDTCommand(BaseAddCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)] + list(get_options(NDTData))
        super().__init__(
            name="add",
            options=options
        )

    
    def _init_service(self) -> NDTDBService:
        return NDTDBService()


class GetNDTCommand(BaseGetCommand):
    def __init__(self) -> None:
        super().__init__(
            name="get"
        )

    
    def _gen_file_name(self, shema: NDTShema) -> str:
        return f"{shema.kleymo}_{shema.company}_{shema.subcompany}_{shema.project}_{shema.welding_date}"

    
    def _init_service(self) -> NDTDBService:
        return NDTDBService()


class UpdateNDTCommand(BaseUpdateCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)] + list(get_options(NDTData))
        super().__init__(
            name="update",
            options=options
        )


    def _init_service(self) -> NDTDBService:
        return NDTDBService()


class DeleteNDTCommand(BaseDeleteCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)]
        super().__init__(
            name="delete",
            options=options
        )


    def _init_service(self) -> NDTDBService:
        return NDTDBService()


@group("ndt", help="CRUD actions with ndt data")
def ndt_commands():
    ...


ndt_commands.add_command(AddNDTCommand())
ndt_commands.add_command(GetNDTCommand())
ndt_commands.add_command(UpdateNDTCommand())
ndt_commands.add_command(DeleteNDTCommand())


"""
=========================================================
naks commands
=========================================================
"""


class BaseParseNaksCommand(Command): 
    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            callback=self.execute
        )
    
    
    def execute(self) -> None:
        raise NaksCommandExeption("not implemented")


class ParseNaksPersonalCommand(BaseParseNaksCommand): 
    def __init__(self) -> None:
        super().__init__(
            name="parse-personal"
        )


class ParseACSTPersonalCommand(BaseParseNaksCommand): 
    def __init__(self) -> None:
        super().__init__(
            name="parse-acst"
        )


class ParseACSOPersonalCommand(BaseParseNaksCommand): 
    def __init__(self) -> None:
        super().__init__(
            name="parse-acso"
        )


class ParseACSMPersonalCommand(BaseParseNaksCommand): 
    def __init__(self) -> None:
        super().__init__(
            name="parse-acsm"
        )


@group("naks", help="extract welders | engineers | acst | acso | acsm data from naks site")
def naks_commands():
    ...


naks_commands.add_command(ParseNaksPersonalCommand())
naks_commands.add_command(ParseACSTPersonalCommand())
naks_commands.add_command(ParseACSOPersonalCommand())
naks_commands.add_command(ParseACSMPersonalCommand())


"""
=========================================================
attestation commands
=========================================================
"""


@group("attestation", help="creates attestation docs for welders | engineers | acst | acso | acsm")
def attestation_commands():
    ...
