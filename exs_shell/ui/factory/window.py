from typing import Any

from exs_shell.interfaces.types import Anchor
from exs_shell.interfaces.schemas.widget.base import WindowEntity
from exs_shell.interfaces.enums.gtk.windows import Exclusivity, KeyboardMode, Layer


def create(
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
    **extra: Any
) -> WindowEntity:
    return WindowEntity.create(
        namespace=namespace,
        monitor=monitor,
        anchor=anchor,
        exclusivity=exclusivity,
        layer=layer,
        kb_mode=kb_mode,
        popup=popup,
        margin_bottom=margin_bottom,
        margin_left=margin_left,
        margin_right=margin_right,
        margin_top=margin_top,
        dynamic_input_region=dynamic_input_region,
        **extra,
    )
