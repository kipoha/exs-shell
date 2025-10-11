import os

from ignis.options_manager import OptionsGroup, OptionsManager

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
        user_avatar: str = ""
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
                "10": ""
            },
            "critical_level": 10,
        }

        actions: list[dict] = [
            {
                "name": "lock",
                "command": "exs-ipc toggle-lock",
                "icon": "lock"
            }
        ]

        powermenu_actions: list[dict] = [
            {"command": "hyprlock", "icon": ""},
            {"command": "niri msg action quit --skip-confirmation", "icon": "󰈆"},
            {"command": "systemctl suspend", "icon": "󰤄"},
            {"command": "systemctl reboot", "icon": ""},
            {"command": "systemctl poweroff", "icon": "⏻"},
        ]

    class Settings(OptionsGroup):
        last_page: int = 0

    _settings: Settings = Settings()
    _user_config: UserConfig = UserConfig()

    @property
    def user_config(self) -> UserConfig:
        return self._user_config

    @property
    def settings(self) -> Settings:
        return self._settings


options = UserOptions()
