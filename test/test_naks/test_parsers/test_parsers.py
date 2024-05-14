import pytest

from utils.naks.parsers import *


class TestPersonalNaksParser:

    @pytest.mark.usefixtures("personal_parse_results")
    def test_parse(self, personal_parse_results: dict[str, list]):
        parser = PersonalNaksParser()

        for key, value in personal_parse_results.items():

            result = parser.parse(key)

            assert result == value
