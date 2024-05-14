from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator, field_serializer

from utils.funcs import to_date
from utils.naks.parsers.funcs import get_from_value_or_none, get_before_value_or_none, parse_gtds, parse_list_data


__all__ = [
    "BaseMainPageData",
    "BaseAdditionalPageData",
    "PersonalMainPageData",
    "PersonalAdditionalPageData"
]


"""
===========================================================================================================
Base types
===========================================================================================================
"""


class BaseMainPageData(BaseModel):
    additional_page_id: str


class BaseAdditionalPageData(BaseModel): ...


"""
===========================================================================================================
Personal types
===========================================================================================================
"""


class PersonalMainPageData(BaseMainPageData):
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


    @field_validator("certification_date", "expiration_date", "expiration_date_fact", mode="before")
    @classmethod
    def validate_date_fields(cls, v: str | date | None) -> date:
        date_value = to_date(v, True)

        if not date_value:
            raise ValueError(f"invalid date data: {v}")
        
        return date_value
        

class PersonalAdditionalPageData(BaseAdditionalPageData):
    certification_type: str | None = Field(default=None, alias="Вид аттестации:")
    details_type: str | None = Field(default=None, alias="Вид деталей")
    joint_type: str | None = Field(default=None, alias="Типы швов")
    welding_materials_groups: str | None = Field(default=None, alias="Группа свариваемого материала")
    welding_materials: str | None = Field(default=None, alias="Сварочные материалы")
    detail_thikness_string: str | None = Field(default=None, alias="Толщина деталей, мм")
    detail_diameter_string: str | None = Field(default=None, alias="Диаметр деталей, мм")
    outer_diameter_string: str | None = Field(default=None, alias="Наружный диаметр, мм")
    welding_position: str | None = Field(default=None, alias="Положение при сварке")
    connection_type: str | None = Field(default=None, alias="Вид соединения")
    rod_diameter_string: str | None = Field(default=None, alias="Диаметр стержня, мм")
    rod_axis_position: str | None = Field(default=None, alias="Положение осей стержней")
    welding_type: str | None = Field(default=None, alias="Тип сварного соединения")
    joint_layer: str | None = Field(default=None, alias="Слой шва")
    gtd: str | None = Field(default=None, alias="Группы технических устройств опасных производственных объектов:")
    sdr: str | None = Field(default=None, alias="SDR")
    automation_level: str | None = Field( default=None, alias="Степень автоматизации")
    welding_equipment: str | None = Field(default=None, alias="Сварочное оборудование")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


    @field_serializer("gtd")
    def serialize_gtd(self, value: str | None) -> list[str]:
        if not value:
            return None
        
        result = []

        for el in parse_gtds(value):
            if not el:
                continue

            result += el

        return result


    @field_serializer("joint_type", "details_type", "welding_materials_groups")
    def serialize_list_data(self, value: str | None) -> list[str]:

        result = parse_list_data(value)

        if not result:
            return None

        return result


    def model_dump(self, mode: str = "python"):

        data = super().model_dump(mode=mode)

        data["detail_thikness_from"] = get_from_value_or_none(self.detail_thikness_string)

        data["detail_thikness_before"] = get_before_value_or_none(self.detail_thikness_string)

        data["detail_diameter_from"] = get_from_value_or_none(self.detail_diameter_string)

        data["detail_diameter_before"] = get_before_value_or_none(self.detail_diameter_string)

        data["outer_diameter_from"] = get_from_value_or_none(self.outer_diameter_string)

        data["outer_diameter_before"] = get_before_value_or_none(self.outer_diameter_string)

        data["rod_diameter_from"] = get_from_value_or_none(self.rod_diameter_string)

        data["rod_diameter_before"] = get_before_value_or_none(self.rod_diameter_string)

        return data

