from abc import ABC, abstractmethod
from re import search

from lxml import html


class BaseNaksExtractor(ABC):

    @abstractmethod
    def parse_main_page(self, main_page: str): ...


    @abstractmethod
    def parse_additional_page(self, additional_page: str): ...


    def _get_additional_page_id(self, tr_tree: html.HtmlElement) -> str:
        result = tr_tree.xpath("//td[13]/a/@onclick")[0]

        ident = search(r"\?ID=[\W\w]+\"", result).group()

        return ident.split("ID=")[1].replace("\"", "").split(",")[0]


    def _get_tree(self, page_content: str) -> html.HtmlElement:
        return html.fromstring(page_content)


    def _to_string(self, html_obj: html.HtmlElement) -> str:
        return html.tostring(html_obj)
