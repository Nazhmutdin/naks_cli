import typing as t
import pytest
import json

from db.db_engine import Base, engine
from settings import Settings

from shemas import *


settings = Settings()


@pytest.fixture(scope="module")
def prepare_db():
    assert settings.MODE() == "TEST"

    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def from_dict_to_cmd_args[T: dict](data: T) -> t.Iterator[str]:
    for key, value in data.items():

        yield f"--{key}={value}"


def from_shema_to_cmd_arguments[Shema: BaseShema](obj: Shema) -> list[str]:
    return list(from_dict_to_cmd_args(obj.model_dump(mode="json", exclude_unset=True, exclude_defaults=True)))


def get_welders() -> list[WelderShema]:
    welders = json.load(open("test/test_data/welders.json", "r", encoding="utf-8"))
    return [WelderShema.model_validate(welder) for welder in welders]


def get_welder_certifications() -> list[WelderCertificationShema]:
    certifications = json.load(open("test/test_data/welder_certifications.json", "r", encoding="utf-8"))
    return [WelderCertificationShema.model_validate(certification) for certification in certifications]


def get_ndts() -> list[NDTShema]:
    ndts = json.load(open("test/test_data/ndts.json", "r", encoding="utf-8"))
    return [NDTShema.model_validate(ndt) for ndt in ndts]


def get_invalid_welders() -> list[dict[str, t.Any]]:
    return json.load(open("test/test_data/invalid_welders.json", "r", encoding="utf-8"))


def get_invalid_welder_certifications() -> list[dict[str, t.Any]]:
    return json.load(open("test/test_data/invalid_welder_certifications.json", "r", encoding="utf-8"))


def get_invalid_ndts() -> list[dict[str, t.Any]]:
    return json.load(open("test/test_data/invalid_ndts.json", "r", encoding="utf-8"))


# def get_users() -> list[UserShema]:
#     ndts = json.load(open("test/test_data/users.json", "r", encoding="utf-8"))
#     return [UserShema.model_validate(ndt) for ndt in ndts]


@pytest.fixture
def welders() -> list[WelderShema]:
    return get_welders()


@pytest.fixture
def welder_certifications() -> list[WelderCertificationShema]:
    return get_welder_certifications()


@pytest.fixture
def ndts() -> list[NDTShema]:
    return get_ndts()


@pytest.fixture
def invalid_welders() -> list[dict[str, t.Any]]:
    return get_invalid_welders()


@pytest.fixture
def invalid_welder_certifications() -> list[dict[str, t.Any]]:
    return get_invalid_welder_certifications()


@pytest.fixture
def invalid_ndts() -> list[dict[str, t.Any]]:
    return get_invalid_ndts()

# @pytest.fixture
# def users() -> list[UserShema]:
#     return get_users()


# @pytest.fixture
# def test_welders() -> list[WelderShema]:
#     welders = json.load(open("test/test_data/_test_welders.json", "r", encoding="utf-8"))
#     return [WelderShema.model_validate(welder) for welder in welders]


# @pytest.fixture
# def test_welder_certifications() -> list[WelderCertificationShema]:
#     certifications = json.load(open("test/test_data/_test_welder_certifications.json", "r", encoding="utf-8"))
#     return [WelderCertificationShema.model_validate(certification) for certification in certifications]


# @pytest.fixture
# def test_welder_ndts() -> list[NDTShema]:
#     ndts = json.load(open("test/test_data/_test_welder_ndts.json", "r", encoding="utf-8"))
#     return [NDTShema.model_validate(ndt) for ndt in ndts]
