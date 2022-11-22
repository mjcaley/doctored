import ast

import pytest

from doctored.models import ASTNodeRecord
from doctored.visitor import Visitor


@pytest.fixture
def module_source(tmp_path):
    src = tmp_path / "source.py"
    src.touch()

    yield src


@pytest.fixture
def module_docstring():
    yield "This is a module docstring."


@pytest.fixture
def module_with_docstring(module_source, module_docstring):
    with open(module_source, "w") as module:
        module.write('"""' + module_docstring + '"""')

    yield {"path": module_source, "docstring": module_docstring}


def test_visit_ast(module_with_docstring):
    result = Visitor.visit_ast(module_with_docstring["path"])

    assert 1 == len(result)
    assert module_with_docstring["docstring"] == result[0].docstring
    assert module_with_docstring["path"] == result[0].path


def test_visits_module(mocker):
    module = ast.Module(body=[])
    mock_path = mocker.Mock()
    v = Visitor(mock_path)

    v.visit(module)
    result = v.nodes

    assert mock_path == result[0].path
    assert [str(mock_path)] == result[0].structure
    assert module is result[0].node
    assert None is result[0].docstring


def test_visits_module_with_docstring(mocker):
    docstring = "This is a docstring"
    module = ast.Module(body=[ast.Expr(ast.Constant(docstring))])
    mock_path = mocker.Mock()
    v = Visitor(mock_path)

    v.visit(module)
    result = v.nodes

    assert mock_path == result[0].path
    assert [str(mock_path)] == result[0].structure
    assert module is result[0].node
    assert docstring is result[0].docstring


def test_visit_empty_class_def(mocker):
    class_def = ast.ClassDef("Name", body=[ast.Pass()])
    mock_path = mocker.Mock()
    v = Visitor(mock_path)

    v.visit(class_def)
    result = v.nodes

    assert mock_path == result[0].path
    assert ["Name"] == result[0].structure
    assert class_def is result[0].node
    assert None is result[0].docstring


def test_visit_class_def_with_docstring(mocker):
    class_def = ast.ClassDef("Name", body=[ast.Pass()])
    mock_path = mocker.Mock()
    v = Visitor(mock_path)

    v.visit(class_def)
    result = v.nodes

    assert mock_path == result[0].path
    assert ["Name"] == result[0].structure
    assert class_def is result[0].node
    assert None is result[0].docstring


def test_visit_empty_function_def(mocker):
    function_def = ast.FunctionDef("name", body=[ast.Pass()])
    mock_path = mocker.Mock()
    v = Visitor(mock_path)

    v.visit(function_def)
    result = v.nodes

    assert mock_path == result[0].path
    assert ["name"] == result[0].structure
    assert function_def is result[0].node
    assert None is result[0].docstring


def test_visit_function_def_with_docstring(mocker):
    function_def = ast.FunctionDef("name", body=[ast.Pass()])
    mock_path = mocker.Mock()
    v = Visitor(mock_path)

    v.visit(function_def)
    result = v.nodes

    assert mock_path == result[0].path
    assert ["name"] == result[0].structure
    assert function_def is result[0].node
    assert None is result[0].docstring


def test_visit_empty_async_function_def(mocker):
    async_function_def = ast.AsyncFunctionDef("name", body=[ast.Pass()])
    mock_path = mocker.Mock()
    v = Visitor(mock_path)

    v.visit(async_function_def)
    result = v.nodes

    assert mock_path == result[0].path
    assert ["name"] == result[0].structure
    assert async_function_def is result[0].node
    assert None is result[0].docstring


def test_visit_async_function_def_with_docstring(mocker):
    async_function_def = ast.AsyncFunctionDef("name", body=[ast.Pass()])
    mock_path = mocker.Mock()
    v = Visitor(mock_path)

    v.visit(async_function_def)
    result = v.nodes

    assert mock_path == result[0].path
    assert ["name"] == result[0].structure
    assert async_function_def is result[0].node
    assert None is result[0].docstring
