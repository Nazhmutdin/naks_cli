import typing as t
from uuid import UUID

from click import echo

from shemas import *
from utils.funcs import filtrate_extra_args
from repositories import *


def base_add_command[Data: t.TypedDict](repo: type[SQLAlchemyRepository], shema: type[BaseShema], data: Data):
    for key, value in data.items():
        if key == "ident":
            continue
        if value == "None":
            data[key] = None

    repo.add(**shema.model_validate(data).model_dump())


def base_update_command[Data: t.TypedDict](repo: type[SQLAlchemyRepository], shema: type[BaseShema], data: Data, ident: str | UUID):
    res: BaseShema = repo.get(ident)

    if not res:
        raise 

    res.model_validate(filtrate_extra_args(data))

    repo.update(ident, **res.model_dump(exclude_unset=True))


def base_delete_command(repo: SQLAlchemyRepository, ident: str | UUID):
    shema: BaseShema = repo.get(ident)
    
    if not shema:
        echo(f"({ident}) not found")
        return

    repo.delete(ident)
