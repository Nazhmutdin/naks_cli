from threading import Thread, active_count
from time import sleep

from rich.progress import (
    Progress, 
    BarColumn, 
    ProgressColumn,
    Task,
    TaskProgressColumn, 
    MofNCompleteColumn, 
    TimeElapsedColumn, 
    TimeRemainingColumn, 
    TaskID
)
from rich.text import Text
from rich.table import Column

from src.application.interfaces.naks_parser import INaksParser
from src.infrastructure.dto import SearchNaksCertificationItem, PersonalNaksCertificationData
from src.infrastructure.parsers.personal import PersonalNaksCertificationParser
from src.utils.queue import ProgressQueue, StoreQueue
from src.config import ApplicationConfig


class ThreadsMountColumn(ProgressColumn):
    def __init__(self, total_threads: int, table_column: Column | None = None) -> None:
        self.total_threads = total_threads
        super().__init__(table_column)

    
    def render(self, task: Task) -> Text:
        return Text(
            f"{active_count() - 2}/{self.total_threads}",
            style="progress.download",
        )


def dump_progress_and_task_id(total: int, total_threads: int) -> tuple[Progress | None, TaskID | None]:
    if ApplicationConfig.MODE() == "TEST":
        return None, None

    progress_columns = (
        "[blue]Processing...", 
        BarColumn(), 
        TaskProgressColumn(),
        "[blue]processed: ",
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        "/",
        TimeRemainingColumn(),
        ThreadsMountColumn(total_threads)
    )
    progress = Progress(*progress_columns)
    progress.start()
    task = progress.add_task("[blue]Parsing", total=total)

    return progress, task


class BaseParseInteractor[T, K]:

    def __call__(self, search_items: list[T], k: int = 1) -> list[K]:
        progress, task_id = dump_progress_and_task_id(total=len(search_items), total_threads=k)

        src_queue: ProgressQueue[T] = ProgressQueue(
            progress=progress,
            task=task_id
        )
        result_queue: StoreQueue[K] = StoreQueue()

        for search_item in search_items:
            src_queue.put(search_item)

        threads: list[Thread] = []

        for _ in range(k):
            thread = Thread(target=self.execute, args=(src_queue, result_queue,))
            thread.start()

            threads.append(thread)

        for thread in threads:
            thread.join()
        
        sleep(.1)

        if progress:
            progress.stop()

        result: list[K] = []

        for _ in range(result_queue.qsize()):
            result += result_queue.get_nowait()

        return result
    

    def execute(self, src_queue: ProgressQueue[T], store_queue: StoreQueue[K]): 
        parser = self._init_parser()

        while not src_queue.empty():
            value = src_queue.get_nowait()

            parse_result = parser.parse(value)

            store_queue.put(parse_result)

    def _init_parser(self) -> INaksParser[T, K]: ...


class ParsePersonalNaksCertificationsInteractor(BaseParseInteractor[SearchNaksCertificationItem, PersonalNaksCertificationData]):

    def _init_parser(self) -> PersonalNaksCertificationParser:
        return PersonalNaksCertificationParser()
