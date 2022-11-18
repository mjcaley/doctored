from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar

T = TypeVar("T")
In = TypeVar("In")
Out = TypeVar("Out")


class IHandler(ABC, Generic[T]):
    @abstractmethod
    def handle(self, item: T):
        """Logic to perform an action on the item.

        If successful, call the `next_handler`'s `handle` method. Otherwise, it can be consumed and processing will stop.

        :param item: T
        """


class Handler(IHandler[In], Generic[In, Out]):
    def __init__(self):
        self._handler = None

    @property
    def next_handler(self) -> Handler[Out] | None:
        return self._handler

    @next_handler.setter
    def next_handler(self, handler: IHandler[Out]):
        self._handler = handler

    def handle(self, item: In):
        raise NotImplementedError


class SinkHandler(Handler[In, None]):
    def __init__(self):
        self._items: list[In] = []
        super().__init__()

    def handle(self, item: In):
        self._items.append(item)

    @property
    def items(self) -> list[In]:
        return self._items


class HandlerCollection(Generic[T]):
    def __init__(self, *handlers: IHandler[Any]):
        self.handlers = list(handlers)
        self._sink: SinkHandler = SinkHandler()
        if self.handlers:
            handlers[-1].next_handler = self._sink
        self.handlers.append(self._sink)

    def handle(self, item: Any) -> list[Any]:
        self.handlers[0].handle(item)

        return self._sink.items

    @property
    def sink(self) -> SinkHandler[T]:
        return self._sink


class GlobFilesHandler(Handler[Path, Path]):
    def __init__(self, pattern: str):
        self.pattern = pattern
        super().__init__()

    def handle(self, item: Path):
        if not self.next_handler or not item.is_dir():
            return

        for sub in item.glob(self.pattern):
            self.next_handler.handle(sub)


class ExcludeFileHandler(Handler[Path, Path]):
    def __init__(self, *exclude_patterns: str):
        self.exclude_patterns = exclude_patterns
        super().__init__()

    def handle(self, item: Path):
        if not self.next_handler:
            return

        for pattern in self.exclude_patterns:
            if item.match(pattern):
                return

        self.next_handler.handle(item)
