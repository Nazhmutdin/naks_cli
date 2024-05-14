import typing as t
from json import load
from re import fullmatch

from requests import Session, Response

from errors import BadResponseError
from settings import Settings


__all__: list[str] = [
    "BaseNaksHTTPWorker",
    "PersonalNaksHTTPWorker"
]


class BaseNaksHTTPWorker(t.Protocol):

    def get_main_page(self, search_value: str) -> Response: ...


    def get_additional_page(self, ident: str) -> Response: ...


class PersonalNaksHTTPWorker:
    def __init__(self) -> None:
        self._session = Session()
        self.base_url = "https://naks.ru/registry/personal/"

        self.request_data: dict[str, dict[str, str]] = load(open(f"{Settings.BASE_DIR()}\\static\\data\\personal_naks_parser_data.json", "r", encoding="utf-8"))

        self._session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://naks.ru',
            'Referer': 'https://naks.ru/registry/personal/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }


    def get_main_page(self, search_value: str) -> Response:
        data = self._get_request_data(search_value)
        response = self._session.post(self.base_url, data=data)

        if response.status_code in [200, 201]:
            return response
        else:
            raise BadResponseError(f"bad status code: {response.status_code}")


    def get_additional_page(self, ident: str) -> Response:
        url = f"{self.base_url}/detail.php?ID={ident}"
        response = self._session.get(f"{url}")

        if response.status_code in [200, 201]:
            return response
        else:
            raise BadResponseError(f"bad status code: {response.status_code}")


    def _detect_search_value_type(self, search_value: str) -> t.Literal["kleymo", "name", "certification_number"]:
        if fullmatch(r"[0-9A-Z]{4}", search_value):
            return "kleymo"
        
        elif fullmatch(r"[А-Я]+-[А-Я0-9]+-[IV]+-[0-9]+", search_value): 
            return "certification_number"
        
        else:
            return "name"


    def _get_request_data(self, search_value: str, page: int = 1) -> str:
        value_type = self._detect_search_value_type(search_value)
        base_data = "PAGEN_1={page}&arrFilter_pf%5Bap%5D=&arrFilter_ff%5BNAME%5D={name}&arrFilter_pf%5Bshifr_ac%5D={cert_abbr}&arrFilter_pf%5Buroven_ac%5D={cert_lvl}&arrFilter_pf%5Bnum_ac%5D={cert_number}&arrFilter_ff%5BCODE%5D={kleymo}&arrFilter_DATE_CREATE_1=&arrFilter_DATE_CREATE_2=&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_DATE_ACTIVE_FROM_1=&arrFilter_DATE_ACTIVE_FROM_2=&g-recaptcha-response=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y"
        
        data_options = {
            "page": page,
            "name": "",
            "kleymo": "",
            "cert_abbr": "",
            "cert_lvl": "",
            "cert_number": ""
        }
        
        match value_type:
            case "name":
                data_options['name'] = repr(search_value.encode("windows-1251"))[2:-1].replace("\\x", "%").upper().replace(" ", "+")
                return base_data.format(**data_options).strip()
            
            case "kleymo":
                data_options['kleymo'] = search_value
                return base_data.format(**data_options).strip()
            
            case "certification_number":
                data_options['cert_abbr'] = self.request_data["attestation_codes"].get("-".join(search_value.split("-")[:2]))
                data_options['cert_lvl'] = self.request_data["attestations_lvl_codes"].get(search_value.split("-")[2])
                data_options['cert_number'] = search_value.split("-")[3]
                return base_data.format(**data_options).strip()
