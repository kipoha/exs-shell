from datetime import datetime

from ignis import widgets, utils


class Clock(widgets.Box):
    def __init__(self):
        super().__init__(
            vertical=True,
            valign="center",
            halign="center",
            css_classes=["dashboard-widget-clock"],
        )

        self.format = "%H:%M"
        self.poller = utils.Poll(1_000, self.get_time)
        self.label = widgets.Label(
            label=self.poller.bind("output"),
            css_classes=["dashboard-widget-clock-info"],
        )

        self.append(self.label)

    def get_time(self, *_):
        return datetime.now().strftime(self.format)
