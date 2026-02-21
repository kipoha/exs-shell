from typing import Any
from ignis.widgets import Label

from exs_shell.interfaces.types import IconSize


class Icon(Label):
    def __init__(self, label: str, size: IconSize, **kwargs: Any):
        sizes = {
            "xs": ["extra-small", "xs"],
            "s": ["small", "s"],
            "m": ["medium", "m"],
            "l": ["large", "l"],
            "xl": ["extra-large", "xl"],
            "xxl": ["extra-extra-large", "xxl"],
            "xxxl": ["extra-extra-extra-large", "xxxl"],
        }
        kwargs["css_classes"] = ["icon", *sizes[size]]
        super().__init__(label=label, **kwargs)
