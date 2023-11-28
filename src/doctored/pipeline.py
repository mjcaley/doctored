from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator, cast
import libcst as cst
import libcst.matchers as m

from doctored.filters import match


@dataclass
class FilterFileResult:
    path: Path
    module: cst.Module


def filter_files(base: Path, *file_filters: Callable[[Path], bool]) -> Iterator[FilterFileResult]:
    for file in base.glob("**/*"):
        if all((file_filter(file) for file_filter in file_filters)):
            module = cst.parse_module(file.read_text())
            yield FilterFileResult(file, module)


@dataclass
class NodeFilterResult:
    path: Path
    name: str
    node: cst.ClassDef | cst.FunctionDef


def filter_nodes_impl(
    path: Path, stack: list[str], node: cst.CSTNode
) -> Iterator[NodeFilterResult]:
    if m.matches(node, m.ClassDef | m.FunctionDef):
        node_def = cast(cst.ClassDef | cst.FunctionDef, node)
        stack.append(node_def.name.value)
        yield NodeFilterResult(path, ".".join(stack), node_def)

        for child in node.children:
            for c in filter_nodes_impl(path, stack, child):
                yield c

        stack.pop()
    else:
        for child in node.children:
            for c in filter_nodes_impl(path, stack, child):
                yield c


def filter_nodes(file_result: FilterFileResult) -> Iterator[NodeFilterResult]:
    for node in filter_nodes_impl(
        file_result.path, [file_result.path.stem], file_result.module
    ):
        yield node


@dataclass
class NodeDetailsResult:
    path: Path
    name: str
    annotations: list[m.Param] | Any
    docstring: str | None


def filter_node_details(node_result: NodeFilterResult) -> NodeDetailsResult:
    if m.matches(node_result.node, m.FunctionDef()):
        func = cast(cst.FunctionDef, node_result.node)
        return NodeDetailsResult(
            node_result.path,
            node_result.name,
            func.params.params,
            func.get_docstring()
        )
    else:
        cls = cast(cst.ClassDef, node_result.node)
        return NodeDetailsResult(
            node_result.path,
            node_result.name,
            None,
            cls.get_docstring()
        )


def pipeline(root: Path):
    """Entry point for the whole thing."""

    for file_result in filter_files(root, match()):
        for node_result in filter_nodes(file_result):
            node_details = filter_node_details(node_result)
            print(node_details)


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
