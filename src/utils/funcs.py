from datetime import datetime, date
from dateutil.parser import parser
from ast import literal_eval
from json import dump, load
import typing as t

from click import ClickException, Option
from rich.table import Table

from errors import InvalidDateException
from settings import Settings


__all__ = [
    "filtrate_extra_args",
    "str_to_datetime",
    "click_date_required",
    "to_date",
    "click_date",
    "click_list_optional",
    "click_float_optional",
    "click_int_optional"
]

type JsonRenderable = list | dict


class IShortDumpShema(t.Protocol):
    def short_model_dump(self) -> dict[str, t.Any]: ...


def save_as_json(data: JsonRenderable, path: str, indent: int = 4, ensure_ascii: bool = False) -> None:
    with open(path, "w", encoding="utf-8") as file:
        dump(data, file, indent=indent, ensure_ascii=ensure_ascii)
        file.close()


def get_options[Data](data_type: type[Data]) -> list[Option]:
    options = []
    for key, value in data_type.__annotations__.items():
        if isinstance(value, t._AnnotatedAlias):
            state = value.__getstate__()
            options.append(Option([f"--{key}"], type=state["__metadata__"][0])) 

        else:
            options.append(Option([f"--{key}"], type=value)) 

    return options


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
    headers: list[str] = ["index"] + list(args[0].short_model_dump().keys())
    shemas_type = type(args[0])

    table = Table(title="Data", show_lines=True)

    for header in headers:
        table.add_column(header, header_style="cyan", justify="center")
        

    for e, arg in enumerate(args, start=1):
        if not isinstance(arg, shemas_type):
            raise ValueError()
        
        data = arg.short_model_dump()
        row_data = [str(e)] + list(map(str, data.values()))
        
        for e in range(len(row_data)):
            if row_data[e] is None:
                row_data[e] = "None"
            elif row_data[e] == "":
                row_data[e] = "-"
        
        table.add_row(*row_data, style="blue")

    return table


def read_gtd_data_json() -> dict[str, dict[str, str | dict]]:
    return load(open(f"{Settings.BASE_DIR()}/static/data/gtd_data.json", "r", encoding="utf-8"))


def get_gtd_description_short_dict(gtd_data: dict[str, dict[str, str | dict]] = read_gtd_data_json()) -> dict[str, str]:

    return {value["description"]: key  for key, value in gtd_data.items()}


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
    if not date_string or date_string == "None":
        return None
    
    _date = to_date(date_string, dayfirst=False)

    if not _date:
        return None
    
    return _date


@func_name_decorator("list or null")
def click_list_optional(string: str | None) -> list[t.Any] | None:

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


@func_name_decorator("int or null")
def click_int_optional(value: str | int | None) -> int | str | None:
    if value == None or isinstance(value, int):
        return value
    
    elif value == "None":
        return value
    
    else:
        try:
            return int(value)
        except:
            raise ClickException("invalid float string")


@func_name_decorator("str or null")
def click_str_optional(value: str | int | None) -> str | None:
    if value == None or isinstance(value, str):
        return value
    
    else:
        try:
            return str(value)
        except:
            raise ClickException(f"{value} cannot be converted to str")
