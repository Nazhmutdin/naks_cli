from queue import Queue

from rich.progress import Progress, TaskID


class TypedQueue[T](Queue):

    def get(self, block: bool = True, timeout: float | None = None) -> T:
        res = super().get(block, timeout)

        return res


    def get_nowait(self) -> T:
        res = super().get_nowait()

        return res

    
    def put(self, item: T, block: bool = True, timeout: float | None = None) -> None:
        return super().put(item, block, timeout)
    

    def put_nowait(self, item: T) -> None:
        return super().put_nowait(item)


class ProgressQueue[T](TypedQueue[T]):

    def __init__(self, progress: Progress | None, task: TaskID | None, maxsize: int = 0) -> None:

        self.progress = progress
        self.task = task

        super().__init__(maxsize)

    
    def get(self, block: bool = True, timeout: float | None = None):
        if self.progress:
            self.progress.update(task_id=self.task, advance=1)
            
        return super().get(block, timeout)


class StoreQueue[T](TypedQueue[T]): ...
    