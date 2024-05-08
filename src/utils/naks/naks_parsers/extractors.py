import typing as t
from abc import ABC, abstractmethod
from re import search

from lxml import html

from utils.naks.naks_parsers._types import PersonalMainPageData, PersonalAdditionalPageData


type NaksTableRow = html.HtmlElement


class BaseNaksExtractor(ABC):

    @abstractmethod
    def parse_main_page(self, main_page: str) -> t.Any: ...


    @abstractmethod
    def parse_additional_page(self, additional_page: str) -> t.Any: ...
    

    def _get_additional_page_id(self, tr_tree: html.HtmlElement) -> str:
        result = tr_tree.xpath("//td[13]/a/@onclick")[0]

        ident = search(r"\?ID=[\W\w]+\"", result).group()

        return ident.split("ID=")[1].replace("\"", "").split(",")[0]


    def get_pages_amount(self, main_page: str) -> int:
        tree = self._get_tree(main_page)

        res = tree.xpath("(//div[@class='table-responsive table-fit-content']//a[contains(text(),'Конец' )])[1]/@href")

        return int(res.split("PAGEN_1=")[1].split("#")[0])
 

    def _get_tree(self, page_content: str) -> html.HtmlElement:
        return html.fromstring(page_content)
    

    def _to_string(self, html_obj: html.HtmlElement) -> str:
        return html.tostring(html_obj)



class PersonalNaksExtractor(BaseNaksExtractor):
    def parse_main_page(self, main_page: str) -> list[PersonalMainPageData]:
        tree = self._get_tree(main_page)
        result = []

        trs: list[html.HtmlElement] = tree.xpath("//table[@class='tabl']//tr[@bgcolor]")

        for tr in trs:
            tr_tree = self._get_tree(self._to_string(tr))
            result.append(
                PersonalMainPageData(
                    kleymo=self._get_kleymo(tr_tree),
                    name=self._get_name(tr_tree),
                    company=self._get_company(tr_tree),
                    job_title=self._get_job_title(tr_tree),
                    certification_number=self._get_certification_number(tr_tree),
                    insert=self._get_insert(tr_tree),
                    certification_date=self._get_certification_date(tr_tree),
                    expiration_date=self._get_expiration_date(tr_tree),
                    expiration_date_fact=self._get_expiration_date_fact(tr_tree),
                    method=self._get_method(tr_tree),
                    additional_page_id=self._get_additional_page_id(tr_tree)
                )
            )
        
        return result


    def parse_additional_page(self, additional_page: str) -> PersonalAdditionalPageData: ...

    
    def _get_name(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[1]/text()")[0].strip()
    

    def _get_kleymo(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[2]/span/text()")[0].strip()
    

    def _get_company(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[3]/text()")[0].split(",")[0].strip()
    

    def _get_job_title(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[4]/text()")[0].strip()
    

    def _get_certification_number(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[5]/text()")[0].strip()
    

    def _get_insert(self, tr_tree: html.HtmlElement) -> str | None:

        result = tr_tree.xpath("//td[6]/text()")[0].strip()

        if not result:
            return None
        
        return result
    

    def _get_certification_date(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[9]/text()")[0].strip()
    

    def _get_expiration_date(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[10]/text()")[0].strip()
    

    def _get_expiration_date_fact(self, tr_tree: html.HtmlElement) -> str:

        exp_fact = tr_tree.xpath("//td[11]/text()")[0].strip()

        if exp_fact:
            return exp_fact
        
        return self._get_expiration_date(tr_tree)
    

    def _get_method(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[12]/text()")[0].strip()
