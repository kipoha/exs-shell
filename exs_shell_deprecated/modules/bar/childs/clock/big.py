import datetime

from ignis import utils, widgets

from exs_shell_deprecated.base.singleton import SingletonClass
from exs_shell_deprecated.config.user import options

class Clock(widgets.Label, SingletonClass):
    def __init__(self, **kwargs):
        self.format = options.user_config.clock_format
        super().__init__(
            css_classes=["clock"],
            label=utils.Poll(
                1_000, lambda _: datetime.datetime.now().strftime(self.format)
            ).bind("output"),
            **kwargs
        )

        options.user_config.connect_option("clock_format", self.update_format)

    def update_format(self):
        self.format = options.user_config.clock_format
        self.update_label()

    def update_label(self):
        self.set_label(datetime.datetime.now().strftime(self.format))
