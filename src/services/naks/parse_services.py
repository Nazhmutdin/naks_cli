import typing as t
from time import sleep 
from threading import Thread
from queue import Queue

from rich.progress import *

from utils.naks.parsers.results import BaseParseResult, PersonalParseResult
from utils.naks.parsers.parsers import BaseNaksParser, PersonalNaksParser
from utils.utils import ProgressQueue
from settings import Settings


class IParseNaksService[Result: BaseParseResult](t.Protocol):
    __parser__: type[BaseNaksParser]

    def parse(self, values: list[t.Any], k: int = 1) -> list[Result]:

        progress, task = self._dump_progress_and_task_id(len(values))

        src_queue = ProgressQueue(task=task, progress=progress)
        result_queue = Queue()

        for value in values:
            src_queue.put(value)

        threads: list[Thread] = []

        for _ in range(k):
            thread = Thread(target=self._execute, args=(src_queue, result_queue,))
            thread.start()

            threads.append(thread)

        for thread in threads:
            thread.join()

        sleep(.1)

        result: list[Result] = []

        for _ in range(result_queue.qsize()):
            result += list(result_queue.get().values())[0]

        return result


    def _dump_progress_and_task_id(self, total: int) -> tuple[Progress | None, TaskID | None]:
        if Settings.MODE() == "TEST":
            return None, None

        progress_columns = (
            "[blue]Processing...", 
            BarColumn(), 
            TaskProgressColumn(),
            "[blue]processed: ",
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            "/",
            TimeRemainingColumn()
        )
        progress = Progress(*progress_columns)
        progress.start()
        task = progress.add_task("[blue]Processing", total=total)

        return progress, task


    def _execute(self, src_queue: Queue, result_queue: Queue) -> None:
        parser = self.__parser__()

        while not src_queue.empty():
            value = src_queue.get_nowait()

            result_queue.put(
                {
                    value: parser.parse(value)
                }
            )


class ParsePersonalService(IParseNaksService[PersonalParseResult]):
    __parser__ = PersonalNaksParser
        