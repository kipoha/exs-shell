from exs_shell.utils import monitor
from exs_shell.ui.modules.notification.widget.center import NotificationCenter
from exs_shell.ui.modules.notification.widget.popup import NotificationPopup
from exs_shell.ui.modules.settings.osd.widget import OSD
from exs_shell.ui.modules.settings.widget import Settings
from exs_shell.ui.modules.launcher.widget import Launcher
from exs_shell.ui.modules.bar.widget import Bar


def init() -> None:
    Settings()
    Launcher()
    OSD()
    NotificationCenter()
    monitor.init_windows(Bar)
    monitor.init_windows(NotificationPopup)
