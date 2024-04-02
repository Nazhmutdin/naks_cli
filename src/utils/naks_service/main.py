import typing as t

from shemas import *
from _types import AnyType
from naks_service._types import NaksPersonResult
from http_workers import PersonalNaksHTTPWorker
from extractors import PersonalNaksExtractor


__all__: list[str] = [
    "PersonalNaksParser"
]



class PersonalNaksParser:
    def __init__(self) -> None:
        self.extractor = PersonalNaksExtractor()
        self.http_worker = PersonalNaksHTTPWorker()


    def parse(self, search_values: list[str | AnyType]) -> list[NaksPersonResult]:
        result = []

        for search_value in search_values:
            main_page_res = self.http_worker.get_main_page(search_value)
