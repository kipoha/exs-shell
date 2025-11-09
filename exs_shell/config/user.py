import os

from ignis.options_manager import OptionsGroup, OptionsManager, TrackedList
from ignis.options import Options

from exs_shell.utils import Dirs, PathUtils


USER_OPTIONS_FILE = f"{Dirs.DATA_DIR}/user_options.json"
OLD_USER_OPTIONS_FILE = f"{Dirs.CACHE_DIR}/user_options.json"


def _migrate_old_options_file() -> None:
    with open(OLD_USER_OPTIONS_FILE) as f:
        data = f.read()

    with open(USER_OPTIONS_FILE, "w") as f:
        f.write(data)


class UserOptions(OptionsManager):
    def __init__(self):
        if not os.path.exists(USER_OPTIONS_FILE) and os.path.exists(
            OLD_USER_OPTIONS_FILE
        ):
            _migrate_old_options_file()

        try:
            super().__init__(file=USER_OPTIONS_FILE)
        except FileNotFoundError:
            pass

    class UserConfig(OptionsGroup):
        avatar: str = ""
        command_prefix: str = ">"
        clock_format: str = "󰥔 %H:%M:%S"
        notification_dnd: bool = False
        battery: dict = {
            "format": "{icon} {percentage}%",
            "icons": {
                "charging": "󱐋",
                "critical": "",
                "100": "",
                "70": "",
                "50": "",
                "30": "",
                "10": "",
            },
            "critical_level": 10,
        }

        actions: TrackedList[dict] = TrackedList()
        for i in [
            {"name": "Lock", "command": "exs-ipc open-lockscreen", "icon": PathUtils.generate_path("icons/action/lock_screen.png", PathUtils.assets_path)},
            {"name": "Clipboard", "command": "exs-ipc toggle-clipboard", "icon": PathUtils.generate_path("icons/action/clipboard.png", PathUtils.assets_path)},
            {"name": "Color Picker", "command": "exs-ipc action-color-picker", "icon": PathUtils.generate_path("icons/action/color_picker.png", PathUtils.assets_path)},
        ]:
            actions.append(i)

        powermenu_actions: TrackedList[dict] = TrackedList()
        for i in [
            {"command": "hyprlock", "icon": ""},
            {"command": "niri msg action quit --skip-confirmation", "icon": "󰈆"},
            {"command": "systemctl suspend", "icon": "󰤄"},
            {"command": "systemctl reboot", "icon": ""},
            {"command": "systemctl poweroff", "icon": "⏻"},
        ]:
            powermenu_actions.append(i)

    class Weather(OptionsGroup):
        location: str = "New-York"
        farenheit: bool = False

    class Settings(OptionsGroup):
        last_page: int = 0

    class Bar(OptionsGroup):
        position: str = "top"
        right: TrackedList[str] = TrackedList()
        right_spacing: int = 10
        center: TrackedList[str] = TrackedList()
        center_spacing: int = 20
        left: TrackedList[str] = TrackedList()
        left_spacing: int = 10

    class Wallpaper(OptionsGroup):
        wallpaper_path: str | None = None
        wallpaper_dir: str | None = None

    _bar: Bar = Bar()
    _settings: Settings = Settings()
    _user_config: UserConfig = UserConfig()
    _wallpaper: Wallpaper = Wallpaper()
    _applications: Options.Applications = Options.Applications()
    _notifications: Options.Notifications = Options.Notifications()
    _weather: Weather = Weather()

    @property
    def user_config(self) -> UserConfig:
        return self._user_config

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def notifications(self) -> Options.Notifications:
        return self._notifications

    @property
    def applications(self) -> Options.Applications:
        return self._applications

    @property
    def wallpaper(self) -> Wallpaper:
        return self._wallpaper

    @property
    def bar(self) -> Bar:
        return self._bar

    @property
    def weather(self) -> Weather:
        return self._weather


options = UserOptions()
