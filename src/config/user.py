import os

from ignis.options_manager import OptionsGroup, OptionsManager, TrackedList
from ignis.options import Options

from utils import Dirs


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

        actions: list[dict] = [
            {"name": "Lock", "command": "exs-ipc open-lockscreen", "icon": "lock"},
            {"name": "Clipboard", "command": "exs-ipc toggle-clipboard", "icon": "clipboard"},
        ]
        # actions: TrackedList[dict] = TrackedList()
        # actions.append({"name": "lock", "command": "exs-ipc toggle-lock", "icon": "lock"})

        powermenu_actions: TrackedList[dict] = TrackedList()
        for i in [
            {"command": "hyprlock", "icon": ""},
            {"command": "niri msg action quit --skip-confirmation", "icon": "󰈆"},
            {"command": "systemctl suspend", "icon": "󰤄"},
            {"command": "systemctl reboot", "icon": ""},
            {"command": "systemctl poweroff", "icon": "⏻"},
        ]:
            powermenu_actions.append(i)

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


options = UserOptions()
