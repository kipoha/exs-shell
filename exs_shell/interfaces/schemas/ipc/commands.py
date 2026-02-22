from __future__ import annotations

from dataclasses import dataclass, field

from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from exs_shell.interfaces.types import AnyDict, AnyList


@dataclass
class Command:
    call: Callable[..., Any]
    args: AnyList = field(default_factory=list)
    kwargs: AnyDict = field(default_factory=dict)
    description: str = ""
    group: str = "base"
