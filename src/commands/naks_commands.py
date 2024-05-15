import typing as t
from pathlib import Path

from click import ClickException, Command, Option, group, echo

from services.naks.parse_services import IParseNaksService, ParsePersonalService
from utils.naks.parsers.results import BaseParseResult
from utils.funcs import read_json, gen_random_string, save_as_json
from _types import click_path_optional
from settings import Settings
from shemas import *


__all__ = [
    "parse_commands"
]


class BaseParseCommand(Command): 
    service: IParseNaksService[BaseParseResult]

    def __init__(self, name: str) -> None:
        super().__init__(
            name=name,
            params=self.options,
            callback=self.execute
        )
    
    
    def execute(self, v: list[str], from_file: Path | None, to_file: str | None, k: int) -> None:
        if from_file:
            v += self._read_file(from_file)

        result = self.service.parse(v, k)

        self._save_to_file(
            [el.model_dump(mode="json") for el in result],
            to_file
        )


    def _save_to_file(self, data: list | dict, to_file: str | None) -> None:
        if not to_file:
            file_name = f"data_{gen_random_string(10)}.json"

            save_as_json(
                data, 
                f"{Settings.SAVES_DIR()}/{file_name}"
            )

            
        elif to_file.endswith(".json"):
            save_as_json(
                data, 
                f"{Settings.SAVES_DIR()}/{to_file}"
            )
        
        else:
            ClickException("supports: .json")


    def _read_file(self, path: Path) -> list[str | int]:
        file_name = path.name

        if file_name.endswith(".json"):
            return self._read_json_file(path)
        else:
            raise ClickException("supports: .json")

    
    def _read_json_file(self, path: Path) -> list[str | int]:
        res = read_json(path)

        if not isinstance(res, list):
            raise ClickException(f"data in {path} is not list")
        
        for el in res:
            if not isinstance(el, (str, int)):
                raise ClickException(f"{el} is invalid data type")
            
        return res
    

    @property
    def options(self) -> list[Option]:
        return [
            Option(["-v"], type=str, multiple=True, help="search value"),
            Option(["-k"], type=int, default=1, help="parser threads amount"),
            Option(["--from-file", "-f"], type=click_path_optional),
            Option(["--to-file"], type=str, help="file name to store parsed data")
        ]


class ParsePersonalCommand(BaseParseCommand): 
    service = ParsePersonalService()
    def __init__(self) -> None:
        super().__init__(
            name="parse-personal"
        )


class ParseACSTCommand(BaseParseCommand): 
    def __init__(self) -> None:
        super().__init__(
            name="parse-acst"
        )


class ParseACSOCommand(BaseParseCommand): 
    def __init__(self) -> None:
        super().__init__(
            name="parse-acso"
        )


class ParseACSMCommand(BaseParseCommand): 
    def __init__(self) -> None:
        super().__init__(
            name="parse-acsm"
        )


@group("parse", help="parse welder|engineer|acst|acso|acsm data from naks")
def parse_commands():
    ...


parse_commands.add_command(ParsePersonalCommand())
# naks_commands.add_command(ParseACSTPersonalCommand())
# naks_commands.add_command(ParseACSOPersonalCommand())
# naks_commands.add_command(ParseACSMPersonalCommand())
