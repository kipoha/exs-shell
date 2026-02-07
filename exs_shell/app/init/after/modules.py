from exs_shell.utils import monitor
from exs_shell.ui.modules.settings.widget import Settings
from exs_shell.ui.modules.launcher.widget import Launcher
from exs_shell.ui.modules.bar.widget import Bar


def init() -> None:
    Settings()
    Launcher()
    monitor.init_windows(Bar)
