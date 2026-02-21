from enum import StrEnum


class ArrowIcons(StrEnum):
    TOP_LEFT = "north_west"
    TOP = "arrow_upward"
    TOP_RIGHT = "north_east"
    LEFT = "arrow_back"
    RIGHT = "arrow_forward"
    BOTTOM_LEFT = "south_west"
    BOTTOM = "arrow_downward"
    BOTTOM_RIGHT = "south_east"
    # TOP_LEFT = ""
    # TOP = ""
    # TOP_RIGHT = ""
    # LEFT = ""
    # RIGHT = ""
    # BOTTOM_LEFT = ""
    # BOTTOM = ""
    # BOTTOM_RIGHT = ""
    # TOP_LEFT = "󰁛"
    # TOP = "󰁝"
    # TOP_RIGHT = "󰁜"
    # LEFT = "󰁍"
    # RIGHT = "󰁔"
    # BOTTOM_LEFT = "󰁂"
    # BOTTOM = "󰁅"
    # BOTTOM_RIGHT = "󰁃"


class AlignIcons(StrEnum):
    TOP = "align_vertical_top"
    BOTTOM = "align_vertical_bottom"
    LEFT = "align_horizontal_left"
    RIGHT = "align_horizontal_right"
    # TOP = "󱇇"
    # BOTTOM = "󱇅"
    # LEFT = "󱇂"
    # RIGHT = "󱇄"
