from exs_shell.ui.modules.settings.widget import Settings
from exs_shell.ui.modules.bar.widget import init_bars


def init() -> None:
    Settings()
    init_bars()
