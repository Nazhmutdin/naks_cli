from typing import Protocol


class INaksParser[T, K](Protocol):

    def parse(self, search_items: list[T]) -> list[K]: ...
