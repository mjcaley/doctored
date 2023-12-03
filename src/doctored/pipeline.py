from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator, cast

import libcst as cst
import libcst.matchers as m

from doctored.filters import match


def parse_files(
    base: Path, *file_filters: Callable[[Path], bool]
) -> Iterator[cst.Module]:
    for file in base.glob("**/*"):
        if all((file_filter(file) for file_filter in file_filters)):
            yield cst.parse_module(file.read_text())


@dataclass
class NodeResult:
    stack: list[str]
    node: cst.ClassDef | cst.FunctionDef


def _filter_nodes(stack: list[str], node: cst.CSTNode) -> Iterator[NodeResult]:
    if m.matches(node, m.ClassDef | m.FunctionDef):
        node_def = cast(cst.ClassDef | cst.FunctionDef, node)
        stack.append(node_def.name.value)
        yield NodeResult(stack.copy(), node_def)

        for child in node.children:
            for c in _filter_nodes(stack, child):
                yield c

        stack.pop()
    else:
        for child in node.children:
            for c in _filter_nodes(stack, child):
                yield c


def filter_nodes(module: cst.Module) -> Iterator[NodeResult]:
    for node in _filter_nodes([], module):
        yield node


@dataclass
class NodeDetails:
    annotations: list[m.Param] | Any
    docstring: str | None


def node_details(node: cst.FunctionDef | cst.ClassDef):
    if m.matches(node, m.FunctionDef()):
        func = cast(cst.FunctionDef, node)
        return NodeDetails(func.params, func.get_docstring())
    else:
        cls = cast(cst.ClassDef, node)
        return NodeDetails(None, cls.get_docstring())


@dataclass
class NodeParamsResult:
    path: Path
    name: str
    annotations: dict[str, str]
    docstring: str | None


# def transform_params(node_details_result: NodeDetailsResult) -> NodeParamsResult:
#     ...


def pipeline(root: Path):
    """Entry point for the whole thing."""

    for file_result in parse_files(root, match()):
        for node_result in filter_nodes(file_result):
            details = node_details(node_result.node)
            print(details)


class Pipeline:
    def __init__(self, file_filters: list[Callable[[Path], bool]]):
        self.file_filters = file_filters

    def run(self, base: Path):
        for file in self.next_file(base):
            module = cst.parse_module(file.read_text())

    def next_file(self, base: Path):
        for file in base.glob("*/**"):
            if all((file_filter(file) for file_filter in self.file_filters)):
                yield file


class PipelineBuilder:
    def __init__(self):
        self.file_filters = []

    def build(self) -> Pipeline:
        pipeline = Pipeline(self.file_filters)

        return pipeline

    def add_file_filter(self, file_filter: Callable[[Path], bool]) -> "PipelineBuilder":
        self.file_filters.append(file_filter)

        return self

    def add_node_filter(self, node: Any) -> "PipelineBuilder":
        return self

    def add_configuration(self, config: Any) -> "PipelineBuilder":
        return self
