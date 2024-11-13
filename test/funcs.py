from datetime import datetime, timedelta, UTC
import typing as t

from jose.jwt import encode as jwt_encode
from http.cookies import SimpleCookie


def from_dict_to_cmd_args[T: dict](data: T) -> t.Iterator[str]:
    for key, value in data.items():

        yield f"--{key}={value}"


def create_test_access_token() -> str:
    payload = {
        "user_ident": "bd4f45dab3bf41bc979d285d54f0ad03",
        "gen_dt": datetime.now(UTC).strftime("%Y/%m/%d, %H:%M:%S.%f")
    }

    return jwt_encode(payload, "test_key", "HS256")


def create_test_refresh_token() -> str:
    payload = {
        "user_ident": "bd4f45dab3bf41bc979d285d54f0ad03",
        "ident": "bd4f4fgdb3bf41bc654d285d54f0ad03",
        "gen_dt": datetime.now(UTC).strftime("%Y/%m/%d, %H:%M:%S.%f"),
        "exp_dt": datetime.fromtimestamp(create_refresh_token_expires()).strftime("%Y/%m/%d, %H:%M:%S.%f")
    }

    return jwt_encode(payload, "test_key", "HS256")


def create_access_token_expires() -> float:
    return (datetime.now(UTC) + timedelta(minutes=60)).replace(tzinfo=None).timestamp()


def create_refresh_token_expires() -> float:
    return (datetime.now(UTC) + timedelta(hours=24)).replace(tzinfo=None).timestamp()


def create_access_token_cookie() -> SimpleCookie:

    cookie = SimpleCookie()

    cookie["access_token"] = create_test_access_token()
    cookie["access_token"]["expires"] = datetime.fromtimestamp(create_refresh_token_expires()).strftime("%a, %d %b %Y %H:%M:%S GMT")
    cookie["access_token"]["path"] = "/v1"

    return cookie


def create_refresh_token_cookie() -> SimpleCookie:

    cookie = SimpleCookie()

    cookie["refresh_token"] = create_test_refresh_token()
    cookie["refresh_token"]["expires"] = datetime.fromtimestamp(create_refresh_token_expires()).strftime("%a, %d %b %Y %H:%M:%S GMT")
    cookie["refresh_token"]["path"] = "/auth"

    return cookie


# def get_welders() -> list[WelderData]:
#     return json.load(open("test/test_data/welders.json", "r", encoding="utf-8"))


# def get_welder_certifications() -> list[WelderCertificationData]:
#     return json.load(open("test/test_data/welder_certifications.json", "r", encoding="utf-8"))


# def get_ndts() -> list[NDTData]:
#     return json.load(open("test/test_data/ndts.json", "r", encoding="utf-8"))


# def get_invalid_welders() -> list[dict[str, t.Any]]:
#     return json.load(open("test/test_data/invalid_welders.json", "r", encoding="utf-8"))


# def get_invalid_welder_certifications() -> list[dict[str, t.Any]]:
#     return json.load(open("test/test_data/invalid_welder_certifications.json", "r", encoding="utf-8"))


# def get_invalid_ndts() -> list[dict[str, t.Any]]:
#     return json.load(open("test/test_data/invalid_ndts.json", "r", encoding="utf-8"))


# def get_test_welder_registry() -> Path:
#     return Settings.BASE_DIR() / "test" / "test_data" / "test_welder_registry.xlsx"
