import typing as t

from sqlalchemy import event

from db_engine import get_session
from repositories import SQLAlchemyRepository


class IUnitOfWork[Repository: SQLAlchemyRepository](t.Protocol):
    def __init__(self, repository: type[Repository]) -> None: ...

    
    def __enter__(self) -> None: ...


    def __exit__(self, *args) -> None: ...


    def commit(self) -> None: ...


    def rollback(self) -> None: ...


class UnitOfWork[Repository: SQLAlchemyRepository]:
    def __init__(self, repository_type: type[Repository]) -> None:
        self.repository_type = repository_type
    

    def __enter__(self) -> t.Self:
        self.session = get_session()
        self.repository = self.repository_type(self.session)

        return self


    def __exit__(self, *args) -> None:
        self.rollback()
        self.session.close()


    def commit(self) -> None:
        self.session.commit()


    def rollback(self) -> None:
        self.session.rollback()


class SQLalchemyUnitOfWork:
    def __enter__(self):
        self.session = get_session()
        self.connection = self.session.connection()
        self.engine = self.connection.engine
        self.count = 0

        event.listen(self.engine, "before_cursor_execute", self.callback)

        return self


    def __exit__(self, *args):
        self.session.close()
        # print(f"Execution_amount: {self.count}")
        event.remove(self.engine, "before_cursor_execute", self.callback)

    
    def commit(self) -> None:
        self.session.commit()


    def rollback(self) -> None:
        self.session.rollback()


    def callback(self, *args, **kwargs) -> None:
        self.count += 1
