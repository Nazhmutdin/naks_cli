import pytest

from utils.naks.naks_parsers.http_workers import PersonalNaksHTTPWorker
from utils.naks.naks_parsers.extractors import PersonalNaksExtractor


class TestPersonalNaksExtractor:

    @pytest.mark.parametrize(
            "search_value",
            [
                "0324", "Кая Мехмет Коджа", "Шйам Шарма", "9H88"
            ]
    )
    @pytest.mark.usefixtures("personal_main_page_data")
    def test_parse_main_page(self, search_value: str, personal_main_page_data):
        http_worker = PersonalNaksHTTPWorker()
        extractor = PersonalNaksExtractor()

        page = http_worker.get_main_page(search_value)

        result = extractor.parse_main_page(page.text)

        assert len(result) == len(personal_main_page_data[search_value])

        assert result == personal_main_page_data[search_value]
