from datetime import datetime, timedelta, date
from dataclasses import dataclass
import typing as t
import re

from pydantic import BaseModel, Field, model_validator, computed_field, field_validator
from naks_library.utils.validators import (
    before_optional_datetime_validator, 
    plain_optional_datetime_serializer, 
    plain_date_serializer,
    before_date_validator
)

from src.utils.parse_utils import parse_gtds, parse_list_data, get_from_value_or_none, get_before_value_or_none


class TokenShema(BaseModel):
    token: str
    gen_dt: t.Annotated[t.Optional[datetime], before_optional_datetime_validator, plain_optional_datetime_serializer] = Field(default=None)
    exp_dt: t.Annotated[t.Optional[datetime], before_optional_datetime_validator, plain_optional_datetime_serializer] = Field(default=None)


    @computed_field
    @property
    def expired(self) -> bool:
        if self.exp_dt is None:
            return False
        
        return self.exp_dt > datetime.now()


    @computed_field
    @property
    def exists(self) -> bool:
        return bool(self.token)


class AccessTokenShema(TokenShema): 

    @model_validator(mode="after")
    def set_gen_dt(self) -> t.Self:

        if self.gen_dt is None:
            self.gen_dt = self.exp_dt - timedelta(minutes=60)

        return self


class RefreshTokenShema(TokenShema): 

    @model_validator(mode="after")
    def set_gen_dt(self):

        if not self.gen_dt:
            self.gen_dt = self.exp_dt - timedelta(days=1)

        return self


class TokensDataShema(BaseModel):
    access_token: AccessTokenShema
    refresh_token: RefreshTokenShema


@dataclass
class SearchNaksCertificationItem:
    kleymo: str = ""
    name: str = ""
    cert_abbr: str = ""
    cert_lvl: str = ""
    cert_number: str = ""


class PersonalNaksCertificationData(BaseModel):
    name: str
    kleymo: str | None = None
    certification_number: str
    certification_date: t.Annotated[date, before_date_validator, plain_date_serializer]
    expiration_date: t.Annotated[date, before_date_validator, plain_date_serializer]
    expiration_date_fact: t.Annotated[date, before_date_validator, plain_date_serializer]
    insert: str | None = Field(default=None)
    company: str
    gtd: list[str]
    method: str | None = Field(default=None)
    detail_types: list[str] | None = Field(default=None)
    joint_types: list[str] | None = Field(default=None)
    materials: list[str] | None = Field(default=None)
    detail_thikness_from: float | None = Field(default=None)
    detail_thikness_before: float | None = Field(default=None)
    outer_diameter_from: float | None = Field(default=None)
    outer_diameter_before: float | None = Field(default=None)
    rod_diameter_from: float | None = Field(default=None)
    rod_diameter_before: float | None = Field(default=None)
    detail_diameter_from: float | None = Field(default=None)
    detail_diameter_before: float | None = Field(default=None)
    html: str


    @field_validator("gtd", mode="before")
    @classmethod
    def parse_gtd(cls, value: str) -> list[str]:
        result = []

        if value == "":
            return []

        for el in parse_gtds(value):
            if not el:
                continue

            result += el

        return result


    @field_validator("materials", mode="before")
    @classmethod
    def parse_materials(cls, value: str | None) -> list[str] | None:

        if value is None:
            return None

        value = value.replace("M", "М")
        material_pattern = re.compile(r"(М[0-9]+)(\+М[0-9]+)?")

        res = material_pattern.findall(value)

        return ["".join(el) for el in res]


    @field_validator("detail_types", "joint_types", mode="before")
    @classmethod
    def parse_list_values(cls, value: str | None) -> list[str] | None:

        if value is None:
            return None

        result = parse_list_data(value)

        if not result:
            return None

        return result


    @model_validator(mode="before")
    @classmethod
    def parse_from_before_values(cls, data: dict) -> dict: 

        data["detail_thikness_from"] = get_from_value_or_none(data["detail_thikness_string"])

        data["detail_thikness_before"] = get_before_value_or_none(data["detail_thikness_string"])

        data["detail_diameter_from"] = get_from_value_or_none(data["detail_diameter_string"])

        data["detail_diameter_before"] = get_before_value_or_none(data["detail_diameter_string"])

        data["outer_diameter_from"] = get_from_value_or_none(data["outer_diameter_string"])

        data["outer_diameter_before"] = get_before_value_or_none(data["outer_diameter_string"])

        data["rod_diameter_from"] = get_from_value_or_none(data["rod_diameter_string"])

        data["rod_diameter_before"] = get_before_value_or_none(data["rod_diameter_string"])

        return data
