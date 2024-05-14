import pytest
import json

from utils.naks.parsers.http_workers import PersonalNaksHTTPWorker
from utils.naks.parsers.extractors import PersonalNaksExtractor


class TestPersonalNaksExtractor:
    @pytest.mark.usefixtures("personal_main_page_data")
    def test_parse_main_page(self, personal_main_page_data: dict[str, list]):
        http_worker = PersonalNaksHTTPWorker()
        extractor = PersonalNaksExtractor()

        for key, value in personal_main_page_data.items():

            page = http_worker.get_main_page(key)

            result = extractor.parse_main_page(page.text)

            assert len(result) == len(value)

            assert result == value


    @pytest.mark.usefixtures("personal_additional_page_data")
    def test_parse_additional_page(self, personal_additional_page_data: dict[str, dict]):
        http_worker = PersonalNaksHTTPWorker()
        extractor = PersonalNaksExtractor()

        for key, value in personal_additional_page_data.items():
 
            page = http_worker.get_additional_page(key)

            result = extractor.parse_additional_page(page.text)

            assert result == value
