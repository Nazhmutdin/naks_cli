from click import ClickException


class BadResponseError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class DataNotFoundException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class BadOptionsError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class InvalidDateException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


"""
=========================================================================
Command Exeptions
=========================================================================
"""


class BaseCommandExeption(ClickException):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class UpdateCommandExeption(BaseCommandExeption):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
    

class AddCommandExeption(BaseCommandExeption):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class GetCommandExeption(BaseCommandExeption):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class GetManyCommandExeption(BaseCommandExeption):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class DeleteCommandExeption(BaseCommandExeption):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class NaksCommandExeption(BaseCommandExeption):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


"""
=========================================================================
Reporitory Exeptions
=========================================================================
"""


class DBException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


"""
=========================================================================
Shema Exeptions
=========================================================================
"""


class FieldValidationException(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
