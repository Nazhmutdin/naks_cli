from typing import Any
from queue import Queue

from rich.progress import Progress, TaskID


class ProgressQueue(Queue):

    def __init__(self, progress: Progress | None, task: TaskID | None, maxsize: int = 0) -> None:

        self.progress = progress
        self.task = task

        super().__init__(maxsize)

    
    def get(self, block: bool = True, timeout: float | None = None) -> Any:
        if self.progress:
            self.progress.update(task_id=self.task, advance=1)
            
        return super().get(block, timeout)