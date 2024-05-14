from utils.naks.parsers.http_workers import *
from utils.naks.parsers.extractors import *
from utils.naks.parsers.results import *


class BaseNaksParser[Result: BaseParseResult]:
    http_worker: BaseNaksHTTPWorker = NotImplemented
    extractor: BaseNaksExtractor = NotImplemented
    __result_type__: type[BaseParseResult] = NotImplemented

    def parse(self, *search_values) -> list[Result]:
        result = []

        for search_value in search_values:
            main_page_response = self.http_worker.get_main_page(search_value)
            main_page_data = self.extractor.parse_main_page(main_page_response.text)

            for el in main_page_data:
                additional_page_response = self.http_worker.get_additional_page(el.additional_page_id)
                additional_page_data = self.extractor.parse_additional_page(additional_page_response.text)

                result.append(
                    self.__result_type__.model_validate(el.model_dump() | additional_page_data.model_dump())
                )
        
        return result


class PersonalNaksParser(BaseNaksParser[PersonalParseResult]):
    http_worker = PersonalNaksHTTPWorker()
    extractor = PersonalNaksExtractor()
    __result_type__ = PersonalParseResult
