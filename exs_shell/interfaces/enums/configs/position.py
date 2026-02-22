from enum import StrEnum

from exs_shell.interfaces.enums.icons import Icons
from exs_shell.core.py import classproperty

Align = Icons.align
Arrow = Icons.arrow


class P(StrEnum):
    TOP_LEFT = "TOP_LEFT"
    TOP = "TOP"
    TOP_RIGHT = "TOP_RIGHT"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM = "BOTTOM"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"


def iterate(cls1: type[StrEnum], cls2: type[StrEnum]) -> list[tuple[str, str]]:
    return [(cls1[a.name].value, a.name.lower()) for a in cls2]


class PositionMixin:
    @classproperty
    def arrows(cls) -> list[tuple[str, str]]:
        return iterate(Arrow, cls)  # type: ignore

    @classproperty
    def aligns(cls) -> list[tuple[str, str]]:
        return iterate(Align, cls)  # type: ignore


class Side(PositionMixin, StrEnum):
    LEFT = P.LEFT
    RIGHT = P.RIGHT


class TopBottom(PositionMixin, StrEnum):
    TOP = P.TOP
    BOTTOM = P.BOTTOM


class Corner(PositionMixin, StrEnum):
    TOP_LEFT = P.TOP_LEFT
    TOP_RIGHT = P.TOP_RIGHT
    BOTTOM_LEFT = P.BOTTOM_LEFT
    BOTTOM_RIGHT = P.BOTTOM_RIGHT


class PositionAxis(PositionMixin, StrEnum):
    TOP = P.TOP
    BOTTOM = P.BOTTOM
    LEFT = P.LEFT
    RIGHT = P.RIGHT


class Position(PositionMixin, StrEnum):
    TOP_LEFT = P.TOP_LEFT
    TOP = P.TOP
    TOP_RIGHT = P.TOP_RIGHT
    BOTTOM_LEFT = P.BOTTOM_LEFT
    BOTTOM = P.BOTTOM
    BOTTOM_RIGHT = P.BOTTOM_RIGHT


class PositionSide(PositionMixin, StrEnum):
    TOP_LEFT = P.TOP_LEFT
    TOP = P.TOP
    TOP_RIGHT = P.TOP_RIGHT
    LEFT = P.LEFT
    RIGHT = P.RIGHT
    BOTTOM_LEFT = P.BOTTOM_LEFT
    BOTTOM = P.BOTTOM
    BOTTOM_RIGHT = P.BOTTOM_RIGHT
