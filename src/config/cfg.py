import os
import asyncio

from utils import PathUtils, Dirs, send_notification, kill_process

from config.log import logger

from base.singleton import SingletonClass

from ipc_utils.server import run_ipc_server

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
        self._app: IgnisApp = IgnisApp()
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

    def init_css(self) -> None:
        self.set_css_file("styles/main.scss")

    def init_widgets(self) -> None:
        from modules.osd import OSD
        from modules.bar import Bar
        from modules.notification import NotificationPopup, NotificationCenter
        from modules.launcher import Launcher
        from modules.lockscreen import LockScreen
        from modules.powermenu import PowenMenu
        from window import Settings

        Launcher.get_default()
        NotificationCenter.get_default()
        PowenMenu.get_default()
        OSD.get_default()

        for i in range(utils.get_n_monitors()):
            Bar(i)
            NotificationPopup(i)

        LockScreen()
        Settings.get_default()
        asyncio.create_task(run_ipc_server())

    def init(self) -> None:
        import window.wallpaper.background as _
        from ignis.services.niri import NiriService

        if not NiriService.get_default().is_available:
            logger.error("Niri is not available")
            exit(1)

        kill_process()
        Dirs.ensure_dirs_exist()
        self.init_css()
        self.init_widgets()

    def get_full_path(self, path: str) -> str:
        return os.path.abspath(os.path.expanduser(path))

    def __call__(self, config: str, debug: bool = False) -> None:
        from ignis.log_utils import configure_logger
        from ignis._deprecation import _enable_deprecation_warnings
        from ignis.config_manager import ConfigManager
        from ignis.client import IgnisClient

        client = IgnisClient()

        if client.has_owner:
            print("Exs-shell is already running.")
            exit(1)

        config_path = self.get_full_path(config)

        _enable_deprecation_warnings()
        configure_logger(debug)

        self.app.connect(
            "activate",
            lambda x: ConfigManager.get_default()._load_config(app=x, path=config_path),
        )

        try:
            self.app.run(None)
        except KeyboardInterrupt:
            pass


cfg = Config.get_default()
app = cfg.app
css_manager = cfg.css_manager
