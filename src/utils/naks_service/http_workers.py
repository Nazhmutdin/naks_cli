import typing as t
from re import fullmatch

from requests import Session, Response

from errors import BadResponseError


__all__: list[str] = [
    "PersonalNaksHTTPWorker"
]


class PersonalNaksHTTPWorker:
    def __init__(self) -> None:
        self.session = Session()
        self.base_url = "https://naks.ru/registry/personal/"

        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://naks.ru',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        }


    def get_main_page(self, search_value: str) -> Response | t.NoReturn:
        data = self._get_request_data(search_value)
        response = self.session.get(self.base_url, data=data)

        if response.status_code in [200, 201]:
            return response
        else:
            raise BadResponseError(f"bad status code: {response.status_code}")


    def get_additional_page(self, id: str) -> str: ...


    def _detect_search_value_type(self, search_value: str) -> t.Literal["kleymo", "name", "certification_number"]:
        if fullmatch(r"[0-9A-Z]{4}", search_value):
            return "kleymo"
        
        elif fullmatch(r"[А-Я]+-[А-Я0-9]+-[IV]+-[0-9]+", search_value): 
            return "certification_number"
        
        else:
            return "name"
        

    def _get_request_data(self, search_value: str) -> str:
        value_type = self._detect_search_value_type(search_value)
        base_data = """arrFilter_pf%5Bap%5D=&arrFilter_ff%5BNAME%5D={name}&arrFilter_pf%5Bshifr_ac{cert_abbr}%5D=&arrFilter_pf%5Buroven_ac%5D={cert_lvl}&arrFilter_pf%5Bnum_ac%5D={cert_number}&arrFilter_ff%5BCODE%5D={kleymo}&arrFilter_DATE_CREATE_1=&arrFilter_DATE_CREATE_2=&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_DATE_ACTIVE_FROM_1=&arrFilter_DATE_ACTIVE_FROM_2=&g-recaptcha-response=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter="""
        
        data_options = {
            "name": "",
            "kleymo": "",
            "cert_abbr": "",
            "cert_lvl": "",
            "cert_number": ""
        }
        
        match value_type:
            case "name":
                data_options['name'] = search_value
                return base_data.format(**data_options).strip()
            
            case "kleymo":
                data_options['kleymo'] = search_value
                return base_data.format(**data_options).strip()
            
            case "certification_number":
                data_options['cert_abbr'] = f"{search_value.split("-")[0]}-{search_value.split("-")[1]}"
                data_options['cert_lvl'] = search_value.split("-")[2]
                data_options['cert_number'] = search_value.split("-")[3]
                return base_data.format(**data_options).strip()
