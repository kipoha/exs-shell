from dataclasses import dataclass


@dataclass
class Action:
    name: str
    command: str
    icon: str


@dataclass
class WebAction:
    name: str
    url: str
    icon: str
