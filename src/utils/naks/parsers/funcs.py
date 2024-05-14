import re
from typing import Iterator

from utils.funcs import get_gtd_description_short_dict


def parse_gtds(string: str) -> Iterator[list[str] | None]:
    strings = re.split(r"\),|\);", string)

    gtd_data = get_gtd_description_short_dict()

    for el in strings:
        description, subgroups = el.split(" (")
        gtd_short = gtd_data.get(description.strip())

        if not gtd_short:
            yield None
    
        subgroups: list[int] = [int(el.strip()) for el in re.findall(r"[0-9]+", subgroups)]

        yield [f"{gtd_short}({el})" for el in subgroups]


def parse_list_data(string: str | None) -> list[str] | None:
    if not string:
        return None

    string = re.sub(r"\[[\w\W]+\]", "", string)

    return [el.strip() for el in re.split(r",|;", string)]


def parse_from_values(string: str | None) -> list[int | float] | None:
    if not string:
        return None
    
    from_pattern = re.compile(r"от [0-9]+[.,][0-9]+|от [0-9]+|свыше [0-9]+[.,][0-9]+|Свыше [0-9]+[.,][0-9]+|свыше [0-9]+|Свыше [0-9]+")

    from_values = from_pattern.findall(string)

    return [
        float(
            el.replace(",", ".").replace("от ", "").replace("свыше ", "").replace("Свыше ", "").strip()
            ) for el in from_values
    ] if from_values != [] else None
    

def parse_before_values(string: str | None) -> list[int | float] | None:
    if not string:
        return None
    
    before_pattern= re.compile(r"до [0-9]+[.,][0-9]+|до [0-9]+|До [0-9]+[.,][0-9]+|До [0-9]+")

    before_values = before_pattern.findall(string)

    return [
        float(
            el.replace(",", ".").replace("до ", "").replace("До ", "").strip()
            ) for el in before_values
    ] if before_values != [] else None


def get_from_value_or_none(string: str | None) -> int | float | None:
    
    from_values = parse_from_values(string)

    if not from_values:
        return None

    return min(from_values)


def get_before_value_or_none(string: str | None) -> int | float | None:
    
    before_values = parse_before_values(string)

    if not before_values:
        return None

    return max(before_values)
