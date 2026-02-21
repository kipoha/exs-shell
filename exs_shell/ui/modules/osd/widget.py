import asyncio

from typing import Any

from ignis.widgets import Box, Label, Scale
from ignis.services.audio import Stream
from ignis.services.backlight import BacklightService

from exs_shell import register
from exs_shell.configs.user import osd
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.widgets.base import MonitorRevealerBaseWidget
from exs_shell.ui.factory import window
from exs_shell.ui.widgets.custom.circle import ArcMeter
from exs_shell.ui.widgets.custom.icon import Icon
from exs_shell.ui.widgets.windows import Revealer
from exs_shell.utils.loop import run_async_task


@register.window
@register.event
@register.commands
class OSD(MonitorRevealerBaseWidget):
    def __init__(
        self,
    ) -> None:
        self.widget_build()
        self.hide_task = None
        win = window.create(
            "osd",
            visible=False,
            anchor=osd.position.split("_"),  # type: ignore
            margin_bottom=20,
            margin_left=20,
            margin_right=20,
            margin_top=20,
        )
        super().__init__(
            self._box,
            win,
            [self._rev_inner],
        )

    @register.events.audio("notify::volume", "speaker")
    @register.events.audio("notify::is-muted", "speaker")
    def __on_volume(self, stream: Stream, *_: Any):
        self.show_osd()
        if stream.is_muted:
            data = {"label": Icons.volume.MUTED, "value": 0}
        else:
            data = {
                "label": Icons.volume.mapping(stream.volume),  # type: ignore
                "value": stream.volume / 100,  # type: ignore
            }
        self.update_progress(**data)  # type: ignore

    @register.events.backlight("notify::brightness")
    def __on_brightness(self, backlight: BacklightService, *_: Any):
        self.show_osd()
        self.update_progress(
            Icons.backlight.mapping(backlight.brightness / 1000),  # type: ignore
            backlight.brightness / backlight.max_brightness,
        )

    @register.events.option(osd, "osd")
    @register.events.option(osd, "position")
    def reload(self, *_: Any):
        if isinstance(self.progress, ArcMeter):
            i = self.progress.label
            p = self.progress.get_value()
        else:
            i = self.icon.label
            p = self.progress.get_value()

        self.win_dict["anchor"] = osd.position.split("_")
        self.widget_build()
        self.set_revealers([self._rev_inner])
        self.recreate_window()

    def update_progress(self, label: str, value: float):
        if isinstance(self.progress, ArcMeter):
            self.progress.label = label
            self.progress.set_value(value)
        elif isinstance(self.progress, Scale):
            self.progress.set_value(value)
            self.icon.label = label
        else:
            raise ValueError

    def widget_build(self) -> None:
        vertical = osd.position in ["left", "right"]
        if osd.osd == "arc":
            self.progress = ArcMeter(80, 10, font_size=30)

            self.inner = Box(child=[self.progress], css_classes=["exs-osd"])
        else:
            self.progress = Scale(
                vertical=vertical,
                min=0,
                max=1,
                value=0.5,
                sensitive=False,
                step=0.01,
                css_classes=[
                    "exs-osd-progress",
                    "vertical" if vertical else "horizontal",
                ],
            )
            self.icon = Icon(
                label=Icons.volume.MUTED,
                size="l",
                css_classes=["vertical" if vertical else "horizontal"]
            )
            self.inner = Box(
                child=[self.icon, self.progress],
                css_classes=["exs-osd"],
                vertical=vertical,
                spacing=5,
            )
        self._rev_inner = Revealer(
            child=self.inner,
            transition_type=RevealerTransition.CROSSFADE,
            transition_duration=200,
        )
        self._box = Box(child=[self._rev_inner])

    def show_osd(self):
        self.set_visible(True)
        if self.hide_task:
            self.hide_task.cancel()
        self.hide_task = run_async_task(self._hide_osd())

    async def _hide_osd(self):
        try:
            await asyncio.sleep(2)
            self.set_visible(False)
        except asyncio.CancelledError:
            pass

    @register.command(group="osd", name="show", description="Show OSD")
    def toggle(self):
        self.update_progress(Icons.volume.MUTED, 0)
        self.show_osd()
