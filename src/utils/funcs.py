from string import digits, ascii_letters
from json import dump, load
from random import choices
from pathlib import Path
import typing as t

from src.config import ApplicationConfig


def gen_random_string(k: int = 1) -> str:

    return "".join(choices(digits + ascii_letters, k=k))


def save_json(data: list | dict, path: str | Path, indent: int = 4, ensure_ascii: bool = False) -> None:
    with open(path, "w", encoding="utf-8") as file:
        dump(data, file, indent=indent, ensure_ascii=ensure_ascii)
        file.close()
    

def read_json(path: str | Path) -> list | dict | t.Any:
    return load(open(path, "r", encoding="utf-8"))


def gtd_data_json() -> dict[str, dict[str, str | dict]]:
    return load(open(f"{ApplicationConfig.BASE_DIR()}/static/data/gtd_data.json", "r", encoding="utf-8"))


def gtd_description_short_dict(gtd_data: dict[str, dict[str, str | dict]] = gtd_data_json()) -> dict[str, str]:

    return {value["description"]: key  for key, value in gtd_data.items()}
