from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

T = TypeVar("T")


class IHandler(ABC, Generic[T]):
    @abstractmethod
    def handle(self, item: T):
        """Logic to perform an action on the item.

        If successful, call the `next_handler`'s `handle` method. Otherwise, it can be consumed and processing will stop.

        :param item: T
        """


class Handler(IHandler, Generic[T]):
    def __init__(self):
        self._handler = None

    @property
    def next_handler(self) -> Handler[T] | None:
        return self._handler

    @next_handler.setter
    def next_handler(self, handler: Handler[T]):
        self._handler = handler

    def handle(self, item: T):
        raise NotImplementedError


class SinkHandler(Handler[T]):
    def __init__(self):
        self._items: list[T] = []
        super().__init__()

    def handle(self, item: T):
        self._items.append(item)

    @property
    def items(self):
        return self._items


class HandlerCollection(Generic[T]):
    def __init__(self, *handlers: Handler[T]):
        self.handlers = list(handlers)
        self._sink: SinkHandler = SinkHandler()
        if self.handlers:
            handlers[-1].next_handler = self._sink
        self.handlers.append(self._sink)

    def handle(self, item: T) -> list[T]:
        self.handlers[0].handle(item)

        return self._sink.items

    @property
    def sink(self) -> SinkHandler[T]:
        return self._sink


class GlobFilesHandler(Handler[Path]):
    def __init__(self, pattern: str):
        self.pattern = pattern
        super().__init__()

    def handle(self, item: Path):
        if not self.next_handler or not item.is_dir():
            return

        for sub in item.glob(self.pattern):
            self.next_handler.handle(sub)


class ExcludeFileHandler(Handler[Path]):
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
