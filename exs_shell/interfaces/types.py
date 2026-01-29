from __future__ import annotations

from typing import Any, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    from exs_shell.interfaces.schemas.ipc.commands import Command


type Anchor = Literal["left", "right", "top", "bottom"]
type AnyDict = dict[str, Any]
type AnyList = list[Any]
type Commands = dict[str, Command]
