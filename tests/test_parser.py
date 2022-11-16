from doctored.parser import rest_parser


def test_rest_parser():
    result = rest_parser("tests/example/sample.py")

    assert None is not result
