import asyncio

from typing import Any

from ignis.widgets import Box
from ignis.services.audio import Stream
from ignis.services.backlight import BacklightService

from exs_shell import register
from exs_shell.interfaces.enums.gtk.transitions import RevealerTransition
from exs_shell.interfaces.enums.icons import Icons
from exs_shell.ui.widgets.base import MonitorRevealerBaseWidget
from exs_shell.ui.factory import window
from exs_shell.ui.widgets.custom.circle import ArcMeter
from exs_shell.ui.widgets.windows import Revealer
from exs_shell.utils.loop import run_async_task


@register.window
@register.event
class OSD(MonitorRevealerBaseWidget):
    def __init__(
        self,
    ) -> None:
        self.widget_build()
        self.hide_task = None
        win = window.create(
            "osd",
            visible=False,
            anchor=["bottom"],
            margin_bottom=20,
        )
        super().__init__(
            self._box,
            win,
            [self._rev_inner],
        )

    def volume_map_icon(self, volume: float) -> str:
        mapping = [
            (10, Icons.volume.LOW),
            (50, Icons.volume.MEDIUM),
            (75, Icons.volume.HIGH),
        ]

        for limit, icon in mapping:
            if volume <= limit:
                return icon

        return Icons.volume.OVERAMPLIFIED

    def backlight_map_icon(self, brightness: int) -> str:
        mapping = [
            (20, Icons.backlight.B1),
            (30, Icons.backlight.B2),
            (40, Icons.backlight.B3),
            (50, Icons.backlight.B4),
            (65, Icons.backlight.B5),
            (75, Icons.backlight.B6),
            (85, Icons.backlight.B7),
        ]

        for limit, icon in mapping:
            if brightness <= limit:
                return icon

        return Icons.backlight.B7

    @register.events.audio("notify::volume", "speaker")
    @register.events.audio("notify::is-muted", "speaker")
    def __on_volume(self, stream: Stream, *_: Any):
        self.show_osd()
        if stream.is_muted:
            self.progress.label = Icons.volume.MUTED
            self.progress.set_value(0)
        else:
            self.progress.label = self.volume_map_icon(stream.volume)  # type: ignore
            self.progress.set_value(stream.volume / 100)  # type: ignore

    @register.events.backlight("notify::brightness")
    def __on_brightness(self, backlight: BacklightService, *_: Any):
        self.show_osd()
        self.progress.label = self.backlight_map_icon(backlight.brightness / 1000)  # type: ignore
        self.progress.set_value(backlight.brightness / backlight.max_brightness)

    def widget_build(self) -> None:
        self.progress = ArcMeter(80, 10, font_size=30)
        self.inner = Box(child=[self.progress], css_classes=["exs-osd"])
        self._rev_inner = Revealer(
            child=self.inner,
            transition_type=RevealerTransition.CROSSFADE,
            transition_duration=200
        )
        self._box = Box(child=[self._rev_inner])

    def show_osd(self):
        self.set_visible(True)
        if self.hide_task:
            self.hide_task.cancel()
        self.hide_task = run_async_task(self._hide_osd())

    async def _hide_osd(self):
        await asyncio.sleep(2)
        self.set_visible(False)
