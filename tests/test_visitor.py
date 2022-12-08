import ast
from dataclasses import dataclass
from pathlib import Path

import pytest

from doctored.visitor import Visitor


@dataclass
class PathAndDocstring:
    path: Path
    docstring: str | None


@pytest.fixture
def module_source(tmp_path):
    src = tmp_path / "source.py"
    src.touch()

    yield src


@pytest.fixture
def docstring():
    yield "This is a docstring."


@pytest.fixture
def module_with_docstring(module_source, docstring):
    module_source.write_text('"""' + docstring + '"""')

    yield PathAndDocstring(module_source, docstring)


@pytest.fixture
def class_with_docstring(module_source, docstring):
    module_source.write_text(
        f"""
class Name:
    '''{docstring}'''
    pass
"""
    )

    yield PathAndDocstring(module_source, docstring)


@pytest.fixture
def class_without_docstring(module_source):
    module_source.write_text(
        f"""
class Name:
    pass
"""
    )

    yield PathAndDocstring(module_source, None)


@pytest.fixture
def function_with_docstring(module_source, docstring):
    module_source.write_text(
        f"""
def name():
    '''{docstring}'''
    pass
"""
    )

    yield PathAndDocstring(module_source, docstring)


@pytest.fixture
def function_without_docstring(module_source):
    module_source.write_text(
        f"""
def name():
    pass
"""
    )

    yield PathAndDocstring(module_source, None)


@pytest.fixture
def async_function_with_docstring(module_source, docstring):
    module_source.write_text(
        f"""
async def name():
    '''{docstring}'''
    pass
"""
    )

    yield PathAndDocstring(module_source, docstring)


@pytest.fixture
def async_function_without_docstring(module_source):
    module_source.write_text(
        f"""
async def name():
    pass
"""
    )

    yield PathAndDocstring(module_source, None)


@pytest.fixture
def nested_source(module_source, docstring):
    src = f"""
'''{docstring}'''


class Class:
    '''{docstring}'''

    class SubClass:
        '''{docstring}'''
        pass

    def func1(self):
        '''{docstring}'''

        def inner_func1():
            pass

    async def func2(self):
        '''{docstring}'''

        def inner_func2():
            pass
"""
    module_source.write_text(src)

    yield PathAndDocstring(module_source, docstring)


def test_visit_module(module_with_docstring):
    result = Visitor.visit_ast(module_with_docstring.path)

    assert ast.Module == type(result.node)
    assert module_with_docstring.path == result.path
    assert module_with_docstring.docstring == result.docstring


def test_visit_class_def_with_docstring(class_with_docstring):
    result = Visitor.visit_ast(class_with_docstring.path)
    result_class = result.children[0]

    assert "Name" == result_class.name
    assert class_with_docstring.docstring == result_class.docstring


def test_visit_class_def_without_docstring(class_without_docstring):
    result = Visitor.visit_ast(class_without_docstring.path)
    result_class = result.children[0]

    assert "Name" == result_class.name
    assert class_without_docstring.docstring == result_class.docstring


def test_visit_function_def_with_docstring(function_with_docstring):
    result = Visitor.visit_ast(function_with_docstring.path)
    result_func = result.children[0]

    assert "name" == result_func.name
    assert function_with_docstring.docstring == result_func.docstring


def test_visit_function_def_without_docstring(function_without_docstring):
    result = Visitor.visit_ast(function_without_docstring.path)
    result_func = result.children[0]

    assert "name" == result_func.name
    assert function_without_docstring.docstring == result_func.docstring


def test_visit_async_function_def_with_docstring(async_function_with_docstring):
    result = Visitor.visit_ast(async_function_with_docstring.path)
    result_func = result.children[0]

    assert "name" == result_func.name
    assert async_function_with_docstring.docstring == result_func.docstring


def test_visit_async_function_def_without_docstring(async_function_without_docstring):
    result = Visitor.visit_ast(async_function_without_docstring.path)
    result_func = result.children[0]

    assert "name" == result_func.name
    assert async_function_without_docstring.docstring == result_func.docstring


def test_visit_complicated(nested_source):
    result = Visitor.visit_ast(nested_source.path)
    result_class = result.children[0]
