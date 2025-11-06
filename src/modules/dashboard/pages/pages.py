from ignis import widgets

from modules.dashboard.pages.kanban import KanbanPage
from modules.dashboard.pages.main import MainPage
from modules.dashboard.pages.metrics import MetricsPage
from modules.dashboard.pages.player import PlayerPage


class DashboardPages(widgets.Box):
    def __init__(self, **kwargs):
        self.pages = {
            "dashboard": widgets.StackPage(
                title="Dashboard",
                child=MainPage(),
            ),
            "player": widgets.StackPage(
                title="Player",
                child=PlayerPage(),
            ),
            "metrics": widgets.StackPage(
                title="Metrics",
                child=MetricsPage(),
            ),
            "kanban": widgets.StackPage(
                title="Kanban",
                child=KanbanPage(),
            )
        }
        self.stack = widgets.Stack(
            child=self.pages.values(),
            transition_type="slide_left_right",
            transition_duration=300,
        )
        self.stack_switcher = widgets.StackSwitcher(
            css_classes=["dashboard-pages-switcher"],
            stack=self.stack
        )

        super().__init__(
            vertical=True,
            spacing=15,
            child=[
                self.stack_switcher,
                self.stack,
            ],
            css_classes=["dashboard-pages"],
            **kwargs
        )
