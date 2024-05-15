from datetime import datetime, date
from dateutil.parser import parser
from random import choices
from json import dump, load
from string import digits, ascii_letters
import typing as t

from click import Option
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



class IShortDumpShema(t.Protocol):
    def short_model_dump(self) -> dict[str, t.Any]: ...


def gen_random_string(k: int = 1) -> str:
    elements = choices(digits + ascii_letters, k=k)

    return "".join(elements)


def save_as_json(data: list | dict, path: str, indent: int = 4, ensure_ascii: bool = False) -> None:
    with open(path, "w", encoding="utf-8") as file:
        dump(data, file, indent=indent, ensure_ascii=ensure_ascii)
        file.close()


def read_json(path: str) -> list | dict:
    return load(open(path, "r", encoding="utf-8"))


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
