import ast
from ast import NodeVisitor
from typing import Any


class Visitor(NodeVisitor):
    def visit_Module(self, node: ast.Module) -> Any:
        return super().visit_Module(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        return super().visit_ClassDef(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        return super().visit_FunctionDef(node)

    def visit_AsyncFunctionDef(node: ast.AsyncFunctionDef) -> Any:
        return super().visit_AsyncFunctionDef(node)
