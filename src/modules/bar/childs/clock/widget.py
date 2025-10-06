import datetime

from ignis import utils, widgets

from config import user_config


class Clock(widgets.Label):
    def __init__(self, **kwargs):
        super().__init__(
            css_classes=["clock"],
            label=utils.Poll(
                1_000, lambda _: datetime.datetime.now().strftime(user_config.get('clock_format', "󰥔 %H:%M:%S"))
            ).bind("output"),
            **kwargs
        )
