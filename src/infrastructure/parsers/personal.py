from dataclasses import dataclass
from time import sleep

from requests import Response, Session
from pydantic import ValidationError
from lxml import html

from src.application.common.exc import BadResponseError
from src.infrastructure.parsers.base import BaseNaksExtractor
from src.infrastructure.dto import PersonalNaksCertificationData, SearchNaksCertificationItem


@dataclass
class PersonalNaksCertificationMainPageData:
    name: str
    company: str
    certification_number: str
    certification_date: str
    expiration_date: str
    expiration_date_fact: str
    additional_page_id: str
    kleymo: str | None = None
    insert: str | None = None
    method: str | None = None


@dataclass
class PersonalNaksCertificationAdditionalPageData:
    gtd: str
    html: str
    detail_types: str | None = None
    joint_types: str | None = None
    materials: str | None = None
    detail_thikness_string: str | None = None
    outer_diameter_string: str | None = None
    rod_diameter_string: str | None = None
    detail_diameter_string: str | None = None


class PersonalNaksCertificationHttpWorker:
    def __init__(self) -> None:
        self.base_url = "https://naks.ru/registry/personal/"

        self.session = Session()

        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://naks.ru',
            'Referer': 'https://naks.ru/registry/personal/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
        }


    def get_main_page(self, search_item: SearchNaksCertificationItem) -> Response:
        data = self._get_request_data(search_item)

        with self.session.post(self.base_url, data=data, timeout=5) as response:
            if response.status_code in [200, 201]:
                return response
            else:
                raise BadResponseError(f"bad status code: {response.status_code} ({response.content})")


    def get_additional_page(self, key: str) -> Response: 
        url = f"{self.base_url}/detail.php?ID={key}"

        with self.session.get(url, timeout=5) as response:

            if response.status_code in [200, 201]:
                return response
            else:
                raise BadResponseError(f"bad status code: {response.status_code} ({response.content})")

    
    def _get_request_data(self, search_settings: SearchNaksCertificationItem, page: int = 1) -> str:
        base_data = "PAGEN_1={page}&arrFilter_pf%5Bap%5D=&arrFilter_ff%5BNAME%5D={name}&arrFilter_pf%5Bshifr_ac%5D={cert_abbr}&arrFilter_pf%5Buroven_ac%5D={cert_lvl}&arrFilter_pf%5Bnum_ac%5D={cert_number}&arrFilter_ff%5BCODE%5D={kleymo}&arrFilter_DATE_CREATE_1=&arrFilter_DATE_CREATE_2=&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_DATE_ACTIVE_FROM_1=&arrFilter_DATE_ACTIVE_FROM_2=&g-recaptcha-response=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y"
        
        data_options = {
            "page": page,
            "name": search_settings.name,
            "kleymo": search_settings.kleymo,
            "cert_abbr": search_settings.cert_abbr,
            "cert_lvl": search_settings.cert_lvl,
            "cert_number": search_settings.cert_number
        }
        
        return base_data.format(**data_options).strip()


class PersonalNaksCertificationExtractor(BaseNaksExtractor):
    def parse_main_page(self, main_page: str) -> list[PersonalNaksCertificationMainPageData]:
        tree = self._get_tree(main_page)
        result = []

        trs: list[html.HtmlElement] = tree.xpath("//table[@class='tabl']//tr[@bgcolor]")

        for tr in trs:
            tr_tree = self._get_tree(self._to_string(tr))
            result.append(
                PersonalNaksCertificationMainPageData(
                    kleymo=self._get_kleymo(tr_tree),
                    name=self._get_name(tr_tree),
                    company=self._get_company(tr_tree),
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


    def parse_additional_page(self, additional_page: str) -> PersonalNaksCertificationAdditionalPageData:
        tree = self._get_tree(additional_page)
        result = {}

        for tr in tree.xpath("//tr"):
            tr_tree = self._get_tree(self._to_string(tr))

            tds = tr_tree.xpath("//td")

            if len(tds) < 2:
                continue

            key = tds[0].text.strip()
            value = " | ".join(td.text_content().strip() for td in tds[1:])

            result[key] = value
        

        gtd = result.get("Группы технических устройств опасных производственных объектов:", "")

        if gtd == "":
            html = ""
        else:
            html = self._to_string(tree.xpath("//div[@class='modal-body']")[0]).replace(b"\n", b"").replace(b"\r", b"").replace(b"\t", b"").replace(b"\"", b"'")


        return PersonalNaksCertificationAdditionalPageData(
            gtd=gtd,
            detail_types=result.get("Вид деталей"),
            joint_types=result.get("Типы швов"),
            materials=result.get("Группа свариваемого материала"),
            detail_thikness_string=result.get("Толщина деталей, мм"),
            outer_diameter_string=result.get("Наружный диаметр, мм"),
            rod_diameter_string=result.get("Диаметр стержня, мм"),
            detail_diameter_string=result.get("Диаметр деталей, мм"),
            html=html
        )


    def _get_name(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[1]/text()")[0].strip()
    

    def _get_kleymo(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[2]/span/text()")[0].strip()
    

    def _get_company(self, tr_tree: html.HtmlElement) -> str:

        return tr_tree.xpath("//td[3]/text()")[0].split(",")[0].strip()
    

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


class PersonalNaksCertificationParser:

    def __init__(self) -> None:
        self.http_worker = PersonalNaksCertificationHttpWorker()
        self.extractor = PersonalNaksCertificationExtractor()


    def parse(self, search_item: SearchNaksCertificationItem) -> list[PersonalNaksCertificationData]:
        result: list[PersonalNaksCertificationData] = []
        main_page_response = self.http_worker.get_main_page(search_item)
        sleep(3)

        for main_cert_data in self.extractor.parse_main_page(main_page_response.text):
            sleep(1)
            additional_page_response = self.http_worker.get_additional_page(main_cert_data.additional_page_id)
            additional_page_data = self.extractor.parse_additional_page(additional_page_response.text)

            try:
                result.append(
                    PersonalNaksCertificationData.model_validate(main_cert_data.__dict__ | additional_page_data.__dict__)
                )
            except ValidationError as e:
                print(e)
                continue

        return result     
