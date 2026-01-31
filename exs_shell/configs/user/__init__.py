import os

from ignis.options_manager import OptionsManager
from ignis.options import Options

from exs_shell.utils.path import Dirs
from exs_shell.configs.user.appearence import Appearance
from exs_shell.configs.user.bar import Bar
from exs_shell.configs.user.main import UserConfig
from exs_shell.configs.user.notification import Notifications
from exs_shell.configs.user.weather import Weather


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

    _bar: Bar = Bar()
    _user_config: UserConfig = UserConfig()
    _appearance: Appearance = Appearance()
    _applications: Options.Applications = Options.Applications()
    _notifications: Notifications = Notifications()
    _weather: Weather = Weather()

    @property
    def user_config(self) -> UserConfig:
        return self._user_config

    @property
    def notifications(self) -> Notifications:
        return self._notifications

    @property
    def applications(self) -> Options.Applications:
        return self._applications

    @property
    def appearance(self) -> Appearance:
        return self._appearance

    @property
    def bar(self) -> Bar:
        return self._bar

    @property
    def weather(self) -> Weather:
        return self._weather


options = UserOptions()
user = options.user_config
notifications = options.notifications
appearance = options.appearance
applications = options.applications
bar = options.bar
weather = options.weather
