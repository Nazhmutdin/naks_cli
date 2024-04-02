from uuid import UUID
import typing as t

from click import group, Command, Option
from rich.console import Console
from pydantic import ValidationError

from _types import WelderData, NDTData, WelderCertificationData
from utils.funcs import filtrate_extra_args, get_options, dicts_as_console_table
from services.db_services import BaseDBService
from services.db_services import *
from errors import (
    DBException, 
    AddCommandExeption, 
    UpdateCommandExeption, 
    DeleteCommandExeption, 
    GetCommandExeption
)
from shemas import *


__all__: list[str] = [
    "welder_commands",
    "welder_certification_commands",
    "ndt_commands"
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


    def _init_service(self) -> BaseDBService[BaseShema]: ...


class BaseGetCommand(Command):
    def __init__(self, name: str, options: t.Iterable[Option], help: str | None = None) -> None:
        super().__init__(
            name=name,
            params=options,
            help=help,
            callback=self.execute
        )


    def execute(self, ident: str, mode: str) -> None:
        res = self._get_data(ident)

        if not res:
            raise GetCommandExeption(f"data with ident ({ident}) not found")
        
        Console().print(dicts_as_console_table(res))
    

    def _get_data[Shema: BaseShema](self, ident: str) -> Shema | None:
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


    def _init_service(self) -> BaseDBService[BaseShema]: ...


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
        options = [Option(["--ident"], type=str), Option(["--mode"], type=str)]
        super().__init__(
            name="get",
            options=options
        )

    
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


@group("welder")
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
        options = [Option(["--ident"], type=str), Option(["--mode"], type=str)]
        super().__init__(
            name="get",
            options=options
        )

    
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


@group("welder-certification")
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
        options = [Option(["--ident"], type=str), Option(["--mode"], type=str)]
        super().__init__(
            name="get",
            options=options
        )

    
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


@group("ndt")
def ndt_commands():
    ...


ndt_commands.add_command(AddNDTCommand())
ndt_commands.add_command(GetNDTCommand())
ndt_commands.add_command(UpdateNDTCommand())
ndt_commands.add_command(DeleteNDTCommand())


"""
=========================================================
ndt commands
=========================================================
"""