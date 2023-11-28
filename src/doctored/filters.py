from pathlib import Path
from typing import Callable


def match(pattern: str = "*.py") -> Callable[[Path], bool]:
    def inner(path: Path) -> bool:
        return path.match(pattern)
    
    return inner

def exclude(pattern: str) -> Callable[[Path], bool]:
    def inner(path: Path) -> bool:
        return not path.match(pattern)

    return inner
