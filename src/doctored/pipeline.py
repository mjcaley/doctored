from __future__ import annotations

from ast import AST
from itertools import pairwise
from pathlib import Path

from .handlers import Handler, HandlerCollection


class Pipeline:
    def __init__(
        self,
        file_handlers: HandlerCollection[Path],
        ast_handlers: HandlerCollection[AST],
    ):
        self.file_handlers = file_handlers
        self.ast_handlers = ast_handlers

    def run_files(self, root: Path) -> list[Path]:
        return self.file_handlers.handle(root)


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
