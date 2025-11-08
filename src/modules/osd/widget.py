import asyncio


from gi.repository import GLib  # type: ignore

from ignis import widgets, utils

from base.window.animated import PartiallyAnimatedWindow
from base.singleton import SingletonClass

from config import config


class OSDProgress(widgets.Box):
    def __init__(self, icon: str, name: str):
        super().__init__(vertical=True, halign="center", valign="center", spacing=20)
        self._name = name
        self._icon_active = icon
        self._icon_muted = "" if name == "volume" else icon
        self._label = widgets.Label(label=icon, css_classes=[f"{name}-icon"])
        self._bar = widgets.Scale(
            orientation="vertical",
            min=0,
            max=100,
            value=0,
            css_classes=[f"{name}-bar"],
        )
        self._bar.set_sensitive(False)

        self._current_value = 0
        self._target_value = 0
        self._anim_source = None
        self._muted = False

        self.append(self._bar)
        self.append(self._label)

    def update(self, value: int):
        self._target_value = max(0, min(100, value))
        if self._anim_source is None:
            self._anim_source = GLib.timeout_add(10, self._animate_step)

    def _animate_step(self):
        diff = self._target_value - self._current_value
        if abs(diff) < 1:
            self._current_value = self._target_value
            self._bar.set_value(self._current_value)
            self._anim_source = None
            return False
        self._current_value += diff * 0.2
        self._bar.set_value(self._current_value)
        return True

    def set_muted(self, muted: bool):
        self._muted = muted
        self._label.set_label(self._icon_muted if muted else self._icon_active)


class OSD(PartiallyAnimatedWindow, SingletonClass):
    def __init__(self, **kwargs):
        super().__init__(
            namespace=f"{config.NAMESPACE}_osd",
            popup=True,
            layer="overlay",
            visible=False,
            anchor=["left"],
            **kwargs,
        )

        self._hide_timeout = None
        self._last_device = None
        self._volume_value = 0
        self._brightness_value = 0

        asyncio.create_task(self.async_init())

        self._volume_widget = OSDProgress("", "volume")
        self._brightness_widget = OSDProgress("󰃞", "brightness")

        self._box = widgets.Box(
            vertical=False,
            spacing=12,
            halign="center",
            valign="center",
            css_classes=["osd-container", "hidden"],
            child=[
                self._volume_widget,
                self._brightness_widget,
            ],
        )

        self.top_corner = widgets.Corner(
            css_classes=["osd-left-corner", "hidden"],
            orientation="bottom-left",
            width_request=35,
            height_request=50,
            halign="start",
            valign="end",
        )
        self.bottom_corner = widgets.Corner(
            css_classes=["osd-right-corner", "hidden"],
            orientation="top-left",
            width_request=35,
            height_request=50,
            halign="start",
            valign="end",
        )

        self._main_box = widgets.Box(
            vertical=True,
            css_classes=["osd-block"],
            child=[
                self.top_corner,
                self._box,
                self.bottom_corner,
            ],
        )

        self.set_child(self._main_box)

        self._animated_parts = [self.top_corner, self._box, self.bottom_corner]

        self._volume_widget.update(self._volume_value)
        self._brightness_widget.update(self._brightness_value)

        self._start_device_monitor()

    async def async_init(self):
        self._volume_value = await self.get_volume()
        self._brightness_value = await self.get_brightness()
        self._volume_widget.update(self._volume_value)
        self._brightness_widget.update(self._brightness_value)

    async def get_volume(self) -> int:
        try:
            result = await utils.exec_sh_async("wpctl get-volume @DEFAULT_AUDIO_SINK@")
            parts = result.stdout.strip().split()
            return int(float(parts[1]) * 100) if len(parts) > 1 else 0
        except Exception:
            return 0

    async def get_brightness(self) -> int:
        try:
            result = await utils.exec_sh_async("brightnessctl get")
            bright = int(result.stdout.strip())
            result = await utils.exec_sh_async("brightnessctl max")
            max_bright = int(result.stdout.strip())
            return int(bright * 100 / max_bright)
        except Exception:
            return 0

    def show_osd(self):
        if not self._is_open:
            self.open()
        else:
            if self._hide_timeout:
                try:
                    GLib.source_remove(self._hide_timeout)
                except Exception:
                    pass

        self._hide_timeout = GLib.timeout_add_seconds(1, self.hide_osd)

    def hide_osd(self):
        if self._is_open:
            self.close()

        self._hide_timeout = None
        return False

    def update_volume(self, up: bool = True):
        step = 5 if up else -5
        self._volume_value = max(0, min(100, self._volume_value + step))
        self._volume_widget.update(self._volume_value)
        self.show_osd()
        asyncio.create_task(self._set_volume_shell())

    async def _set_volume_shell(self):
        try:
            await utils.exec_sh_async(
                f"wpctl set-volume @DEFAULT_AUDIO_SINK@ {self._volume_value / 100.0}"
            )
        except Exception:
            pass

    def toggle_mute(self):
        self.show_osd()
        GLib.timeout_add(100, self._update_mute_state)
        asyncio.create_task(self._set_mute_shell())

    async def _set_mute_shell(self):
        await utils.exec_sh_async("wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle")

    async def _update_mute_state(self):
        try:
            out = (
                await utils.exec_sh_async("wpctl get-volume @DEFAULT_AUDIO_SINK@")
            ).stdout
            self._volume_widget.set_muted("MUTED" in out)
        except Exception:
            pass
        return False

    def update_brightness(self, up: bool = True):
        step = 5 if up else -5
        self._brightness_value = max(1, min(100, self._brightness_value + step))
        self._brightness_widget.update(self._brightness_value)
        self.show_osd()
        asyncio.create_task(self._set_brightness_shell())

    async def _set_brightness_shell(self):
        try:
            await utils.exec_sh_async(f"brightnessctl set {self._brightness_value}%")
        except Exception:
            pass

    def _start_device_monitor(self):
        self._last_device = None

        async def poll_device():
            try:
                out = (await utils.exec_sh_async("pactl info")).stdout
                for line in out.splitlines():
                    if line.startswith("Default Sink:"):
                        device = line.split(":", 1)[1].strip()
                        if device != self._last_device:
                            self._last_device = device
                            self._volume_value = await self.get_volume()
                            self._volume_widget.update(self._volume_value)
                            self.show_osd()
                        break
            except Exception:
                pass
            return True

        def poll_wrapper():
            asyncio.create_task(poll_device())
            return True

        GLib.timeout_add_seconds(2, poll_wrapper)
