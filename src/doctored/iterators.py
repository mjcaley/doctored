from pathlib import Path


def walk(path: Path) -> list[Path]:
    return path.glob("**/*.py")
