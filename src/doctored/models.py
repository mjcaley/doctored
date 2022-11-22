from ast import AST
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ASTNodeRecord:
    path: Path
    structure: list[str]
    node: AST
    docstring: str | None
