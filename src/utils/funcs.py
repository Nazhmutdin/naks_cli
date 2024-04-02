from dateutil.parser import parser
from datetime import datetime, date
from ast import literal_eval
import typing as t

from click import ClickException, option, Option
from rich.table import Table

from errors import InvalidDateException


__all__ = [
    "click_extra_args_decorator",
    "filtrate_extra_args",
    "str_to_datetime",
    "click_date_required",
    "to_date",
    "click_date",
    "click_float_optional"
]


class IShortDumpShema(t.Protocol):
    def short_model_dump(self) -> dict[str, t.Any]: ...



def get_options[Data: t.TypedDict](data_type: type[Data]) -> t.Iterator[Option]:
    for key, value in data_type.__annotations__.items():
        if isinstance(value, t._AnnotatedAlias):
            state = value.__getstate__()
            yield Option([f"--{key}"], type=state["__metadata__"][0])

        else:
            yield Option([f"--{key}"], type=value)


def click_extra_args_decorator[Data: t.TypedDict](cls: type[Data]):
    def inner(func: t.Callable[..., t.Any]):
        for key, value in cls.__annotations__.items():
            if isinstance(value, t._AnnotatedAlias):
                state = value.__getstate__()
                option(f"--{key}", type=state["__metadata__"][0])(func)

            else:
                option(f"--{key}", type=value)(func)
        
        return func
        
    return inner


def click_extra_args[Data: t.TypedDict](cls: type[Data]) -> t.Iterator[Option]:
    for key, value in cls.__annotations__.items():
        if isinstance(value, t._AnnotatedAlias):
            state = value.__getstate__()
            yield Option(f"--{key}", type=state["__metadata__"][0])

        else:
            yield Option(f"--{key}", type=value)


def filtrate_extra_args(data: dict[str, t.Any]) -> dict[str, t.Any]:
    res = {}
    
    for key, value in data.items():
        if value == None:
            continue
        elif value == "None":
            res[key] = None
        else:
            res[key] = value
    
    return res 


def str_to_datetime(date_string, dayfirst: bool = False) -> datetime | None:
    try:
        return parser().parse(date_string, dayfirst=dayfirst)
    except:
        return None


def to_date(date_data: str | date | t.Iterable[int] | None, dayfirst: bool = False) -> date | None:
    if not date_data:
        return None
    
    if isinstance(date_data, date):
        return date_data
    
    if isinstance(date_data, str):
        _datetime = str_to_datetime(date_data, dayfirst)
        if not _datetime:
            raise InvalidDateException(f"Invalid date data '{date_data}'")

        return _datetime.date()
    
    if isinstance(date_data, t.Iterable) and len(date_data) == 3:
        return date(*date_data)
    
    raise InvalidDateException(f"Invalid date data '{date_data}'")


def dicts_as_console_table[Shema: IShortDumpShema](*args: Shema) -> Table: 
    dict_for_print: dict[str, list] = {}
    headers: list[str] = ["index"] + list(args[0].short_model_dump().keys())
    shemas_type = type(args[0])

    table = Table(title="Data", show_lines=True)

    for header in headers:
        table.add_column(header, header_style="cyan", justify="center")
        

    for e, arg in enumerate(args):
        if not isinstance(arg, shemas_type):
            raise ValueError()
        
        data = arg.short_model_dump()
        row_data = [str(e)] + list(map(str, data.values()))
        row_data = [i for i in row_data]
        
        for e in range(len(row_data)):
            if row_data[e] is None:
                row_data[e] = "None"
            elif row_data[e] == "":
                row_data[e] = "-"
        
        table.add_row(*row_data, style="blue")

    return table


def func_name_decorator(func_name: str):
    def inner(func: (...)):
        func.__name__ = func_name

        return func
    
    return inner


@func_name_decorator("date")
def click_date_required(date_string: str) -> date:
    _date = to_date(date_string, dayfirst=False)

    if not _date:
        raise InvalidDateException(f"Invalid date data '{date_string}'")
    
    return _date


@func_name_decorator("date or null")
def click_date_optional(date_string: str) -> date | None:
    _date = to_date(date_string, dayfirst=False)

    if not _date:
        return None
    
    return _date


@func_name_decorator("list or null")
def click_list(string: str | None) -> list[t.Any] | None:

    if not string:
        return None
    
    _list = literal_eval(string)
    
    return _list


@func_name_decorator("float or null")
def click_float_optional(value: str | float | None) -> float | str | None:
    if value == None or isinstance(value, float):
        return value
    
    elif value == "None":
        return value
    
    else:
        try:
            return float(value)
        except:
            raise ClickException("invalid float string")
