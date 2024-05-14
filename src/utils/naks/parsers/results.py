from typing import Any
from datetime import date
import re

from pydantic import BaseModel, Field, field_validator

from utils.funcs import to_date



__all__ = [
    "BaseParseResult",
    "PersonalParseResult",
    "ACSTParseResult",
    "ACSOParseResult",
    "ACSMParseResult",
]


class BaseParseResult(BaseModel): 
    ...


class PersonalParseResult(BaseParseResult):
    kleymo: str
    name: str
    certification_number: str
    certification_date: date
    expiration_date: date
    expiration_date_fact: date
    job_title: str | None = Field(default=None)
    insert: str | None = Field(default=None)
    certification_type: str | None = Field(default=None)
    company: str | None = Field(default=None)
    gtd: list[str] | None = Field(default=None)
    method: str | None = Field(default=None)
    details_type: list[str] | None = Field(default=None)
    joint_type: list[str] | None = Field(default=None)
    welding_materials_groups: list[str] | None = Field(default=None)
    welding_materials: str | None = Field(default=None)
    detail_thikness_from: float | None = Field(default=None)
    detail_thikness_before: float | None = Field(default=None)
    outer_diameter_from: float | None = Field(default=None)
    outer_diameter_before: float | None = Field(default=None)
    welding_position: str | None = Field(default=None)
    connection_type: str | None = Field(default=None)
    rod_diameter_from: float | None = Field(default=None)
    rod_diameter_before: float | None = Field(default=None)
    rod_axis_position: str | None = Field(default=None)
    weld_type: str | None = Field(default=None)
    joint_layer: str | None = Field(default=None)
    sdr: str | None = Field(default=None)
    automation_level: str | None = Field(default=None)
    detail_diameter_from: float | None = Field(default=None)
    detail_diameter_before: float | None = Field(default=None)
    welding_equipment: str | None = Field(default=None)
    
    detail_thikness_string: str | None = Field(default=None)
    detail_diameter_string: str | None = Field(default=None,)
    outer_diameter_string: str | None = Field(default=None,)
    rod_diameter_string: str | None = Field(default=None)


    @field_validator("certification_date", "expiration_date", "expiration_date_fact", mode="before")
    @classmethod
    def validate_date_values(cls, value: date | str | None) -> date:
        
        if isinstance(value, date):
            return value
        
        date_result = to_date(value)

        if not date_result:
            raise ValueError(f"Invalid date data: {value}")
        
        return date_result


class ACSTParseResult(BaseParseResult):
    ...


class ACSOParseResult(BaseParseResult):
    ...


class ACSMParseResult(BaseParseResult):
    ...