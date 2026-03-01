from typing import Any
from ignis.widgets import Button, Entry, Separator, SpinButton

from exs_shell.configs.user import weather, osd, notifications, user
from exs_shell.interfaces.enums.configs.position import PositionSide
from exs_shell.interfaces.enums.configs.osd import osd_type
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.modules.settings.tabs.base import BaseTab, BaseCategory
from exs_shell.ui.modules.settings.widgets import (
    CategoryLabel,
    DynamicTable,
    SettingsRow,
    DialogRow,
    SpinRow,
    SwitchRow,
    SelectRow,
)
from exs_shell.utils.commands import run_command
from exs_shell.utils.notify_system import send_notification


class WeatherCategory(BaseCategory):
    def __init__(self):
        self.entry = Entry(
            hexpand=True,
            halign="fill",
            placeholder_text="Enter your location",
            text=weather.bind("location"),
            css_classes=["settings-row-dialog-entry"],
        )
        super().__init__(
            child=[
                CategoryLabel(title="Weather", icon=Icons.ui.WEATHER),
                SettingsRow(
                    Icons.ui.LOCATION,
                    title="Location",
                    description="Your location",
                    child=[
                        DialogRow(
                            title="Choose Location",
                            description="Choose your location\n(example: New York)",
                            child=[self.entry],
                            value_getter=lambda: self.entry.get_text(),
                            on_change=lambda x: weather.set_location(x),
                            clear_on_cancel=lambda: self.entry.set_text(
                                weather.location
                            ),
                        ),
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
                Separator(),
                SettingsRow(
                    title="Test notification",
                    description="Send a test notification",
                    child=[
                        Button(
                            css_classes=["settings-row-button"],
                            label="Send a Test Notification",
                            on_click=lambda _: send_notification(
                                "Test notification", "Test message"
                            ),
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
                Separator(),
                SettingsRow(
                    title="Show OSD",
                    description="Show the OSD on the screen",
                    child=[
                        Button(
                            css_classes=["settings-row-button"],
                            label="Show OSD",
                            on_click=lambda _: run_command("osd", "show"),
                        )
                    ],
                ),
            ]
        )


class BatteryTrackerCategory(BaseCategory):
    def __init__(self):
        super().__init__(
            [
                CategoryLabel(title="Battery Tracker", icon=Icons.battery.CHARGING),
                SettingsRow(
                    title="Battery Critical Percentage",
                    description="Set the battery critical percentage",
                    child=[
                        SpinRow(
                            min=0,
                            max=100,
                            step=1,
                            value=user.bind("critical_percentage"),
                            on_change=lambda x: user.set_critical_percentage(x),
                        )
                    ],
                ),
            ]
        )


class IdleCategory(BaseCategory):
    def __init__(self):
        row_datas = [
            [a.timeout_seconds, a.on_timeout, a.on_resume]
            for a in user.get_idle_actions_objs()
        ]

        def build(datas: list[list[Any]]) -> list[dict]:
            return [
                {
                    "timeout_seconds": int(data[0]),
                    "on_timeout": data[1],
                    "on_resume": data[2],
                }
                for data in datas
            ]

        self.actions_table = DynamicTable(
            ["Timeout", "On Timeout", "On Resume"],
            [SpinButton, Entry, Entry],
            row_datas,
            build,
            150,
        )
        super().__init__(
            [
                CategoryLabel(title="Idle", icon=Icons.ui.IDLE),
                SettingsRow(
                    title="Idle Actions",
                    description="Set the idle actions",
                    child=[
                        DialogRow(
                            title="Idle Actions",
                            description="Set the idle actions",
                            child=[self.actions_table],
                            value_getter=self.actions_table.get_data,
                            on_change=lambda x: user.set_idle_actions(x),
                            clear_on_cancel=lambda: self.actions_table.clear(),
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
                BatteryTrackerCategory(),
                IdleCategory(),
                WeatherCategory(),
            ]
        )
