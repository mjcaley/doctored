import ast
from ast import NodeVisitor
from copy import copy
from pathlib import Path
from typing import Any

from .models import ASTNodeRecord


def _auto_stack(func):
    def inner(self, node: Any) -> Any:
        self.stack.append(node.name)
        ret = func(self, node)
        self.stack.pop()
        return ret

    return inner


class Visitor(NodeVisitor):
    def __init__(self, path: Path):
        self.path = path
        self.stack: list[str] = []
        self.nodes: list[ASTNodeRecord] = []

    @classmethod
    def visit_ast(cls, path: Path) -> list[ASTNodeRecord]:
        with open(path) as file:
            source = file.read()
        tree = ast.parse(source)
        visitor = cls(path)
        visitor.visit(tree)

        return visitor.nodes

    def visit_Module(self, node: ast.Module) -> Any:
        self.stack.append(str(self.path))
        self.nodes.append(
            ASTNodeRecord(self.path, copy(self.stack), node, ast.get_docstring(node))
        )
        self.stack.pop()

    @_auto_stack
    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.nodes.append(
            ASTNodeRecord(self.path, copy(self.stack), node, ast.get_docstring(node))
        )

    @_auto_stack
    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.nodes.append(
            ASTNodeRecord(self.path, copy(self.stack), node, ast.get_docstring(node))
        )

    @_auto_stack
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
        self.nodes.append(
            ASTNodeRecord(self.path, copy(self.stack), node, ast.get_docstring(node))
        )
