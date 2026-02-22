from exs_shell.utils import monitor
from exs_shell.ui.modules.corners import Corners
from exs_shell.ui.modules.bar.widget import Bar
from exs_shell.ui.modules.control_center.widget import ControlCenter
from exs_shell.ui.modules.notification.widget.popup import NotificationPopup
from exs_shell.ui.modules.osd.widget import OSD
from exs_shell.ui.modules.settings.widget import Settings
from exs_shell.ui.modules.launcher.widget import Launcher


def init() -> None:
    Settings()
    Launcher()
    OSD()
    ControlCenter()
    monitor.init_windows(Bar)
    monitor.init_windows(NotificationPopup)
    monitor.init_windows(Corners)
