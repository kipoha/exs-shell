from ignis import widgets

from modules.dashboard.widgets.mpris import MprisPlayerManager


class PlayerPage(widgets.Box):
    def __init__(self):
        super().__init__(
            spacing=10,
            css_classes=["dashboard-page-player"],
            child=[
                MprisPlayerManager(),
            ],
        )
