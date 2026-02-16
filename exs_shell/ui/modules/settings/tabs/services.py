from ignis.widgets import Separator

from exs_shell.configs.user import weather, osd
from exs_shell.interfaces.enums.configs.position import PositionSide
from exs_shell.interfaces.enums.configs.osd import osd_type
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    DialogRow,
    SwitchRow,
    SelectRow,
)


class WeatherCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel(title="Weather", icon=Icons.ui.WEATHER),
                SettingsRow(
                    title="Location",
                    description="Your location",
                    child=[
                        DialogRow(
                            on_change=lambda x: weather.set_location(x),
                            title="Choose Location",
                            description="Choose your location\n(example: New York)",
                            placeholder="Enter your location",
                            value=weather.bind("location"),
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    title="Farenheit",
                    description="Show temperature in farenheit",
                    child=[
                        SwitchRow(
                            active=weather.bind("farenheit"),  # type: ignore
                            on_change=lambda active: weather.set_farenheit(active),
                        )
                    ],
                ),
            ]
        )


class OSDCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            [
                CategoryLabel(title="OSD", icon=Icons.ui.OSD),
                SettingsRow(
                    icon=Icons.ui.SLINE,
                    title="Type",
                    description="Type of OSD",
                    child=[
                        SelectRow(
                            osd_type,
                            lambda x: osd.set_osd(x),
                            active=osd.osd,
                            css_classes=["exs-osd-select-type"],
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    icon=Icons.align.TOP,
                    title="Position",
                    description="Position of the OSD",
                    child=[
                        SelectRow(
                            PositionSide.arrows,
                            lambda x: osd.set_position(x),
                            active=osd.position,
                            css_classes=["exs-osd-select-arrow"],
                        )
                    ],
                ),
            ]
        )


class ServicesTab(BaseTab):
    def __init__(self):
        super().__init__(
            child=[
                WeatherCategory(),
                OSDCategory(),
            ]
        )
