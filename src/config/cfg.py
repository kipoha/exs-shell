import json

from typing import Any

from commands.osd import generate_osd_commands
from commands.notification import generate_notification_commands
from commands.launcher import generate_launcher_commands
from utils import PathUtils, send_notification

from config.log import logger

from base.singleton import SingletonClass

try:
    from ignis import utils
    from ignis.app import IgnisApp
    from ignis.css_manager import CssManager, CssInfoPath
except ImportError:
    logger.error("Ignis is not installed")
    send_notification("Ignis", "Ignis is not installed")
    exit(1)


class Config(SingletonClass):
    NAMESPACE: str = "EXS_SHELL"

    def __init__(self):
        self._app: IgnisApp = IgnisApp.get_initialized()
        self._css_manager: CssManager = CssManager.get_default()

    @property
    def app(self) -> IgnisApp:
        return self._app

    @property
    def css_manager(self) -> CssManager:
        return self._css_manager

    def set_css_file(self, css_file_path: str | list[str]) -> None:
        file = (
            css_file_path
            if isinstance(css_file_path, str)
            else css_file_path[-1]
            if len(css_file_path) > 0
            else ""
        )
        if file.split(".")[-1] != "scss":
            logger.error("File must be a scss file")
            exit(1)

        self.css_manager.apply_css(
            CssInfoPath(
                name="exs-shell",
                compiler_function=lambda path: utils.sass_compile(path),
                path=PathUtils.generate_path(css_file_path),
            )
        )

    def init_css(self):
        self.set_css_file("styles/main.scss")

    def init_widgets(self):
        from modules import (
            Bar,
            OSD,
            Launcher,
            LockScreen,
            NotificationPopup,
            NotificationCenter,
        )

        from window import Settings
        launcher = Launcher()
        generate_launcher_commands(launcher)
        notification_center = NotificationCenter()
        generate_notification_commands(notification_center)
        osd = OSD()
        generate_osd_commands(osd)

        for i in range(utils.get_n_monitors()):
            Bar(i)
            NotificationPopup(i)

        LockScreen()
        Settings()

    def __call__(self) -> None:
        self.init_css()
        self.init_widgets()


cfg = Config.get_default()
app = cfg.app
css_manager = cfg.css_manager


def get_user_config() -> dict[str, Any]:
    config_file = PathUtils.generate_path("config.jsonc", PathUtils.root)
    try:
        with open(config_file, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "clock_format": "󰥔 %H:%M:%S",
        }


user_config = get_user_config()
