import datetime

from ignis import utils, widgets

from config.user import options

class Clock(widgets.Label):
    def __init__(self, **kwargs):
        super().__init__(
            css_classes=["clock"],
            label=utils.Poll(
                1_000, lambda _: datetime.datetime.now().strftime(options.user_config.clock_format)
            ).bind("output"),
            **kwargs
        )
