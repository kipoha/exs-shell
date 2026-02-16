from ignis.widgets import Separator

from exs_shell.configs.user import weather, osd, notifications
from exs_shell.interfaces.enums.configs.position import PositionSide
from exs_shell.interfaces.enums.configs.osd import osd_type
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    SettingsRow,
    DialogRow,
    SpinRow,
    SwitchRow,
    SelectRow,
)


class WeatherCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel(title="Weather", icon=Icons.ui.WEATHER),
                SettingsRow(
                    Icons.ui.LOCATION,
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
                    icon=Icons.ui.TEMPERATURE,
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


class NotificationsCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            child=[
                CategoryLabel(title="Notifications", icon=Icons.ui.NOTIFICATIONS),
                SettingsRow(
                    title="Do not disturb",
                    description="Do not show notifications",
                    child=[
                        SwitchRow(
                            active=notifications.bind("dnd"),  # type: ignore
                            on_change=lambda active: notifications.set_dnd(active),
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    title="Popup timeout",
                    description="How long(in seconds) to show notifications",
                    child=[
                        SpinRow(
                            min=1,
                            max=10,
                            step=1,
                            value=notifications.popup_timeout / 1000,  # type: ignore
                            on_change=lambda x: notifications.set_popup_timeout(
                                x * 1000
                            ),
                        )
                    ],
                ),
                Separator(),
                SettingsRow(
                    title="Max popups count",
                    description="How many notifications to show at the same time",
                    child=[
                        SpinRow(
                            min=1,
                            max=10,
                            step=1,
                            value=notifications.max_popups_count,  # type: ignore
                            on_change=lambda x: notifications.set_max_popups_count(x),
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
                NotificationsCategory(),
                OSDCategory(),
                WeatherCategory(),
            ]
        )
