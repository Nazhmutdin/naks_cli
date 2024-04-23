import typing as t

from click import Command, group
from errors import NaksCommandExeption
from shemas import *


__all__ = [
    "naks_commands"
]


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
