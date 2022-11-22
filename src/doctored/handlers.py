"""Handlers definitions and implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class INextHandler(ABC, Generic[T]):
    @property
    @abstractproperty
    def next_handler(self) -> IHandle[T] | None:
        """Next handler in the chain.

        :return: Instance of `IHandler`.
        """

    @next_handler.setter
    @abstractproperty
    def next_handler(self, handler: IHandle[T]):
        """Set the handler."""


class IHandle(ABC, Generic[T]):
    @abstractmethod
    def handle(self, item: T):
        """Logic to perform an action on the item.

        If successful, call the `next_handler`'s `handle` method. Otherwise, it can be consumed and processing will stop.

        :param item: T
        """


class Handler(IHandle[T], INextHandler[T], Generic[T]):
    def __init__(self):
        self._handler = None

    @property
    def next_handler(self) -> IHandle[T] | None:
        return self._handler

    @next_handler.setter
    def next_handler(self, handler: IHandle[T]):
        self._handler = handler

    def handle(self, item: T):
        raise NotImplementedError


class SinkHandler(Handler[T]):
    def __init__(self):
        self._items = []
        super().__init__()

    def handle(self, item: T):
        self._items.append(item)

    @property
    def items(self) -> list[T]:
        return self._items


class HandlerChain(Generic[T]):
    def __init__(self, *handlers: Handler[T]):
        self.handlers = list(handlers)

    def handle(self, item: T) -> list[T]:
        if not self.handlers:
            return [item]

        sink = SinkHandler()

        head = self.handlers[0]
        tail = self.handlers[-1]
        tail.next_handler = sink
        head.handle(item)
        tail.next_handler = None

        return sink.items


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
