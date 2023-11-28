from pathlib import Path
from doctored.filters import match, exclude


def test_match_filter_default():
    src_file = Path("./src.py")
    txt_file = Path("./text.txt")

    m = match()

    assert m(src_file)
    assert not m(txt_file)


def test_match_filter_custom(tmp_path):
    src_file = Path("./src.py")
    txt_file = Path("./text.txt")

    m = match("*.txt")

    assert not m(src_file)
    assert m(txt_file)


def test_exclude_match_filter_custom(tmp_path):
    src_file = Path("./src.py")
    txt_file = Path("./text.txt")

    m = exclude("*.txt")

    assert m(src_file)
    assert not m(txt_file)
