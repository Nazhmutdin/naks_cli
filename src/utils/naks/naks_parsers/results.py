from pydantic import BaseModel



class BaseParseResult(BaseModel): 
    ...


class ParsePersonalResult(BaseParseResult):
    ...


class ParseACSTResult(BaseParseResult):
    ...


class ParseACSOResult(BaseParseResult):
    ...


class ParseACSMResult(BaseParseResult):
    ...