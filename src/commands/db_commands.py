from uuid import UUID
from random import choices
from string import ascii_letters, digits
import json
import os
import typing as t

from click import Command, Option, Choice, ClickException, group, echo
from pydantic import ValidationError
from rich.console import Console

from utils.funcs import filtrate_extra_args, get_options, dicts_as_console_table, save_as_json, JsonRenderable
from _types import (
    WelderData, 
    NDTData, 
    WelderCertificationData
)
from services.db_services import *
from settings import Settings
from errors import (
    DBException, 
    AddCommandExeption, 
    UpdateCommandExeption, 
    DeleteCommandExeption, 
    GetCommandExeption,
    GetManyCommandExeption
)
from shemas import *


__all__: list[str] = [
    "welder_commands",
    "welder_certification_commands",
    "ndt_commands"
]


"""
=============================================================================================================
base db commands
=============================================================================================================
"""


class BaseAddCommand[CreateShema: BaseShema](Command):
    def __init__(self, name: str, options: t.Iterable[Option], help: str | None = None) -> None:
        self.__create_shema__: CreateShema

        super().__init__(
            name=name,
            params= self._default_options + options,
            help=help,
            callback=self.execute
        )


    def execute(self, from_file: str, **data) -> None:
        service = self._init_service()
        
        try:
            if from_file:
                data = self._read_data_from_file(from_file)
                
                if isinstance(data, list):
                    service.add(*[item for item in data])

                if isinstance(data, dict):
                    service.add(data)
                    
            else:
                service.add(self.__create_shema__.model_validate(filtrate_extra_args(data)))

        except ValidationError as e:
            raise AddCommandExeption(f"data validation failed\n\nDetail: {e}")
        except DBException as e:
            raise AddCommandExeption(f"adding failed\n\nDetail: {e.message}")
        

    def _read_data_from_file(self, file_path: str) -> JsonRenderable:

        if not os.path.exists(file_path):
            raise ClickException(f"file ({file_path}) not exists")
        
        if file_path.endswith(".json"):
            return json.load(open(file_path, "r", encoding="utf-8"))
        
        else:
            raise ClickException("invalid file extension")


    def _init_service(self) -> BaseDBService: ...
        
    
    @property
    def _default_options(self) -> list[Option]:
        return [
            Option(["--from-file"], type=str, default=None)
        ]


class BaseGetCommand[Shema: BaseShema](Command):
    def __init__(self, name: str, options: list[Option] = [], help: str | None = None) -> None:

        super().__init__(
            name=name,
            params= self._default_options + options,
            help=help,
            callback=self.execute
        )


    def execute(self, ident: str, mode: t.Literal["show", "json", "excel"], file_name: str | None) -> None:
        res = self._get_data(ident)

        if not res:
            raise GetCommandExeption(f"data with ident ({ident}) not found")
        
        if not file_name:
            file_name = self._gen_file_name()
        
        match mode:
            case "show":
                self._show_result(res)
            case "json":
                data = res.model_dump(mode="json")
                self._save_as_json(data, file_name)
            case "excel":
                raise NotImplementedError


    def _show_result(self, *shemas: Shema) -> None:
        Console().print(dicts_as_console_table(*shemas))

        
    def _save_as_json(self, data: JsonRenderable, file_name: str) -> None:
        path = f"{Settings.SAVES_DIR()}/{file_name}.json"

        save_as_json(data, path)
        
        echo(f"file ({file_name}.json) created | {len(data)} elements found")

    
    def _gen_file_name(self) -> str:
        return f"file_{"".join(choices(ascii_letters+digits, k=10))}"


    def _get_data(self, ident: str) -> Shema | None:
        service = self._init_service()

        try:
            return service.get(ident)
        except DBException as e:
            raise GetCommandExeption(f"failed getting data\n\nDetail: {e.message}")
        except Exception as e:
            raise GetCommandExeption(f"something gone wrong\n\nDetail: {e.args}")


    def _init_service(self) -> BaseDBService: ...
            
    
    @property
    def _default_options(self) -> list[Option]:
        return [
            Option(["--ident"], type=str), 
            Option(["--mode"], type=Choice(["show", "json", "excel"]), default="show"),
            Option(["--file-name"], type=str, default=None)
        ]
        

class BaseUpdateCommand[UpdateShema: BaseShema](Command):
    def __init__(self, name: str, options: list[Option] = [], help: str | None = None) -> None:
        self.__update_shema__: UpdateShema

        super().__init__(
            name=name, 
            params=self._default_options + options,
            help=help,
            callback=self.execute
        )


    def execute(self, ident: str | UUID, **data) -> None:

        service = self._init_service()
        UpdateCommandExeption(ident)
        try:
            data = filtrate_extra_args(data)
            service.update(ident, data)
        except ValidationError as e:
            raise UpdateCommandExeption(f"data validation failed\n\nDetail: {e.title}")
        except DBException as e:
            raise UpdateCommandExeption(f"update failed\n\nDetail: {e.message}")


    def _init_service(self) -> BaseDBService: ...
        
    
    @property
    def _default_options(self) -> list[Option]:
        return [
            Option(["--ident"], type=str, default=None)
        ]


class BaseDeleteCommand(Command):
    def __init__(self, name: str, options: t.Iterable[Option] = [], help: str | None = None) -> None:

        super().__init__(
            name=name, 
            params=self._default_options + options,
            help=help,
            callback=self.execute
        )


    def execute(self, ident: str | UUID) -> None:
        service = self._init_service()
        try:
            service.delete(ident)
        except DBException as e:
            raise DeleteCommandExeption(e.message)


    def _init_service(self) -> BaseDBService: ...
        
    
    @property
    def _default_options(self) -> list[Option]:
        return [
            Option(["--ident"], type=str, default=None)
        ]


"""
=============================================================================================================
welder commands
=============================================================================================================
"""


class AddWelderCommand(BaseAddCommand):
    def __init__(self) -> None:
        options = get_options(WelderData)
        self.__create_shema__ = CreateWelderShema

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

    
    def _init_service(self) -> WelderDBService:
        return WelderDBService()


class UpdateWelderCommand(BaseUpdateCommand):
    def __init__(self) -> None:
        options = get_options(WelderData)
        self.__update_shema__ = UpdateWelderShema

        super().__init__(
            name="update",
            options=options
        )


    def _init_service(self) -> WelderDBService:
        return WelderDBService()


class DeleteWelderCommand(BaseDeleteCommand):
    def __init__(self) -> None:
        super().__init__(
            name="delete"
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
=============================================================================================================
welder certification commands
=============================================================================================================
"""


class AddWelderCertificationCommand(BaseAddCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)] + get_options(WelderCertificationData)
        self.__create_shema__ = CreateWelderCertificationShema

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

    
    def _init_service(self) -> WelderCertificationDBService:
        return WelderCertificationDBService()


class UpdateWelderCertificationCommand(BaseUpdateCommand):
    def __init__(self) -> None:
        options = get_options(WelderCertificationData)
        self.__update_shema__ = UpdateWelderCertificationShema

        super().__init__(
            name="update",
            options=options
        )


    def _init_service(self) -> WelderCertificationDBService:
        return WelderCertificationDBService()


class DeleteWelderCertificationCommand(BaseDeleteCommand):
    def __init__(self) -> None:

        super().__init__(
            name="delete"
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
=============================================================================================================
ndt commands
=============================================================================================================
"""


class AddNDTCommand(BaseAddCommand):
    def __init__(self) -> None:
        options = [Option(["--ident"], type=str)] + get_options(NDTData)
        self.__create_shema__ = CreateNDTShema
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
    
    def _init_service(self) -> NDTDBService:
        return NDTDBService()


class UpdateNDTCommand(BaseUpdateCommand):
    def __init__(self) -> None:
        options = get_options(NDTData)
        self.__update_shema__ = UpdateNDTShema
        super().__init__(
            name="update",
            options=options
        )


    def _init_service(self) -> NDTDBService:
        return NDTDBService()


class DeleteNDTCommand(BaseDeleteCommand):
    def __init__(self) -> None:
        super().__init__(
            name="delete"
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
