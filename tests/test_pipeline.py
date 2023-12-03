from pathlib import Path

import libcst as cst

from doctored.pipeline import NodeDetails, NodeResult, filter_nodes, parse_files


def test_filter_files_default(tmp_path):
    (tmp_path / "src.py").touch()
    modules = [f for f in parse_files(tmp_path)]

    assert all(isinstance(module, cst.Module) for module in modules)


def test_filter_files_filter_success(tmp_path):
    (tmp_path / "src.py").touch()
    modules = [f for f in parse_files(tmp_path, lambda _: True)]

    assert all(isinstance(module, cst.Module) for module in modules)


def test_filter_files_filter_fail(tmp_path):
    (tmp_path / "src.py").touch()
    modules = [f for f in parse_files(tmp_path, lambda _: False)]

    assert all(isinstance(module, cst.Module) for module in modules)


def test_node_filter():
    test_src = """
class TestClass:
    def nested_method(self):
        ...

def test_function():
    ...
    """
    module = cst.parse_module(test_src)

    nodes = [node for node in filter_nodes(module)]

    class_result = nodes[0]
    func_result = nodes[1]
    assert isinstance(class_result.node, cst.ClassDef)
    assert isinstance(func_result.node, cst.FunctionDef)
