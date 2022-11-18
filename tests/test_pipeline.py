from pathlib import Path

from doctored.handlers import Handler, HandlerCollection
from doctored.pipeline import Pipeline, PipelineBuilder


def test_pipeline_run_files():
    root = Path(__file__).absolute().parent / "example"
    p = Pipeline(HandlerCollection(), HandlerCollection())
    result = p.run_files(root)

    assert [root] == result


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
