# import typing as t
# import pytest
# import json
# from funcs import get_invalid_welders, get_invalid_welder_certifications, get_invalid_ndts


# @pytest.fixture
# def invalid_welders() -> list[dict[str, t.Any]]:
#     return get_invalid_welders()


# @pytest.fixture
# def invalid_welder_certifications() -> list[dict[str, t.Any]]:
#     return get_invalid_welder_certifications()


# @pytest.fixture
# def invalid_ndts() -> list[dict[str, t.Any]]:
#     return get_invalid_ndts()


# @pytest.fixture
# def personal_parse_results() -> dict[str, list[PersonalParseResult]]:
#     data: dict[str, list[dict]] = json.load(open("test/test_data/test_personal_parse_results.json", "r", encoding="utf-8"))
#     result = {}

#     for key, value in data.items():
#         result[key] = [PersonalParseResult.model_validate(el) for el in value]

#     return result
