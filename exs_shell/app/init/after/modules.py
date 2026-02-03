from exs_shell.ui.modules.settings.widget import Settings
from exs_shell.ui.modules.launcher.widget import Launcher
from exs_shell.ui.modules.bar.widget import init_bars


def init() -> None:
    Settings()
    Launcher()
    init_bars()
