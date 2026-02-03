from dataclasses import dataclass


@dataclass
class Action:
    name: str
    command: str
    icon: str
