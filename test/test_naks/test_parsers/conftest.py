import pytest
import json

from utils.naks.naks_parsers._types import PersonalMainPageData


@pytest.fixture
def personal_main_page_data() -> dict[str, list[PersonalMainPageData]]:
    data: dict[str, list[dict]] = json.load(open("test/test_data/test_personal_main_page_data.json", "r", encoding="utf-8"))
    result = {}

    for key, value in data.items():
        result[key] = [PersonalMainPageData.model_validate(el) for el in value]

    return result
