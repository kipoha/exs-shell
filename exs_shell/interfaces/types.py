from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from exs_shell.interfaces.schemas.ipc.commands import Command


type Anchor = Literal["left", "right", "top", "bottom"]
type TopBottom = Literal["top", "bottom"]
type Arrow = Literal[
    "top",
    "top_left",
    "top_right",
    "bottom_left",
    "bottom_right",
    "bottom",
    "left",
    "right",
]
type Align = Literal["top", "bottom", "left", "right"]
type OSD = Literal["arc", "scale"]
type AnyDict = dict[str, Any]
type AnyList = list[Any]
type Commands = dict[str, dict[str, Command]]
type RGB = tuple[int, int, int]
type RGBA = tuple[int, int, int, int]
type CavaOutput = Literal["text", "values"]
type IconSize = Literal["xs", "s", "m", "l", "xl", "xxl"]
