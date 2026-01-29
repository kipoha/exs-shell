from enum import StrEnum


class Layer(StrEnum):
    BACKGROUND = "background"
    BOTTOM = "bottom"
    TOP = "top"
    OVERLAY = "overlay"


class Exclusivity(StrEnum):
    IGNORE = "ignore"
    NORMAL = "normal"
    EXCLUSIVE = "exclusive"


class KeyboardMode(StrEnum):
    NONE = "none"
    EXCLUSIVE = "exclusive"
    ON_DEMAND = "on_demand"
