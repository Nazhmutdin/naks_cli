import typing as t
from abc import ABC, abstractmethod

from lxml import html

from utils.naks_service.naks_parsers._types import PersonalMainPageData, PersonalAdditionalPageData


type NaksTableRow = html.HtmlElement


class BaseNaksExtractor(ABC):

    @abstractmethod
    def parse_main_page(self, main_page: str) -> t.Any: ...


    @abstractmethod
    def parse_additional_page(self, additional_page: str) -> t.Any: ...


    def get_id(self, row: NaksTableRow) -> str:
        onclick_data = row.xpath("//*[@data-toggle]/@onclick")

        print(onclick_data)



    def _get_tree(self, page_content: str) -> html:
        return html.fromstring(page_content)
    

    def _to_string(self, html_obj: html.HtmlElement) -> str:
        return html.tostring(html_obj)



class PersonalNaksExtractor(BaseNaksExtractor):
    def parse_main_page(self, main_page: str) -> list[PersonalMainPageData]: ...

    
    def parse_additional_page(self, additional_page: str) -> t.Any: ...
