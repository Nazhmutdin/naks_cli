import pytest
from lxml import html

from utils.naks_service.naks_parsers.http_workers import PersonalNaksHTTPWorker


class TestPersonalNaksHTTPWorker:
    worker = PersonalNaksHTTPWorker()

    @pytest.mark.parametrize(
        "search_value, amount",
        [
            ("0324", 10),
            ("9H88", 10),
            ("ЮР-9АЦ-I-03551", 1),
            ("ЮР-9АЦ-I-07619", 4),
            ("Мырадов Айдогды", 2),
        ]
    )
    def test_get_main_page(self, search_value: str, amount: int):
        response = self.worker.get_main_page(search_value)
        tree = html.fromstring(response.text)

        assert len(tree.xpath("//table[@class='tabl']/tr[@bgcolor]")) == amount


    @pytest.mark.parametrize(
        "data_id",
        [
            "YTo0OntzOjM6ImZpbyI7czoxNjoizPvw4OTu4iDA6eTu4+T7ICI7czo5OiJ1ZG9zdF9udW0iO3M6MTQ6It7QLTnA1i1JLTExNzc2IjtzOjEwOiJ1ZG9zdF9kYXRlIjtzOjEwOiIyNi4xMi4yMDIzIjtzOjQ6InR5cGUiO3M6MDoiIjt9",
            "YTo0OntzOjM6ImZpbyI7czoxMToi2Ong7CDY4PDs4CAiO3M6OToidWRvc3RfbnVtIjtzOjE1OiLSztAtNsDWLUktMDg3MzUiO3M6MTA6InVkb3N0X2RhdGUiO3M6MTA6IjI1LjA4LjIwMjMiO3M6NDoidHlwZSI7czoyOiLCMSI7fQ==",
            "YTo0OntzOjM6ImZpbyI7czoxNzoi0ejt4/Ug0ODsINfg7eTw4CAiO3M6OToidWRvc3RfbnVtIjtzOjE1OiLe0C0zw8DWLUktMjM4NTgiO3M6MTA6InVkb3N0X2RhdGUiO3M6MTA6IjA5LjEwLjIwMjMiO3M6NDoidHlwZSI7czowOiIiO30="
        ]
    )
    def test_get_additional_page(self, data_id: str):
        response = self.worker.get_additional_page(data_id)
        tree = html.fromstring(response.text)

        assert len(tree.xpath("//table")) >= 2


    @pytest.mark.parametrize(
            "search_value, result",
            [
                ("0324", "kleymo"),
                ("ASDF", "kleymo"),
                ("ЮР-9АЦ-I-07620", "certification_number"),
                ("ТОР-6АЦ-I-08958", "certification_number"),
                ("dfasrvfdv avsrf", "name"),
            ]
    )
    def test_detect_search_value_type(self, search_value: str, result: str):
        res = self.worker._detect_search_value_type(search_value)

        assert res == result