from pathlib import Path

from src.utils.funcs import read_json, save_json
from click import Command, Option, group
from dishka import FromDishka

from src.application.interactors import ParsePersonalNaksCertificationsInteractor
from src.infrastructure.dto import SearchNaksCertificationItem, PersonalNaksCertificationData
from src.presentation.cli_types import OptionalPath
from src.config import ApplicationConfig


class PersonalNaksCertificationsCommand(Command): 
    def __init__(self):
        name = "personal-naks-certs"

        params= [
            Option(["--search-items-path", "-sip"], type=OptionalPath(), help="path to json file"),
            Option(["--threads", "-th"], type=int, default=1, show_default=True, help="threads amount"),
            Option(["--save-file-name", "-sfn"], type=str)
        ]

        super().__init__(
            name=name,
            params=params,
            callback=self.execute
        )

    
    def execute(self, 
        search_items_path: Path | None, 
        threads: int,
        save_file_name: str,
        parse: FromDishka[ParsePersonalNaksCertificationsInteractor]
    ):
        if search_items_path:
            search_values  = self.load_search_values_file_data(search_items_path)
        else:
            search_values = self.load_default_search_values_file_data()

        parse_result = parse(search_values, threads)

        self.save_search_result(parse_result, save_file_name)

    
    def load_search_values_file_data(self, path: Path) -> list[SearchNaksCertificationItem]:
        content: list[dict] = read_json(path)

        return [SearchNaksCertificationItem(**i) for i in content]

    
    def load_default_search_values_file_data(self) -> list[SearchNaksCertificationItem]:
        content: list[dict] = read_json(ApplicationConfig.SEARCH_VALUES_JSON_PATH())

        return [SearchNaksCertificationItem(**i) for i in content]

    
    def save_search_result(self, data: list[PersonalNaksCertificationData], save_file_name: str) -> list[SearchNaksCertificationItem]:
        data = [el.model_dump(mode="json") for el in data]
        
        save_json(data, ApplicationConfig.SAVES_DIR() / f"{save_file_name}.json")


@group("parse")
def parse_group(): ...


parse_group.add_command(PersonalNaksCertificationsCommand())
