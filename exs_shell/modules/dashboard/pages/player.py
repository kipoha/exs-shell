from ignis import widgets

from exs_shell.modules.dashboard.widgets.mpris import MprisPlayerWidget
from exs_shell.modules.dashboard.widgets.shared.mpris import MprisPlayerManager


class PlayerPage(widgets.Box):
    def __init__(self):
        super().__init__(
            spacing=10,
            css_classes=["dashboard-page-player"],
            child=[
                MprisPlayerManager(MprisPlayerWidget, "mpris"),
            ],
        )
