import libcst as cst


class DoctoredVisitor(cst.CSTVisitor):
    def __init__(self):
        self.stack = []

    def visit_FunctionDef(self, node: cst.FunctionDef):
        self.stack.append(node.name.value)

    def leave_FunctionDef(self, _: cst.FunctionDef):
        self.stack.pop()

    def visit_ClassDef(self, node: cst.ClassDef):
        self.stack.append(node.name.value)

    def leave_ClassDef(self, _: cst.ClassDef):
        self.stack.pop()


# import ast
# from ast import NodeVisitor
# from typing import Any


# class Visitor(NodeVisitor):
#     def visit_Module(self, node: ast.Module) -> Any:
#         return super().visit_Module(node)

#     def visit_ClassDef(self, node: ast.ClassDef) -> Any:
#         return super().visit_ClassDef(node)

#     def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
#         return super().visit_FunctionDef(node)

#     def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> Any:
#         return super().visit_AsyncFunctionDef(node)
