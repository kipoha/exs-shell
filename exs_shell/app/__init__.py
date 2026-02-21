import traceback

from loguru import logger

from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from exs_shell.app.watch import ReloadHandler
from exs_shell.app.vars import APP_NAME
from exs_shell.app.init import before, after
from exs_shell.utils.loop import run_in_thread
from exs_shell.utils.notify_system import send_notification
from exs_shell.utils.path import Paths
from exs_shell.utils.proc import kill_process

try:
    from ignis.app import IgnisApp
    from ignis.client import IgnisClient
    from ignis.css_manager import CssManager
    from ignis.log_utils import configure_logger
except ImportError:
    body = "Ignis is not installed"
    logger.error(body)
    send_notification("Ignis", body)
    raise ImportError(body, name="ignis")


class App:
    _app: IgnisApp = IgnisApp()
    _css_manager: CssManager = CssManager.get_default()
    _watcher: BaseObserver | None = None

    @classmethod
    @run_in_thread
    def watch_files(cls) -> None:
        handler = ReloadHandler()
        cls._watcher = Observer()
        cls._watcher.schedule(handler, str(Paths.root), recursive=True)
        cls._watcher.start()
        logger.info("Autoreloader started")

    @classmethod
    def before_init(cls, dev: bool, reload: bool = False) -> None:
        if reload:
            cls.watch_files()
        kill_process()
        before.states.init()
        before.files.init()
        before.services.init()
        before.system.init()
        before.styles.init(cls._css_manager, dev)

    @classmethod
    def after_init(cls) -> None:
        after.system.init()
        after.services.init()
        after.modules.init()

    @classmethod
    def run(cls, dev: bool = False, debug: bool = False, reload: bool = False) -> None:
        client = IgnisClient()
        cls.before_init(dev, reload)

        if client.has_owner:
            logger.error(f"{APP_NAME} is already running.")
            exit(1)

        if debug:
            from ignis._deprecation import _enable_deprecation_warnings

            _enable_deprecation_warnings()
        configure_logger(debug)

        cls._app.connect("activate", lambda _: cls.after_init())

        try:
            cls._app.run(None)
        except KeyboardInterrupt:
            pass
        except Exception:
            e = traceback.format_exc()
            logger.error(e)
