import traceback

from loguru import logger

from exs_shell.utils.path import Paths
from exs_shell.utils.notify_system import send_notification

try:
    from ignis.log_utils import configure_logger
    from ignis.app import IgnisApp
    from ignis.css_manager import CssManager
    from ignis.config_manager import ConfigManager
    from ignis.client import IgnisClient
except ImportError:
    logger.error("Ignis is not installed")
    send_notification("Ignis", "Ignis is not installed")
    exit(1)

from exs_shell.app.vars import APP_NAME
from exs_shell.app.init import system, styles, states


class App:
    _app: IgnisApp = IgnisApp()
    _css_manager: CssManager = CssManager.get_default()

    @classmethod
    def run(cls, config: str, debug: bool = False) -> None:
        states.init()
        system.init()
        styles.init(cls._css_manager, debug)
        client = IgnisClient()

        if client.has_owner:
            print(f"{APP_NAME} is already running.")
            exit(1)

        if debug:
            from ignis._deprecation import _enable_deprecation_warnings

            _enable_deprecation_warnings()
        configure_logger(debug)

        cls._app.connect(
            "activate",
            lambda x: ConfigManager.get_default()._load_config(
                app=x, path=Paths.generate_path(config)
            ),
        )

        try:
            cls._app.run(None)
        except KeyboardInterrupt:
            pass
        except Exception:
            e = traceback.format_exc()
            logger.error(e)
        finally:
            cls._app.quit()
