from typing import Any

from datetime import datetime

from ignis.widgets import Label

from exs_shell import register
from exs_shell.configs.user import user


@register.event
class Clock(Label):
    def __init__(self, **kwargs: Any):
        self.format = user.clock_format
        kwargs.pop("label", None)
        super().__init__(
            label=self.format_dt(),
            **kwargs,
        )

    def format_dt(self) -> str:
        return datetime.now().strftime(self.format)

    @register.events.option(user, "clock_format")
    def update_format(self):
        self.format = user.clock_format
        self.update_label()

    @register.events.poll(1_000)
    def update_label(self):
        self.set_label(self.format_dt())
