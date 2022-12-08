from __future__ import annotations

import ast
from ast import NodeVisitor
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class RecordProperties:
    @property
    def name(self) -> str:
        return self.node.name

    @property
    def docstring(self) -> str:
        return ast.get_docstring(self.node)


@dataclass
class ModuleRecord(RecordProperties):
    node: ast.Module
    path: Path
    children: list[ASTRecord] = field(default_factory=list)


@dataclass
class ClassRecord(RecordProperties):
    node: ast.ClassDef
    children: list[ASTRecord] = field(default_factory=list)


@dataclass
class FunctionRecord(RecordProperties):
    node: ast.AST
    children: list[ASTRecord] = field(default_factory=list)


@dataclass
class AsyncFunctionRecord(RecordProperties):
    node: ast.AST
    children: list[ASTRecord] = field(default_factory=list)


ASTRecord = ModuleRecord | ClassRecord | FunctionRecord | AsyncFunctionRecord


class Visitor(NodeVisitor):
    def __init__(self, path: Path):
        self.path = path
        self.stack = []

    @property
    def top(self) -> ASTRecord:
        return self.stack[-1]

    @classmethod
    def visit_ast(cls, path: Path) -> ModuleRecord:
        with open(path) as file:
            source = file.read()
        tree = ast.parse(source)
        visitor = cls(path)
        visitor.visit(tree)

        return visitor.stack[0]

    def visit_Module(self, node: ast.Module) -> Any:
        record = ModuleRecord(node, self.path)
        self.stack.append(record)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        record = ClassRecord(node)
        self.top.children.append(record)
        self.stack.append(record)
        self.generic_visit(node)
        self.stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        record = FunctionRecord(node)
        self.top.children.append(record)
        self.stack.append(record)
        self.generic_visit(node)
        self.stack.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        record = AsyncFunctionRecord(node)
        self.top.children.append(record)
        self.stack.append(record)
        self.generic_visit(node)
        self.stack.pop()
