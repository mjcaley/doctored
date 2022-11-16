from pathlib import Path

import pytest

from doctored.pipeline import (
    Handler,
    HandlerCollection,
    Pipeline,
    PipelineBuilder,
    SinkHandler,
)


def test_pipeline_run_files():
    root = Path(__file__).absolute().parent / "example"
    p = Pipeline(HandlerCollection(), HandlerCollection())
    result = p.run_files(root)

    assert [root / "sample.py"] == result


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


def test_pipeline_builder_empty():
    b = PipelineBuilder()
    p = b.build()

    assert "p" in locals()


def test_pipeline_builder_add_file_handler(mocker):
    b = PipelineBuilder()
    b1 = b.add_file_handler(mocker.Mock())

    assert b is b1


def test_pipeline_builder_add_ast_handler(mocker):
    b = PipelineBuilder()
    b1 = b.add_ast_handler(mocker.Mock())

    assert b is b1


def test_pipeline_builder_multiple_handlers(mocker):
    class MockHandler(Handler):
        ...

    h1 = MockHandler()
    h2 = MockHandler()

    b = PipelineBuilder()
    b.add_ast_handler(h1)
    b.add_ast_handler(h2)
    p = b.build()

    assert h2 is h1.next_handler
