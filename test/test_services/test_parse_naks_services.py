import pytest

from services.naks.parse_services import ParsePersonalService

class TestParsePersonalService:

    @pytest.mark.parametrize(
        "value, count",
        [
            (["0324"], 10),
            (["BKMH"], 2),
            (["0324", "BKMH"], 12)
        ]
    )
    def test_parse(self, value: list[str | int] | str | int, count: int) -> None:
        service = ParsePersonalService()

        res = service.parse(value)

        assert len(res) == count