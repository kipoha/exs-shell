from dataclasses import dataclass


@dataclass
class ClipboardItem:
    id: str
    raw: str
    is_binary: bool
