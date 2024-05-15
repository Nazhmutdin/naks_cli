import typing as t
from datetime import date, datetime
from ast import literal_eval
from pathlib import Path

from click import ClickException

from utils.funcs import to_date


__all__: list[str] = [
    "PathType",
    "AnyType",
    "DataBaseRequest",
    "WelderCertificationDataBaseRequest",
    "WelderDataBaseRequest",
    "NDTDataBaseRequest",
    "WelderData",
    "WelderCertificationData",
    "NDTData",
    "UserData"
]


type PathType = str | Path
type AnyType = str | int | float | date | datetime | None
type Kleymo = str | int


"""
====================================================================================================
func types
====================================================================================================
"""


def func_name_decorator(func_name: str):
    def inner(func: (...)):
        func.__name__ = func_name

        return func
    
    return inner


@func_name_decorator("date")
def click_date_required(date_string: str) -> date:
    _date = to_date(date_string, dayfirst=False)

    if not _date:
        raise ValueError(f"Invalid date data '{date_string}'")
    
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


@func_name_decorator("path or null")
def click_path_optional(value: str | None) -> Path | None:
    if value == None:
        return value
    
    path = Path(value)

    if not path.exists():
        raise ClickException(f"invalid path ({value})")
    
    return path


"""
====================================================================================================
Database Requests
====================================================================================================
"""


class DataBaseRequest(t.TypedDict):
    limit: t.Annotated[float | None, click_int_optional] 
    offset: t.Annotated[float | None, click_int_optional] 


class WelderCertificationDataBaseRequest(DataBaseRequest):
    kleymos: t.Annotated[list[str | int] | None, click_list_optional]
    idents: t.Annotated[list[str] | None, click_list_optional]
    certification_numbers: t.Annotated[list[str] | None, click_list_optional]
    certification_date_from: t.Annotated[date | None, click_date_optional]
    certification_date_before: t.Annotated[date | None, click_date_optional]
    expiration_date_from: t.Annotated[date | None, click_date_optional]
    expiration_date_before: t.Annotated[date | None, click_date_optional]
    expiration_date_fact_from: t.Annotated[date | None, click_date_optional]
    expiration_date_fact_before: t.Annotated[date | None, click_date_optional]
    details_thikness_from: t.Annotated[float | None, click_float_optional] 
    details_thikness_before: t.Annotated[float | None, click_float_optional] 
    outer_diameter_from: t.Annotated[float | None, click_float_optional] 
    outer_diameter_before: t.Annotated[float | None, click_float_optional] 
    rod_diameter_from: t.Annotated[float | None, click_float_optional] 
    rod_diameter_before: t.Annotated[float | None, click_float_optional] 
    details_diameter_from: t.Annotated[float | None, click_float_optional] 
    details_diameter_before: t.Annotated[float | None, click_float_optional] 
    gtds: t.Annotated[list[str] | None, click_list_optional]
    methods: t.Annotated[list[str] | None, click_list_optional]


class WelderDataBaseRequest(WelderCertificationDataBaseRequest):
    names: t.Annotated[list[str] | None, click_list_optional]


class NDTDataBaseRequest(DataBaseRequest):
    names: t.Annotated[list[str] | None, click_list_optional]
    kleymos: t.Annotated[list[str | int] | None, click_list_optional]
    comps: t.Annotated[list[str] | None, click_list_optional]
    subcomps: t.Annotated[list[str] | None, click_list_optional]
    projects: t.Annotated[list[str] | None, click_list_optional]
    welding_date_from: t.Annotated[date | None, click_date_optional]
    welding_date_before: t.Annotated[date | None, click_date_optional]


"""
====================================================================================================
Data dicts
====================================================================================================
"""


class WelderData(t.TypedDict):
    kleymo: t.Annotated[str | None, click_str_optional]
    name: t.Annotated[str | None, click_str_optional]
    birthday: t.Annotated[date | None, click_date_optional]
    passport_number: t.Annotated[str | None, click_str_optional]
    sicil: t.Annotated[str | None, click_str_optional]
    nation: t.Annotated[str | None, click_str_optional]
    status: t.Annotated[int | None, click_int_optional]


class WelderCertificationData(t.TypedDict):
    kleymo: t.Annotated[str | None, click_str_optional]
    job_title: t.Annotated[str | None, click_str_optional]
    certification_number: t.Annotated[str | None, click_str_optional]
    certification_date: t.Annotated[date, click_date_required]
    expiration_date: t.Annotated[date, click_date_required]
    expiration_date_fact: t.Annotated[date, click_date_required]
    insert: t.Annotated[str | None, click_str_optional] 
    certification_type: t.Annotated[str | None, click_str_optional] 
    company: t.Annotated[str | None, click_str_optional] 
    gtd: t.Annotated[list[str] | None, click_list_optional]
    method: t.Annotated[str | None, click_str_optional]
    details_type: t.Annotated[list[str] | None, click_list_optional]
    joint_type: t.Annotated[list[str] | None, click_list_optional]
    welding_materials_groups: t.Annotated[list[str] | None, click_list_optional]
    welding_materials: t.Annotated[str | None, click_str_optional] 
    details_thikness_from: t.Annotated[float | None, click_float_optional] 
    details_thikness_before: t.Annotated[float | None, click_float_optional] 
    outer_diameter_from: t.Annotated[float | None, click_float_optional] 
    outer_diameter_before: t.Annotated[float | None, click_float_optional] 
    welding_position: t.Annotated[str | None, click_str_optional] 
    connection_type: t.Annotated[str | None, click_str_optional] 
    rod_diameter_from: t.Annotated[float | None, click_float_optional] 
    rod_diameter_before: t.Annotated[float | None, click_float_optional] 
    rod_axis_position: t.Annotated[str | None, click_str_optional] 
    weld_type: t.Annotated[str | None, click_str_optional] 
    joint_layer: t.Annotated[str | None, click_str_optional] 
    sdr: t.Annotated[str | None, click_str_optional] 
    automation_level: t.Annotated[str | None, click_str_optional] 
    details_diameter_from: t.Annotated[float | None, click_float_optional] 
    details_diameter_before: t.Annotated[float | None, click_float_optional] 
    welding_equipment: t.Annotated[str | None, click_str_optional] 


class NDTData(t.TypedDict):
    kleymo: t.Annotated[str | None, click_str_optional]
    company: t.Annotated[str | None, click_str_optional]
    subcompany: t.Annotated[str | None, click_str_optional]
    project: t.Annotated[str | None, click_str_optional]
    welding_date: t.Annotated[date, click_date_required] 
    total_weld_1: t.Annotated[float | None, click_float_optional] 
    total_ndt_1: t.Annotated[float | None, click_float_optional] 
    total_accepted_1: t.Annotated[float | None, click_float_optional] 
    total_repair_1: t.Annotated[float | None, click_float_optional] 
    repair_status_1: t.Annotated[float | None, click_float_optional] 
    total_weld_2: t.Annotated[float | None, click_float_optional] 
    total_ndt_2: t.Annotated[float | None, click_float_optional] 
    total_accepted_2: t.Annotated[float | None, click_float_optional] 
    total_repair_2: t.Annotated[float | None, click_float_optional] 
    repair_status_2: t.Annotated[float | None, click_float_optional] 
    total_weld_3: t.Annotated[float | None, click_float_optional] 
    total_ndt_3: t.Annotated[float | None, click_float_optional] 
    total_accepted_3: t.Annotated[float | None, click_float_optional] 
    total_repair_3: t.Annotated[float | None, click_float_optional] 
    repair_status_3: t.Annotated[float | None, click_float_optional] 


class UserData(t.TypedDict):
    name: str
    login: str
    hashed_password: str
    email: str 
    sign_date: datetime
    update_date: datetime
    login_date: datetime
    is_active: bool
    is_superuser: bool
