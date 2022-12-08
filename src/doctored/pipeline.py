from __future__ import annotations

import ast
from ast import AST
from itertools import pairwise
from pathlib import Path
from typing import Iterable

from .handlers import Handler, HandlerChain
from .visitor import ASTRecord, Visitor


class Pipeline:
    def __init__(
        self,
        file_handlers: HandlerChain[Path],
        ast_handlers: HandlerChain[ASTRecord],
    ):
        self.file_handlers = file_handlers
        self.ast_handlers = ast_handlers

    def run_files(self, root: Path) -> list[Path]:
        return self.file_handlers.handle(root)

    def run_ast(self, files: Iterable[Path]) -> list[ASTRecord]:
        records = [Visitor.visit_ast(file) for file in files]

        result = []
        for record in records:
            record_result = self.ast_handlers.handle(record)
            result.append(record_result)

        return result


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
    def _link_handlers(handlers: list[Handler]) -> HandlerChain:
        for handler, next_handler in pairwise(handlers):
            handler.next_handler = next_handler

        return HandlerChain(*handlers)

    def build(self) -> Pipeline:
        file_handlers = self._link_handlers(self._file_handlers)
        ast_handlers = self._link_handlers(self._ast_handlers)

        return Pipeline(file_handlers, ast_handlers)
