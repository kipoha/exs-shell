from enum import StrEnum


class P(StrEnum):
    TOP_LEFT = "TOP_LEFT"
    TOP = "TOP"
    TOP_RIGHT = "TOP_RIGHT"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM = "BOTTOM"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"


class Side(StrEnum):
    LEFT = P.LEFT
    RIGHT = P.RIGHT


class TopBottom(StrEnum):
    TOP = P.TOP
    BOTTOM = P.BOTTOM


class Corner(StrEnum):
    TOP_LEFT = P.TOP_LEFT
    TOP_RIGHT = P.TOP_RIGHT
    BOTTOM_LEFT = P.BOTTOM_LEFT
    BOTTOM_RIGHT = P.BOTTOM_RIGHT


class PositionAxis(StrEnum):
    TOP = P.TOP
    BOTTOM = P.BOTTOM
    LEFT = P.LEFT
    RIGHT = P.RIGHT


class Position(StrEnum):
    TOP_LEFT = P.TOP_LEFT
    TOP = P.TOP
    TOP_RIGHT = P.TOP_RIGHT
    BOTTOM_LEFT = P.BOTTOM_LEFT
    BOTTOM = P.BOTTOM
    BOTTOM_RIGHT = P.BOTTOM_RIGHT


class PositionSide(StrEnum):
    TOP_LEFT = P.TOP_LEFT
    TOP = P.TOP
    TOP_RIGHT = P.TOP_RIGHT
    LEFT = P.LEFT
    RIGHT = P.RIGHT
    BOTTOM_LEFT = P.BOTTOM_LEFT
    BOTTOM = P.BOTTOM
    BOTTOM_RIGHT = P.BOTTOM_RIGHT
