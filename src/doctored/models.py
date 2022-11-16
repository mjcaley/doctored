from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
from queue import SimpleQueue


class Kind(Enum):
    Module = auto()
    Function = auto()
    AsyncFunction = auto()
    Class = auto()


@dataclass
class DocStringNode:
    path: Path
    kind: Kind
    docstring: str
