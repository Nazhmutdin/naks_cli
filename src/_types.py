import typing as t
from datetime import date, datetime
from pathlib import Path

from pydantic import BaseModel, Field

from utils.funcs import click_date, click_date_required, click_float_optional, click_list


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


class DataBaseRequest(BaseModel):
    limit: t.Optional[int] = Field(default=None)
    offset: t.Optional[int] = Field(default=None)


class WelderCertificationDataBaseRequest(DataBaseRequest):
    kleymos: t.Optional[list[str | int]] = Field(default=None)
    ids: t.Optional[list[str]] = Field(default=None)
    certification_numbers: list[str] = Field(default=None)
    certification_date_from: t.Optional[date] = Field(default=None)
    certification_date_before: t.Optional[date] = Field(default=None)
    expiration_date_from: t.Optional[date] = Field(default=None)
    expiration_date_before: t.Optional[date] = Field(default=None)
    expiration_date_fact_from: t.Optional[date] = Field(default=None)
    expiration_date_fact_before: t.Optional[date] = Field(default=None)
    details_thikness_from: t.Optional[float] = Field(default=None)
    details_thikness_before: t.Optional[float] = Field(default=None)
    outer_diameter_from: t.Optional[float] = Field(default=None)
    outer_diameter_before: t.Optional[float] = Field(default=None)
    rod_diameter_from: t.Optional[float] = Field(default=None)
    rod_diameter_before: t.Optional[float] = Field(default=None)
    details_diameter_from: t.Optional[float] = Field(default=None)
    details_diameter_before: t.Optional[float] = Field(default=None)
    gtd: t.Optional[list[str]] = Field(default=None)
    method: t.Optional[list[str]] = Field(default=None)


class WelderDataBaseRequest(WelderCertificationDataBaseRequest):
    names: t.Optional[list[str]] = Field(default=None)


class NDTDataBaseRequest(DataBaseRequest):
    names: t.Optional[list[str]] = Field(default=None)
    kleymos: t.Optional[list[str | int]] = Field(default=None)
    comps: t.Optional[list[str]] = Field(default=None)
    subcomps: t.Optional[list[str]] = Field(default=None)
    projects: t.Optional[list[str]] = Field(default=None)
    welding_date_from: t.Optional[date] = Field(default=None)
    welding_date_before: t.Optional[date] = Field(default=None)


"""
====================================================================================================
Data dicts
====================================================================================================
"""


class WelderData(t.TypedDict):
    kleymo: str
    name: str
    birthday: t.Annotated[date, click_date]
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
    welding_date: t.Annotated[date, click_date]
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
