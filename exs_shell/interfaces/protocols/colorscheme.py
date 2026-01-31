from typing import Any, Protocol


class ColorSchemeInterface(Protocol):
    def __init__(self, source_color_hct: Any, is_dark: bool, contrast_level: float): ...
