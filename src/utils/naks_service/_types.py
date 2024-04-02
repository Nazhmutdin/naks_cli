from pydantic import BaseModel, Field



"""
===========================================================================================================
Personal types
===========================================================================================================
"""


class PersonalMainPageResult(BaseModel):
    kleymo: str = Field()
    name: str | None = Field(default=None)
    company: str | None = Field(default=None)
    job_title: str | None = Field(default=None)
    certification_number: str = Field()
    insert: str | None = Field(default=None)
    certification_date: str = Field()
    expiration_date: str = Field()
    expiration_date_fact: str = Field()
    method: str | None = Field(default=None)


class PersonalAdditionalPageResult(BaseModel):
    kleymo: str = Field()
    certification_type: str | None = Field(default=None)
    gtd: list[str] | None = Field(default=None)
    details_type: list[str] | None = Field(default=None)
    joint_type: list[str] | None = Field(default=None)
    groups_materials_for_welding: list[str] | None = Field(default=None)
    welding_materials: str | None = Field(default=None)
    details_thikness_from: float | None = Field(default=None)
    details_thikness_before: float | None = Field(default=None)
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
    details_diameter_from: float | None = Field(default=None)
    details_diameter_before: float | None = Field(default=None)
    welding_equipment: str | None = Field(default=None)


class NaksPersonResult(BaseModel):
    kleymo: str = Field()
    name: str | None = Field(default=None)
    job_title: str | None = Field(default=None)
    certification_number: str = Field()
    certification_date: str = Field()
    expiration_date: str = Field()
    expiration_date_fact: str = Field()
    insert: str | None = Field(default=None)
    certification_type: str | None = Field(default=None)
    company: str | None = Field(default=None)
    gtd: list[str] | None = Field(default=None)
    method: str | None = Field(default=None)
    details_type: list[str] | None = Field(default=None)
    joint_type: list[str] | None = Field(default=None)
    groups_materials_for_welding: list[str] | None = Field(default=None)
    welding_materials: str | None = Field(default=None)
    details_thikness_from: float | None = Field(default=None)
    details_thikness_before: float | None = Field(default=None)
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
    details_diameter_from: float | None = Field(default=None)
    details_diameter_before: float | None = Field(default=None)
    welding_equipment: str | None = Field(default=None)
