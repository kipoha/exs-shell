from enum import StrEnum


class BacklightIcons(StrEnum):
    B1 = "brightness_1"
    B2 = "brightness_2"
    B3 = "brightness_3"
    B4 = "brightness_4"
    B5 = "brightness_5"
    B6 = "brightness_6"
    B7 = "brightness_7"
    AUTO = "brightness_auto"
    # B1 = "󰃚"
    # B2 = "󰃛"
    # B3 = "󰃜"
    # B4 = "󰃝"
    # B5 = "󰃞"
    # B6 = "󰃟"
    # B7 = "󰃠"
    # AUTO = "󰃡"

    @classmethod
    def mapping(cls, brightness: int) -> str:
        _mapping = [
            (20, cls.B1),
            (30, cls.B2),
            (40, cls.B3),
            (50, cls.B4),
            (65, cls.B5),
            (75, cls.B6),
            (85, cls.B7),
        ]

        for limit, icon in _mapping:
            if brightness <= limit:
                return icon

        return cls.B7
