from dataclasses import dataclass
from pathlib import Path


@dataclass
class Plugin:
    name: str
    path: Path
