import pytest
import json

from utils.naks.parsers._types import PersonalMainPageData, PersonalAdditionalPageData
from utils.naks.parsers.results import PersonalParseResult


@pytest.fixture
def personal_main_page_data() -> dict[str, list[PersonalMainPageData]]:
    data: dict[str, list[dict]] = json.load(open("test/test_data/test_personal_main_page_data.json", "r", encoding="utf-8"))
    result = {}

    for key, value in data.items():
        result[key] = [PersonalMainPageData.model_validate(el) for el in value]

    return result


@pytest.fixture
def personal_additional_page_data() -> dict[str, list[PersonalAdditionalPageData]]:
    data: dict[str, list[dict]] = json.load(open("test/test_data/test_personal_additional_page_data.json", "r", encoding="utf-8"))
    result = {}

    for key, value in data.items():
        result[key] = PersonalAdditionalPageData.model_validate(value)

    return result


@pytest.fixture
def personal_parse_results() -> dict[str, list[PersonalParseResult]]:
    data: dict[str, list[dict]] = json.load(open("test/test_data/test_personal_parse_results.json", "r", encoding="utf-8"))
    result = {}

    for key, value in data.items():
        result[key] = [PersonalParseResult.model_validate(el) for el in value]

    return result
