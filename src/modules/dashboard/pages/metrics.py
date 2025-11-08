from ignis import widgets
from modules.dashboard.widgets.metrics import SystemMonitor


class MetricsPage(widgets.Box):
    def __init__(self):
        super().__init__(
            spacing=10,
            css_classes=["dashboard-page-player"],
            child=[SystemMonitor()],
        )
