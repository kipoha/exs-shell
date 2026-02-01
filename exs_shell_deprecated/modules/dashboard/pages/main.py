from typing import Any

from ignis import widgets

from exs_shell_deprecated.modules.dashboard.widgets.actions import Actions
from exs_shell_deprecated.modules.dashboard.widgets.clock import Clock
from exs_shell_deprecated.modules.dashboard.widgets.powerprofile import PowerProfile
from exs_shell_deprecated.modules.dashboard.widgets.mini_player import MiniPlayer
from exs_shell_deprecated.modules.dashboard.widgets.shared.mpris import MprisPlayerManager
from exs_shell_deprecated.modules.dashboard.widgets.profile import UserProfile
from exs_shell_deprecated.modules.dashboard.widgets.calendar import Calendar
from exs_shell_deprecated.modules.dashboard.widgets.weather import Weather


class MainPage(widgets.Box):
    def __init__(self, **kwargs: Any):
        self._profile__power_box = widgets.Box(
            spacing=2,
            css_classes=["dashboard-page-main-profile-power"],
            child=[
                UserProfile(),
                Actions(),
                PowerProfile(),
            ],
        )
        self._weather__clock_box = widgets.Box(
            spacing=10,
            vertical=True,
            css_classes=["dashboard-page-main-weather-clock"],
            child=[
                Clock(),
                Weather(),
            ],
        )
        self._weather__mini_player_box = widgets.Box(
            spacing=10,
            css_classes=["dashboard-page-main-weather-mini-player"],
            child=[
                self._weather__clock_box,
                MprisPlayerManager(MiniPlayer, "mini-player"),
            ],
        )
        self._left_box = widgets.Box(
            spacing=10,
            vertical=True,
            css_classes=["dashboard-page-main-left"],
            child=[
                self._profile__power_box,
                self._weather__mini_player_box,
            ],
        )
        super().__init__(
            spacing=10,
            css_classes=["dashboard-page-main"],
            child=[
                self._left_box,
                Calendar(),
            ],
        )
