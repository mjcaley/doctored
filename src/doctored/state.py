from dataclasses import dataclass, field
from pathlib import Path
import libcst as cst


@dataclass
class State:
    trees: dict[Path, cst.Module] = field(default_factory=dict)
