import traceback
import threading

from loguru import logger

from watchdog.observers import Observer
from watchdog.observers.api import BaseObserver

from exs_shell.app.watch import ReloadHandler
from exs_shell.utils.notify_system import send_notification
from exs_shell.utils.path import Paths
from exs_shell.utils.proc import kill_process
from exs_shell.app.vars import APP_NAME
from exs_shell.app.init import before, after

try:
    from ignis.log_utils import configure_logger
    from ignis.app import IgnisApp
    from ignis.css_manager import CssManager
    from ignis.client import IgnisClient
except ImportError:
    logger.error("Ignis is not installed")
    send_notification("Ignis", "Ignis is not installed")
    exit(1)


class App:
    _app: IgnisApp = IgnisApp()
    _css_manager: CssManager = CssManager.get_default()
    _watcher: BaseObserver | None = None

    @classmethod
    def watch_files(cls) -> None:
        handler = ReloadHandler()
        cls._watcher = Observer()
        cls._watcher.schedule(handler, str(Paths.root), recursive=True)
        cls._watcher.start()
        logger.info("Autoreloader started")

    @classmethod
    def before_init(cls, debug: bool) -> None:
        threading.Thread(target=cls.watch_files).start()
        kill_process()
        before.states.init()
        before.services.init()
        before.system.init()
        before.styles.init(cls._css_manager, debug)

    @classmethod
    def after_init(cls) -> None:
        after.system.init()
        after.services.init()
        after.modules.init()

    @classmethod
    def run(cls, debug: bool = False) -> None:
        client = IgnisClient()
        cls.before_init(debug)

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
        finally:
            cls._app.quit()
