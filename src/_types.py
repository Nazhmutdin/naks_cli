import typing as t
from datetime import date, datetime
from pathlib import Path

from utils.funcs import click_date_optional, click_date_required, click_float_optional, click_list


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
Database Requests
====================================================================================================
"""


class DataBaseRequest(t.TypedDict):
    limit: int | None
    offset: int | None


class WelderCertificationDataBaseRequest(DataBaseRequest):
    kleymos: t.Annotated[list[str | int] | None, click_list]
    idents: t.Annotated[list[str] | None, click_list]
    certification_numbers: t.Annotated[list[str] | None, click_list]
    certification_date_from: t.Annotated[date | None, click_date_optional]
    certification_date_before: t.Annotated[date | None, click_date_optional]
    expiration_date_from: t.Annotated[date | None, click_date_optional]
    expiration_date_before: t.Annotated[date | None, click_date_optional]
    expiration_date_fact_from: t.Annotated[date | None, click_date_optional]
    expiration_date_fact_before: t.Annotated[date | None, click_date_optional]
    details_thikness_from: float | None
    details_thikness_before: float | None
    outer_diameter_from: float | None
    outer_diameter_before: float | None
    rod_diameter_from: float | None
    rod_diameter_before: float | None
    details_diameter_from: float | None
    details_diameter_before: float | None
    gtds: t.Annotated[list[str] | None, click_list]
    methods: t.Annotated[list[str] | None, click_list]


class WelderDataBaseRequest(WelderCertificationDataBaseRequest):
    names: t.Annotated[list[str] | None, click_list]


class NDTDataBaseRequest(DataBaseRequest):
    names: t.Annotated[list[str] | None, click_list]
    kleymos: t.Annotated[list[str | int] | None, click_list]
    comps: t.Annotated[list[str] | None, click_list]
    subcomps: t.Annotated[list[str] | None, click_list]
    projects: t.Annotated[list[str] | None, click_list]
    welding_date_from: t.Annotated[date | None, click_date_optional]
    welding_date_before: t.Annotated[date | None, click_date_optional]


"""
====================================================================================================
Data dicts
====================================================================================================
"""


class WelderData(t.TypedDict):
    kleymo: str
    name: str
    birthday: t.Annotated[date | None, click_date_optional]
    passport_number: str
    sicil: str
    nation: str
    status: int


class WelderCertificationData(t.TypedDict):
    kleymo: str
    job_title: str
    certification_number: str
    certification_date: t.Annotated[date, click_date_required]
    expiration_date: t.Annotated[date, click_date_required]
    expiration_date_fact: t.Annotated[date, click_date_required]
    insert: str 
    certification_type: str 
    company: str 
    gtd: t.Annotated[list[str] | None, click_list]
    method: str
    details_type: t.Annotated[list[str] | None, click_list]
    joint_type: t.Annotated[list[str] | None, click_list]
    groups_materials_for_welding: t.Annotated[list[str] | None, click_list]
    welding_materials: str 
    details_thikness_from: t.Annotated[float | None, click_float_optional] 
    details_thikness_before: t.Annotated[float | None, click_float_optional] 
    outer_diameter_from: t.Annotated[float | None, click_float_optional] 
    outer_diameter_before: t.Annotated[float | None, click_float_optional] 
    welding_position: str 
    connection_type: str 
    rod_diameter_from: t.Annotated[float | None, click_float_optional] 
    rod_diameter_before: t.Annotated[float | None, click_float_optional] 
    rod_axis_position: str 
    weld_type: str 
    joint_layer: str 
    sdr: str 
    automation_level: str 
    details_diameter_from: t.Annotated[float | None, click_float_optional] 
    details_diameter_before: t.Annotated[float | None, click_float_optional] 
    welding_equipment: str 


class NDTData(t.TypedDict):
    kleymo: str
    company: str
    subcompany: str
    project: str
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
