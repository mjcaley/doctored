from __future__ import annotations

from abc import ABC, abstractmethod, abstractproperty
from ast import AST
from itertools import pairwise
from pathlib import Path
from typing import Any, Generic, TypeVar


class Pipeline:
    def __init__(
        self,
        file_handlers: HandlerCollection[Path],
        ast_handlers: HandlerCollection[AST],
    ):
        self.file_handlers = file_handlers
        self.ast_handlers = ast_handlers

    def run_files(self, root: Path) -> list[Path]:
        files = root.glob("**/*.py")
        for file in files:
            self.file_handlers.handle(file)
        return self.file_handlers.sink.items


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

    def handle(self, item: T):
        self.handlers[0].handle(item)

    @property
    def sink(self) -> SinkHandler[T]:
        return self._sink


class PipelineBuilder:
    def __init__(self):
        self._file_handlers: list[Handler[Path]] = []
        self._ast_handlers: list[Handler[AST]] = []

    def add_file_handler(self, handler: Handler[Path]) -> PipelineBuilder:
        self._file_handlers.append(handler)
        return self

    def add_ast_handler(self, handler: Handler[AST]) -> PipelineBuilder:
        self._ast_handlers.append(handler)
        return self

    @staticmethod
    def _link_handlers(handlers: list[Handler]) -> HandlerCollection:
        for handler, next_handler in pairwise(handlers):
            handler.next_handler = next_handler

        return HandlerCollection(*handlers)

    def build(self) -> Pipeline:
        file_handlers = self._link_handlers(self._file_handlers)
        ast_handlers = self._link_handlers(self._ast_handlers)

        return Pipeline(file_handlers, ast_handlers)
