from pathlib import Path

import pytest

from doctored.handlers import (
    ExcludeFileHandler,
    GlobFilesHandler,
    Handler,
    HandlerCollection,
    SinkHandler,
)


@pytest.fixture
def py_file(tmp_path: Path):
    py_file = tmp_path / "py_file.py"
    py_file.touch()

    yield py_file


@pytest.fixture
def py_dir(py_file: Path):
    yield py_file.parent


def test_base_handler(mocker):
    h = Handler()

    assert None is h.next_handler
    h2 = Handler()
    h.next_handler = h2
    assert h2 is h.next_handler
    with pytest.raises(NotImplementedError):
        h.handle(mocker.Mock())


def test_sink_handler(mocker):
    s = SinkHandler()

    assert [] == s.items
    s.handle(42)
    assert [42] == s.items


def test_handler_collection(mocker):
    class FakeHandler(Handler[int]):
        def handle(self, item: int):
            self.next_handler.handle(item)

    h1 = FakeHandler()
    h2 = FakeHandler()
    h1.next_handler = h2
    h1_spy = mocker.spy(h1, "handle")
    h2_spy = mocker.spy(h2, "handle")
    c = HandlerCollection(h1, h2)
    c.handle(42)

    h1_spy.assert_called_once_with(42)
    h2_spy.assert_called_once_with(42)


def test_empty_handler_collection():
    c = HandlerCollection()
    c.handle(42)

    assert 1 == len(c.sink.items)
    assert 42 == c.sink.items[0]


def test_glob_file_handler_no_next_handler(py_dir):
    g = GlobFilesHandler("*.py")

    g.handle(py_dir)

    assert True


def test_glob_file_handler_globs_files(py_file):
    g = GlobFilesHandler("*.py")
    s = SinkHandler()
    g.next_handler = s

    g.handle(py_file.parent)

    assert [py_file] == s.items


def test_exclude_file_handler_no_handler(py_file):
    e = ExcludeFileHandler()

    e.handle(py_file)

    assert True


def test_exclude_file_handler_no_exclusions(py_file):
    e = ExcludeFileHandler()
    s = SinkHandler()
    e.next_handler = s

    e.handle(py_file)

    assert [py_file] == s.items


def test_exclude_file_handler_file_excluded(py_file):
    e = ExcludeFileHandler("*.py")
    s = SinkHandler()
    e.next_handler = s

    e.handle(py_file)

    assert [] == s.items


def test_exclude_file_handler_file_passes_exclusions(py_file):
    e = ExcludeFileHandler("*.txt", "docs/")
    s = SinkHandler()
    e.next_handler = s

    e.handle(py_file)

    assert [py_file] == s.items
