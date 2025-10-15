from ignis import widgets
from window.settings.elements.row import SettingsRow
from typing import Callable

class SliderRow(SettingsRow):
    def __init__(
        self,
        value: float = 0.0,
        min: float = 0.0,
        max: float = 100.0,
        step: float = 1.0,
        on_change: Callable[[float], None] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self._scale = widgets.Scale(
            value=value,
            # draw_value=True,
            min=min,
            max=max,
            step=step,
            hexpand=True,
            halign="end",
        )
        self._scale.set_size_request(200, -1)

        if on_change:
            self._scale.connect("value-changed", lambda w: on_change(w.get_value()))

        self.child.append(self._scale)
