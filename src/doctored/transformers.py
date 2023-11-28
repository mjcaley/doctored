from pathlib import Path
import libcst as cst


def file_to_cst(file: Path):
    content = file.read_text()
    module = cst.parse_module(content)

    return module
