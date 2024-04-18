from abc import ABC, abstractmethod

from results import BaseParseResult, ParsePersonalResult


class BaseNaksParser(ABC):

    @abstractmethod
    def parse(self, *search_values) -> BaseParseResult: ... 


class BaseNaksParser(BaseNaksParser):

    def parse(self, *search_values) -> ParsePersonalResult: ... 