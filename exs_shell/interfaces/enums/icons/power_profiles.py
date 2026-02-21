from enum import StrEnum

from exs_shell.core.py import classproperty

class PPIcons(StrEnum):
    PERFORMANCE = "electric_bolt"
    BALANCED = "balance"
    POWER_SAVER = "energy_savings_leaf"
    # PERFORMANCE = "󱐋"
    # BALANCED = ""
    # POWER_SAVER = "󰌪"

    __mappings__: dict[str, tuple[str, str]] = {
        "performance": (PERFORMANCE, "Performance"),
        "balanced": (BALANCED, "Balanced"),
        "power-saver": (POWER_SAVER, "Power saver"),
    }

    @classmethod
    def icon(cls, profile: str) -> str:
        return cls.__mappings__[profile][0]

    @classmethod
    def label(cls, profile: str) -> str:
        return cls.__mappings__[profile][1]

    @classproperty
    def raw(cls) -> dict[str, tuple[str, str]]:
        return cls.__mappings__
