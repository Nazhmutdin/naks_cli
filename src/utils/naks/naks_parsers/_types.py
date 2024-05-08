from datetime import date

from pydantic import BaseModel, Field, field_validator

from utils.funcs import to_date



"""
===========================================================================================================
Personal types
===========================================================================================================
"""


class PersonalMainPageData(BaseModel):
    kleymo: str
    name: str
    company: str
    job_title: str
    certification_number: str
    insert: str | None = Field(default=None)
    certification_date: date
    expiration_date: date
    expiration_date_fact: date
    method: str | None = Field(default=None)
    additional_page_id: str


    @field_validator("certification_date", "expiration_date", "expiration_date_fact", mode="before")
    @classmethod
    def validate_date_fields(cls, v: str | date | None) -> date:
        date_value = to_date(v)

        if not date_value:
            raise ValueError(f"invalid date data: {v}")
        
        return date_value
        

class PersonalAdditionalPageData(BaseModel):
    certification_type: str | None = Field(default=None)
    gtd: list[str] | None = Field(default=None)
    details_type: list[str] | None = Field(default=None)
    joint_type: list[str] | None = Field(default=None)
    welding_materials_groups: list[str] | None = Field(default=None)
    welding_materials: str | None = Field(default=None)
    detail_thikness_from: float | None = Field(default=None)
    detail_thikness_before: float | None = Field(default=None)
    detail_diameter_from: float | None = Field(default=None)
    detail_diameter_before: float | None = Field(default=None)
    outer_diameter_from: float | None = Field(default=None)
    outer_diameter_before: float | None = Field(default=None)
    welding_position: str | None = Field(default=None)
    connection_type: str | None = Field(default=None)
    rod_diameter_from: float | None = Field(default=None)
    rod_diameter_before: float | None = Field(default=None)
    rod_axis_position: str | None = Field(default=None)
    welding_type: str | None = Field(default=None)
    joint_layer: str | None = Field(default=None)
    sdr: str | None = Field(default=None)
    automation_level: str | None = Field(default=None)
    welding_equipment: str | None = Field(default=None)


class NaksPersonalResult(BaseModel):
    kleymo: str
    name: str
    certification_number: str
    certification_date: str
    expiration_date: str
    expiration_date_fact: str
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
