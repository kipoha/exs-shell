from enum import StrEnum


class VolumeIcons(StrEnum):
    OVERAMPLIFIED = "󰕾"
    HIGH = "󰕾"
    MEDIUM = "󰖀"
    LOW = "󰕿"
    MUTED = "󰝟"

    @classmethod
    def mapping(cls, volume: float) -> str:
        _mapping = [
            (10, cls.LOW),
            (50, cls.MEDIUM),
            (75, cls.HIGH),
        ]

        for limit, icon in _mapping:
            if volume <= limit:
                return icon

        return cls.OVERAMPLIFIED
