from typing import Any
from dataclasses import dataclass, field, fields

from exs_shell.interfaces.enums.gtk.windows import Exclusivity, KeyboardMode, Layer
from exs_shell.interfaces.types import Anchor, AnyDict


@dataclass
class WindowParam:
    namespace: str
    monitor: int | None = None
    anchor: list[Anchor] | None = None
    exclusivity: Exclusivity = Exclusivity.NORMAL
    layer: Layer = Layer.TOP
    kb_mode: KeyboardMode = KeyboardMode.NONE
    popup: bool = False
    margin_bottom: int = 0
    margin_left: int = 0
    margin_right: int = 0
    margin_top: int = 0
    dynamic_input_region: bool = False
    extra: AnyDict = field(default_factory=dict)

    def __init__(
        self,
        namespace: str,
        monitor: int | None = None,
        anchor: list[Anchor] | None = None,
        exclusivity: Exclusivity = Exclusivity.NORMAL,
        layer: Layer = Layer.TOP,
        kb_mode: KeyboardMode = KeyboardMode.NONE,
        popup: bool = False,
        margin_bottom: int = 0,
        margin_left: int = 0,
        margin_right: int = 0,
        margin_top: int = 0,
        dynamic_input_region: bool = False,
        **kwargs: Any,
    ):
        self._standard_fields = set(self.__dataclass_fields__.keys())
        self.namespace = namespace
        self.monitor = monitor
        self.anchor = anchor
        self.exclusivity = exclusivity
        self.layer = layer
        self.kb_mode = kb_mode
        self.popup = popup
        self.margin_bottom = margin_bottom
        self.margin_left = margin_left
        self.margin_right = margin_right
        self.margin_top = margin_top
        self.dynamic_input_region = dynamic_input_region
        self.extra = {}
        self.extra = kwargs

    def asdict(self) -> AnyDict:
        return {
            f.name: getattr(self, f.name) for f in fields(self) if f.name != "extra"
        } | self.extra
